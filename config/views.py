from measuremeterdata.models import Measure, Country, MeasureType, MeasureCategory, CHCases, CHCanton, CHMeasure, CasesDeaths
from django.shortcuts import get_object_or_404, render
from datetime import date, timedelta
from django.template import loader
from django.http import HttpResponse

def render_country(request, country_name):
    item = get_object_or_404(Country, code=country_name)
    return render(request, 'pages/country.html', {'item': item })

def render_euromap(request, measure_id):
    item = get_object_or_404(MeasureType, pk=measure_id)
    return render(request, 'pages/euromap.html', {'item': item })

def render_timeline(request, country_name):
    return render(request, 'pages/timeline.html', {'items': country_name })

def render_compare(request, country_name):
    return render(request, 'pages/compare.html', {'items': country_name })


def calc_ranking_countries(countries):
    country_vals = []

    for country in countries:
        date_tocheck = date.today()

        print(country)

        cases = CasesDeaths.objects.filter(country=country, date__range=[date_tocheck - timedelta(days=60), date_tocheck]).order_by("-date")

        last_date = cases[0].date
        last_prev14 = cases[0].cases_past14days
        last_deaths14 = cases[0].deaths_past14days
        last_positivity = None
        last_positivity_date = None
        positivity_last7 = 0.0
        positivity_last7_count = 0
        positivity_before7 = 0.0
        positivity_before7_count = 0
        pos_count = 0
        for case in cases:
            if (case.positivity != None and last_positivity == None):
                last_positivity = case.positivity
                last_positivity_date = case.date

            if (case.positivity != None):
                if (pos_count < 7):
                    positivity_last7 += float(case.positivity)
                    positivity_last7_count += 1
                else:
                    positivity_before7 += float(case.positivity)
                    positivity_before7_count += 1
                pos_count += 1



        past_date_tocheck = last_date - timedelta(days=14)
        past_past_date_tocheck = past_date_tocheck - timedelta(days=14)

        case_14days_7daysago = CasesDeaths.objects.get(country=country, date=last_date - timedelta(days=7))
        case_14days_14daysago = CasesDeaths.objects.get(country=country, date=past_date_tocheck)
        case_14days_21daysago = CasesDeaths.objects.get(country=country, date=last_date - timedelta(days=21))

        if (case_14days_14daysago.cases_past14days > 0):
            tendency = ((cases[0].cases_past14days * 100 / case_14days_14daysago.cases_past14days) - 100)
        else:
            tendency = ((cases[0].cases_past14days * 100 / 1) - 100)

        if (case_14days_21daysago.cases_past14days > 0):
            tendency_7daysbefore = ((case_14days_7daysago.cases_past14days * 100 / case_14days_21daysago.cases_past14days) - 100)
        else:
            tendency_7daysbefore = ((case_14days_7daysago.cases_past14days * 100 / 1) - 100)

        print(positivity_last7)
        print(positivity_last7_count)
        print(positivity_before7)
        print(positivity_before7_count)


        if (last_positivity == None):
            positivity_last7 = 5
            positivity_last7_count = 1
            positivity_before7 = 5
            positivity_before7_count = 1

        print(str(float(cases[0].cases_past14days)) +"//" + str(float(cases[0].cases_past7days)) +"//" + str(float((tendency / 5))) +"//" +  str(float((cases[0].deaths_past14days * 100))) +"//" + str(float((positivity_last7 / positivity_last7_count *10))))
        print(str(float(case_14days_14daysago.cases_past14days)) +"//" + str(float(case_14days_14daysago.cases_past7days)) +"//" + str(float((tendency_7daysbefore / 5))) +"//" + str(float((case_14days_14daysago.deaths_past14days * 100))) +"//" + str(float((positivity_before7 / positivity_before7_count * 10))))

        score = float(cases[0].cases_past14days) + float(cases[0].cases_past7days) + float((tendency / 5)) +  float((cases[0].deaths_past14days * 100)) + float((positivity_last7 / positivity_last7_count *50))
        score_7days_before = float(case_14days_7daysago.cases_past14days) + float(case_14days_7daysago.cases_past7days) + float((tendency_7daysbefore / 5)) + float((case_14days_7daysago.deaths_past14days * 100)) + float((positivity_before7 / positivity_before7_count * 50))

        if (score > score_7days_before):
            arrow = "arrow circle up red"
        elif (score == score_7days_before):
            arrow = "arrow circle left orange"
        else:
            arrow = "arrow circle down green"

        canton_toadd = {"name": country.name, "score": int(score), "score_before": int(score_7days_before),
                        "date": last_date, "code": country.code,
                        "cur_prev14": last_prev14, "tendency": int(tendency),
                        "cur_prev7": case_14days_14daysago.cases_past7days, "tendency7": int(tendency_7daysbefore),
                        "positivity": last_positivity, "positivity_date":last_positivity_date, "deaths": last_deaths14,
                        "has_measures": country.has_measures, "continent": country.continent.pk, "icon": arrow}

        country_vals.append(canton_toadd)

    scores = sorted(country_vals, key=lambda i: i['score_before'],reverse=False)
    rank = 1
    for score in scores:
        score["rank_old"] = rank
        rank += 1

    scores = sorted(scores, key=lambda i: i['score'],reverse=False)
    rank = 1
    for score in scores:
        score["rank"] = rank
        score["rank_diff"] = score["rank_old"] - rank
        rank += 1
        if (score["rank"] < score["rank_old"]):
            score["rank_icon"] = "arrow circle up green"
        elif (score["rank"] == score["rank_old"]):
            score["rank_icon"] = "arrow circle left orange"
        else:
            score["rank_icon"] = "arrow circle down red"


    context = {
        'countries': scores,
    }
    return context

