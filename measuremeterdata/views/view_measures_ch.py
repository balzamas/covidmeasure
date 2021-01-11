from measuremeterdata.models.models_ch import CHCanton, CHCases, CHMeasure, CHMeasureType
from django.template import loader
from django.http import HttpResponse
from datetime import date, timedelta



def measures_ch(request):
    measures = CHMeasure.objects.all().order_by('canton', 'start')
    #measures = CHMeasure.objects.filter(canton__pk=37).order_by('canton', 'start')

    measures_analytics = []

    for measure in measures:
        if measure.start != measure.end:
            canton = measure.canton.name
            type = measure.type.name
            start = measure.start
            end = measure.end
            level = measure.level

            tend_start_before = None
            tend_start_during = None
            tend_start_after = None
            tend_start_after2 = None
            r_start_before = None
            r_start_during = None
            r_start_after = None
            r_start_after2 = None

            tend_end_before = None
            tend_end_during = None
            tend_end_after = None
            r_end_before = None
            r_end_during = None
            r_end_after = None

            if measure.start:
                print(canton)
                print(start)
                if measure.canton.level == 0:
                    try:
                        during_start_date = start - timedelta(days=7)
                        during_end_date = start + timedelta(days=7)
                        tend_start_during = CHCases.objects.get(canton=measure.canton, date=during_end_date).development7to7 - CHCases.objects.get(canton=measure.canton, date=during_start_date).development7to7

                        r_start_during = CHCases.objects.get(canton=measure.canton, date=start).r0median

                    except:
                        pass

                    before_start_date = start - timedelta(days=21)
                    before_end_date = start - timedelta(days=7)
                    tend_start_before = CHCases.objects.get(canton=measure.canton, date=before_end_date).development7to7 - CHCases.objects.get(canton=measure.canton, date=before_start_date).development7to7
                    r_start_before = CHCases.objects.get(canton=measure.canton, date=before_end_date).r0median

                    try:
                        after_start_date = start + timedelta(days=7)
                        after_end_date = start + timedelta(days=21)
                        tend_start_after = CHCases.objects.get(canton=measure.canton, date=after_end_date).development7to7 - CHCases.objects.get(canton=measure.canton, date=after_start_date).development7to7
                        r_start_after = CHCases.objects.get(canton=measure.canton, date=after_start_date).r0median
                    except:
                        pass

                    try:
                        after2_start_date = start + timedelta(days=21)
                        after2_end_date = start + timedelta(days=35)
                        tend_start_after2 = CHCases.objects.get(canton=measure.canton, date=after2_end_date).development7to7 - CHCases.objects.get(canton=measure.canton, date=after2_start_date).development7to7
                        r_start_after2 = CHCases.objects.get(canton=measure.canton, date=start + timedelta(days=14)).r0median
                    except:
                        pass

                    measure_record = {'canton': canton, 'type': type, 'start': start, 'end':end, 'level':level,'tend_start_before':tend_start_before,
                                      'tend_start_during':tend_start_during, 'tend_start_after': tend_start_after, 'tend_start_after2': tend_start_after2,
                                      'r_start_during':r_start_during, 'r_start_before':r_start_before, 'r_start_after':r_start_after, 'r_start_after2':r_start_after2}
                    measures_analytics.append(measure_record)
                    print(f"{canton};{type};{start};{end};{level};{tend_start_before};{tend_start_during};{tend_start_after}")


    template = loader.get_template('pages/measures_ch.html')

    context = {
        'measures': measures_analytics,
    }

    return HttpResponse(template.render(context, request))
