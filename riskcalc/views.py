from django.shortcuts import render

# Create your views here.
from riskcalc.models import BELProvince, BELCases, BELAgeGroups
from django.shortcuts import get_object_or_404, render
from datetime import date, timedelta
from django.template import loader
from django.http import HttpResponse
from django.db.models import F, Func

def belgium_risk(request):
    provinces = BELProvince.objects.all()
    date_border = date.today()- timedelta(days=20)
    provinces_vals = []
    print("hansa")


    for province in provinces:
        print(province)
        cases = BELCases.objects.filter(province=province, date__gte=date_border).order_by("-date")


        case_7 = {"0_9":0,"10_19":0,"20_29":0,"30_39":0,"40_49":0,"50_59":0,"60_69":0,"70_79":0,"80_89":0,"90plus":0,"Total":0}
        case_10 = {"0_9":0,"10_19":0,"20_29":0,"30_39":0,"40_49":0,"50_59":0,"60_69":0,"70_79":0,"80_89":0,"90plus":0,"Total":0}
        case_14 = {"0_9":0,"10_19":0,"20_29":0,"30_39":0,"40_49":0,"50_59":0,"60_69":0,"70_79":0,"80_89":0,"90plus":0,"Total":0}
        count = 0
        for case in cases:
            print(".....")
            print(case.date)
            if (count < 7):
                case_7["0_9"] += case.cases0_9
                case_7["10_19"] += case.cases10_19
                case_7["20_29"] += case.cases20_29
                case_7["30_39"] += case.cases30_39
                case_7["40_49"] += case.cases40_49
                case_7["50_59"] += case.cases50_59
                case_7["60_69"] += case.cases60_69
                case_7["70_79"] += case.cases70_79
                case_7["80_89"] += case.cases80_89
                case_7["90plus"] += case.cases90plus
                case_7["Total"] += (case.cases0_9 + case.cases10_19 + case.cases20_29 + case.cases30_39 + case.cases40_49 + case.cases50_59 + case.cases60_69 + case.cases70_79 + case.cases80_89 + case.cases90plus)
            if (count < 10):
                case_10["0_9"] += case.cases0_9
                case_10["10_19"] += case.cases10_19
                case_10["20_29"] += case.cases20_29
                case_10["30_39"] += case.cases30_39
                case_10["40_49"] += case.cases40_49
                case_10["50_59"] += case.cases50_59
                case_10["60_69"] += case.cases60_69
                case_10["70_79"] += case.cases70_79
                case_10["80_89"] += case.cases80_89
                case_10["90plus"] += case.cases90plus
                case_10["Total"] += (case.cases0_9 + case.cases10_19 + case.cases20_29 + case.cases30_39 + case.cases40_49 + case.cases50_59 + case.cases60_69 + case.cases70_79 + case.cases80_89 + case.cases90plus)
            if (count < 14):
                case_14["0_9"] += case.cases0_9
                case_14["10_19"] += case.cases10_19
                case_14["20_29"] += case.cases20_29
                case_14["30_39"] += case.cases30_39
                case_14["40_49"] += case.cases40_49
                case_14["50_59"] += case.cases50_59
                case_14["60_69"] += case.cases60_69
                case_14["70_79"] += case.cases70_79
                case_14["80_89"] += case.cases80_89
                case_14["90plus"] += case.cases90plus
                case_14["Total"] += (case.cases0_9 + case.cases10_19 + case.cases20_29 + case.cases30_39 + case.cases40_49 + case.cases50_59 + case.cases60_69 + case.cases70_79 + case.cases80_89 + case.cases90plus)

            count += 1

        province_toadd = {"name": province.name,
                          "population": province.population,
                          "hasc": province.hasc,
                          "cases7": case_7,
                          "cases10": case_10,
                          "cases14": case_14,
                          }

        provinces_vals.append(province_toadd)

    age_dist = BELAgeGroups.objects.all()

    age_groups_vals = {}
    total = 0
    for ag in age_dist:
        age_groups_vals[ag.name.replace("-", "_")]=ag.population
        total += ag.population

    age_groups_vals["Total"] =total


    context = {
        'provinces': provinces_vals,
        "age_dist": age_groups_vals
    }
    template = loader.get_template('pages/belrisk.html')
    return HttpResponse(template.render(context, request))