def ranking_world(request):
    countries = Country.objects.all()
    context = calc_ranking_countries(countries)

    template = loader.get_template('pages/ranking_world.html')
    return HttpResponse(template.render(context, request))



def ranking_europe(request):

    countries = Country.objects.filter(continent=1)
    context = calc_ranking_countries(countries)

    template = loader.get_template('pages/ranking_europe.html')
    return HttpResponse(template.render(context, request))

def ranking(request):

    cantons = CHCanton.objects.filter(level=0)
#    cantons = CHCanton.objects.all()
    canton_vals = []

    for canton in cantons:
        date_tocheck = date.today()

        cases = CHCases.objects.filter(canton=canton, date__range=[date_tocheck - timedelta(days=10), date_tocheck]).order_by("-date")

        last_date = cases[0].date
        last_prev7 = cases[0].incidence_past7days
        last_prev14 = cases[0].incidence_past14days
        past_date_tocheck = last_date - timedelta(days=7)
        past_past_date_tocheck = past_date_tocheck - timedelta(days=7)

        case_7days_before = CHCases.objects.get(canton=canton, date=past_date_tocheck)
        case_7days_before_before = CHCases.objects.get(canton=canton, date=past_past_date_tocheck)


        if (case_7days_before.incidence_past7days > 0):
            tendency = ((cases[0].incidence_past7days * 100 / case_7days_before.incidence_past7days) - 100)
        else:
            tendency = ((cases[0].incidence_past7days * 100 / 1) - 100)

        if (case_7days_before_before.incidence_past7days > 0):
            tendency_7daysbefore = ((case_7days_before.incidence_past7days * 100 / case_7days_before_before.incidence_past7days) - 100)
        else:
            tendency_7daysbefore = ((case_7days_before.incidence_past7days * 100 / 1) - 100)


        score = 0 - cases[0].incidence_past7days - (tendency / 5)
        score_7days_before = 0 - case_7days_before.incidence_past7days - (tendency_7daysbefore / 5)

        if (score > score_7days_before):
            arrow = "arrow circle up green"
        elif (score == score_7days_before):
            arrow = "arrow circle left orange"
        else:
            arrow = "arrow circle down red"

        canton_toadd = {"name": canton.name, "score": int(score), "score_before": int(score_7days_before),
                        "date": last_date, "code": canton.code,
                        "cur_prev": last_prev7, "cur_prev14": last_prev14, "tendency": int(tendency),
                        "cur_prev7": case_7days_before.incidence_past7days, "tendency7": int(tendency_7daysbefore), "icon": arrow}

        canton_vals.append(canton_toadd)

    scores = sorted(canton_vals, key=lambda i: i['score_before'],reverse=True)
    rank = 1
    for score in scores:
        score["rank_old"] = rank
        rank += 1

    scores = sorted(scores, key=lambda i: i['score'],reverse=True)
    rank = 1
    for score in scores:
        score["rank"] = rank
        score["rank_diff"] = score["rank_old"] - rank
        rank += 1
        if (score["rank"] < score["rank_old"]):
            score["rank_icon"] = "arrow circle up green"
        elif (score["rank"] == score["rank_old"]):
            score["rank_icon"] = "arrow circle left orange"
        else:
            score["rank_icon"] = "arrow circle down red"


    template = loader.get_template('pages/ranking.html')
    context = {
        'cantons': scores,
    }
    return HttpResponse(template.render(context, request))

