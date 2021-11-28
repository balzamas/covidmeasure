from measuremeterdata.models.models import Country, MeasureCategory,CasesDeaths
from django.shortcuts import get_object_or_404, render
from datetime import date, timedelta
from django.template import loader
from django.http import HttpResponse
from django.db.models import F, Func

def calc_ranking_countries(countries):
    country_vals = []

    for country in countries:

        #skip Noth Korea, it only makes problems
        if country.pk != 11:
            date_tocheck = date.today()
            print(country)

            cases = CasesDeaths.objects.filter(country=country, date__range=[date_tocheck - timedelta(days=60), date_tocheck]).order_by("-date")

            last_date = cases[0].date
            last_prev14 = cases[0].cases_past14days
            last_deaths14 = cases[0].deaths_past14days
            last_tendency = cases[0].development7to7
            last_positivity = None
            last_positivity_date = None
            last_hosp = None
            last_hosp_date = None
            last_R = None
            last_R_date = None
            last_vaccinated = None
            last_vaccinated_date = None
            positivity_before7 = None
            last_stringency = None
            for case in cases:
                if (case.stringency_index != None and last_stringency == None):
                    last_stringency = case.stringency_index
                    last_stringency_date = case.date

                if (case.r0median != None and last_R == None):
                    last_R = case.r0median
                    last_R_date = case.date

                if (case.positivity != None and last_positivity == None):
                    last_positivity = case.positivity
                    last_positivity_calc = last_positivity
                    last_positivity_date = case.date

                if (case.people_vaccinated_per_hundred != None and last_vaccinated == None):
                    last_vaccinated = case.people_vaccinated_per_hundred
                    last_vaccinated_date = case.date

                if (case.hosp_per_million != None and last_hosp == None):
                    last_hosp = case.hosp_per_million
                    last_hosp_date = case.date

            past_date_tocheck = last_date - timedelta(days=14)

            case_14days_7daysago = CasesDeaths.objects.get(country=country, date=last_date - timedelta(days=7))
            case_14days_14daysago = CasesDeaths.objects.get(country=country, date=past_date_tocheck)


            if (last_positivity == None):
                last_positivity_calc = 5

            if positivity_before7 == None:
                positivity_before7 = 5

            score = float(cases[0].cases_past14days) + float(cases[0].cases_past7days) + (float(cases[0].development7to7) * float(cases[0].cases_past7days) /100) + (float(last_positivity_calc) * float(cases[0].cases_past7days)) + float((cases[0].deaths_past14days * 20))
            score_7days_before = float(case_14days_7daysago.cases_past14days) + float(case_14days_7daysago.cases_past7days) + (float(case_14days_7daysago.development7to7) * float(case_14days_7daysago.cases_past7days) /100) + (float(positivity_before7) * float(case_14days_7daysago.cases_past7days)) + float((case_14days_7daysago.deaths_past14days * 20))

            try:
                score = float(cases[0].cases_past14days) + float(cases[0].cases_past7days) + (float(cases[0].development7to7) * float(cases[0].cases_past7days) /100) + (float(last_positivity_calc) * float(cases[0].cases_past7days)) + float((cases[0].deaths_past14days * 20))
                score_7days_before = float(case_14days_7daysago.cases_past14days) + float(case_14days_7daysago.cases_past7days) + (float(case_14days_7daysago.development7to7) * float(case_14days_7daysago.cases_past7days) /100) + (float(positivity_before7) * float(case_14days_7daysago.cases_past7days)) + float((case_14days_7daysago.deaths_past14days * 20))
            except:
                print(f"{country} failed...")
                score = None

            if (score):
                if (score > score_7days_before):
                    arrow = "arrow circle up red"
                elif (score == score_7days_before):
                    arrow = "arrow circle left orange"
                else:
                    arrow = "arrow circle down green"

                peak_cases_ds = CasesDeaths.objects.filter(country=country).order_by("-cases_past14days")
                peak_cases = peak_cases_ds[0].cases_past14days
                peak_cases_date = peak_cases_ds[0].date

                peak_deaths_ds = CasesDeaths.objects.filter(country=country).order_by("-deaths_past14days")
                peak_deaths = peak_deaths_ds[0].deaths_past14days
                peak_deaths_date = peak_deaths_ds[0].date

                positivity_ds = CasesDeaths.objects.filter(country=country).order_by(F('positivity').desc(nulls_last=True))
                peak_positivity = positivity_ds[0].positivity
                peak_positivity_date = positivity_ds[0].date

                hosp_ds = CasesDeaths.objects.filter(country=country).order_by(F('hosp_per_million').desc(nulls_last=True))
                peak_hosp = hosp_ds[0].hosp_per_million
                peak_hosp_date = hosp_ds[0].date

                canton_toadd = {"name": country.name, "score": int(score), "score_before": int(score_7days_before),
                                "date": last_date, "code": country.code,
                                "cur_prev14": last_prev14, "tendency": last_tendency,
                                "cur_prev7": case_14days_14daysago.cases_past7days,
                                "hosp": last_hosp, "hosp_date": last_hosp_date,
                                "positivity": last_positivity, "positivity_date":last_positivity_date, "deaths": last_deaths14,
                                "has_measures": country.has_measures, "continent": country.continent.pk, "icon": arrow,
                                "peak_cases": peak_cases, "peak_cases_date": peak_cases_date,
                                "peak_deaths": peak_deaths, "peak_deaths_date": peak_deaths_date,
                                "peak_hosp": peak_hosp, "peak_hosp_date": peak_hosp_date,
                                "peak_positivity": peak_positivity, "peak_positivity_date": peak_positivity_date,
                                "R": last_R, "R_date": last_R_date, "stringency": last_stringency, "stringency_date": last_stringency_date,
                                "vaccinated": last_vaccinated, "vaccinated_date": last_vaccinated_date
                                }

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
    countries = Country.objects.filter(isactive=True)
    context = calc_ranking_countries(countries)

    template = loader.get_template('pages/ranking_world.html')
    return HttpResponse(template.render(context, request))



def ranking_europe(request):

    countries = Country.objects.filter(continent=1,isactive=True)
    context = calc_ranking_countries(countries)

    template = loader.get_template('pages/ranking_europe.html')
    return HttpResponse(template.render(context, request))


