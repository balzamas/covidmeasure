from measuremeterdata.models.models_ch import CHCases, CHCanton, CHMeasure
from django.shortcuts import get_object_or_404, render
from datetime import date, timedelta
from django.template import loader
from django.http import HttpResponse
from django.db.models import F, Func, Q


def ranking7_calc(cantons):
    canton_vals = []

    for canton in cantons:
        date_tocheck = date.today()

        cases = CHCases.objects.filter(canton=canton, date__range=[date_tocheck - timedelta(days=10), date_tocheck]).order_by("-date")

        try:
            if (canton.level == 0 and cases[0].date == date.today()):
                last_date = cases[1].date
                last_prev7 = cases[1].incidence_past7days
                last_prev14 = cases[1].incidence_past14days
                last_tendency = cases[1].development7to7

                past_date_tocheck = last_date - timedelta(days=7)

                case_7days_before = CHCases.objects.get(canton=canton, date=past_date_tocheck)

                score = 0 - cases[1].incidence_past7days - (last_tendency * 2)
            else:
                last_date = cases[0].date
                last_prev7 = cases[0].incidence_past7days
                last_prev14 = cases[0].incidence_past14days
                last_tendency = cases[0].development7to7

                past_date_tocheck = last_date - timedelta(days=7)

                case_7days_before = CHCases.objects.get(canton=canton, date=past_date_tocheck)

                score = 0 - cases[0].incidence_past7days - (last_tendency * 2)

            score_7days_before = 0 - case_7days_before.incidence_past7days - (case_7days_before.development7to7 * 2)
        except:
            score = -99999
            score_14days_before = -99999

        if (score > score_7days_before):
            arrow = "arrow circle up green"
        elif (score == score_7days_before):
            arrow = "arrow circle left orange"
        else:
            arrow = "arrow circle down red"

        measures = CHMeasure.objects.filter(canton=canton).filter(Q(end__gte=date.today())|Q(end__isnull=True)).filter(Q(start__lte=date.today())).order_by("type__name")

        canton_toadd = {"name": canton.name, "score": int(score), "score_before": int(score_7days_before),
                        "date": last_date, "code": canton.code,
                        "cur_prev": last_prev7, "cur_prev14": last_prev14, "tendency": last_tendency,
                        "cur_prev7": case_7days_before.incidence_past7days, "id": canton.swisstopo_id,
                        "level": canton.level, "icon": arrow, "measures": measures}

        canton_vals.append(canton_toadd)

    scores = sorted(canton_vals, key=lambda i: i['cur_prev7'], reverse=False)
    rank = 1
    for score in scores:
        score["rank_old"] = rank
        rank += 1

    scores = sorted(scores, key=lambda i: i['cur_prev'], reverse=False)
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
        'cantons': scores,
    }
    return context


def ranking14_calc(cantons):
    canton_vals = []

    for canton in cantons:
        date_tocheck = date.today()

        cases = CHCases.objects.filter(canton=canton,
                                       date__range=[date_tocheck - timedelta(days=10), date_tocheck]).order_by("-date")

        try:
            if (canton.level == 0 and cases[0].date == date.today()):
                last_date = cases[1].date
                last_prev = cases[1].incidence_past14days
                last_tendency = cases[1].development7to7

                past_date_tocheck = last_date - timedelta(days=14)

                case_14days_before = CHCases.objects.get(canton=canton, date=past_date_tocheck)

                score_14days_before = 0 - case_14days_before.incidence_past14days - (case_14days_before.development7to7 * 2)
                score = 0 - cases[1].incidence_past14days - (last_tendency * 2)
            else:
                last_date = cases[0].date
                last_prev = cases[0].incidence_past14days
                last_tendency = cases[0].development7to7

                past_date_tocheck = last_date - timedelta(days=14)

                case_14days_before = CHCases.objects.get(canton=canton, date=past_date_tocheck)

                score_14days_before = 0 - case_14days_before.incidence_past14days - (
                        case_14days_before.development7to7 * 2)
                score = 0 - cases[0].incidence_past14days - (last_tendency * 2)
        except:
            score = -99999
            score_14days_before = -99999

        if (score > -99999):
            if (score > score_14days_before):
                arrow = "arrow circle up green"
            elif (score == score_14days_before):
                arrow = "arrow circle left orange"
            else:
                arrow = "arrow circle down red"

            measures = CHMeasure.objects.filter(canton=canton).filter(Q(end__gte=date.today()) | Q(end__isnull=True)).filter(Q(start__lte=date.today())).order_by("type__name")

            canton_toadd = {"name": canton.name, "score": int(score), "score_before": int(score_14days_before),
                            "date": last_date, "cur_prev": last_prev, "cur_prev14": case_14days_before.incidence_past14days,
                            "tendency": last_tendency, "icon": arrow, "level": canton.level, "code": canton.code,
                            "id": canton.swisstopo_id, "measures": measures}
            canton_vals.append(canton_toadd)

    scores = sorted(canton_vals, key=lambda i: i['cur_prev14'], reverse=False)
    rank = 1
    for score in scores:
        score["rank_old"] = rank
        rank += 1

    scores = sorted(scores, key=lambda i: i['cur_prev'], reverse=False)
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

    template = loader.get_template('pages/ranking14.html')
    context = {
        'cantons': scores,
    }
    return HttpResponse(template.render(context, request))


def ranking7(request):
    cantons = CHCanton.objects.filter(level=0)
    #    cantons = CHCanton.objects.all()
    context = ranking7_calc(cantons)
    template = loader.get_template('pages/ranking.html')

    return HttpResponse(template.render(context, request))


def ranking7_all(request):
    cantons = CHCanton.objects.all()
    #    cantons = CHCanton.objects.all()
    context = ranking7_calc(cantons)
    template = loader.get_template('pages/ranking.html')

    return HttpResponse(template.render(context, request))