def ranking14_calc(cantons):
    canton_vals = []

    for canton in cantons:
        date_tocheck = date.today()

        print(canton)

        cases = CHCases.objects.filter(canton=canton, date__range=[date_tocheck - timedelta(days=10), date_tocheck]).order_by("-date")
        print("got the cases")

        try:
            last_date = cases[0].date
            last_prev = cases[0].incidence_past14days
            past_date_tocheck = last_date - timedelta(days=14)
            past_past_date_tocheck = past_date_tocheck - timedelta(days=14)

            print("check the past")

            case_14days_before = CHCases.objects.get(canton=canton, date=past_date_tocheck)
            case_14days_before_before = CHCases.objects.get(canton=canton, date=past_past_date_tocheck)
            print("checked")

            if (case_14days_before.incidence_past14days is not None):
                if (case_14days_before.incidence_past14days > 0):
                    tendency = ((cases[0].incidence_past14days * 100 / case_14days_before.incidence_past14days) - 100)
                else:
                    tendency = ((cases[0].incidence_past14days * 100 / 1) - 100)
            else:
                tendency = 0

            if (case_14days_before_before.incidence_past14days is not None):
                if (case_14days_before_before.incidence_past14days > 0):
                    tendency_14daysbefore = ((case_14days_before.incidence_past14days * 100 / case_14days_before_before.incidence_past14days) - 100)
                else:
                    tendency_14daysbefore = ((case_14days_before.incidence_past14days * 100 / 1) - 100)
            else:
                tendency_14daysbefore = 0

            score_14days_before = 0 - case_14days_before.incidence_past14days - (tendency_14daysbefore / 5)
            score = 0 - cases[0].incidence_past14days - (tendency / 5)
        except:
            tendency = 0
            tendency_14daysbefore = 0
            score = -999
            score_14days_before = -999


        if (score > -999):
            if (score > score_14days_before):
                arrow = "arrow circle up green"
            elif (score == score_14days_before):
                arrow = "arrow circle left orange"
            else:
                arrow = "arrow circle down red"

            canton_toadd = {"name": canton.name, "score": int(score),"score_before": int(score_14days_before),
                            "date": last_date, "cur_prev": last_prev,
                            "tendency": int(tendency), "icon": arrow, "level": canton.level, "code": canton.code, "id": canton.swisstopo_id}
            canton_vals.append(canton_toadd)

    print("finished getting cases")

    scores = sorted(canton_vals, key=lambda i: i['score_before'],reverse=True)
    rank = 1
    for score in scores:
        score["rank_old"] = rank
        rank += 1

    scores = sorted(scores, key=lambda i: i['score'],reverse=True)
    rank = 1
    for score in scores:
        score["rank"] = rank
        score["rank_diff"] = score["rank_old"] - rank
        rank += 1
        if (score["rank"] < score["rank_old"]):
            score["rank_icon"] = "arrow circle up green"
        elif (score["rank"] == score["rank_old"]):
            score["rank_icon"] = "arrow circle left orange"
        else:
            score["rank_icon"] = "arrow circle down red"

    return scores

def ch(request):
    measures = CHMeasure.objects.all().order_by('-created')[:10]

    template = loader.get_template('pages/ch.html')
    context = {
        'measures': measures,
    }
    return HttpResponse(template.render(context, request))

def international(request):
    measures = Measure.objects.all().order_by('-created')[:10]

    template = loader.get_template('pages/home.html')
    context = {
        'measures': measures,
    }
    return HttpResponse(template.render(context, request))

def ranking14(request):

    cantons = CHCanton.objects.filter(level=0)

    scores = ranking14_calc(cantons)

    template = loader.get_template('pages/ranking14.html')
    context = {
        'cantons': scores,
    }
    return HttpResponse(template.render(context, request))


def ranking14_all(request):
    cantons = CHCanton.objects.all()

    scores = ranking14_calc(cantons)
    print(scores)

    template = loader.get_template('pages/ranking14.html')
    context = {
        'cantons': scores,
    }
    return HttpResponse(template.render(context, request))
