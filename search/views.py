from django.shortcuts import render
from django.http import JsonResponse
from search.models import *


# !Beispiel! für eine Controller Methode, die für open_data gedacht ist.
# übergeben / Ausgelesen wird, vom Template, eine Liste mit 2+ Elementen:
#   1. Element = angefordertes Open-Data, als Keyword. Wird über eine If-Abfrage gecheckt (s.u.)
#   Ab dem 2. Element = Anfragespezifische Werte, die benötigt werden, z.B. Punkt+Distanz o. ein Stadtteil Name
def opendata_von_stadtteil(request):
    column_name = request.POST.get('table_name').lower()
    stadtteil = request.session['polygons'][0]['name']
    # punkt = request.session['polygons'][0]['way']
    #punkt = 'POINT(6.97364225377671 50.9457393529467)'
    print (column_name)
    print (stadtteil)
    '''
    # Landtag benötigt nur ein Stadtteil. werte[1] würde Stadtteil Namen enthalten
    if column_name == 'landtag':
        laermpegel = Landtagswahl.get_parteiverteilung_in_stadtteil(stadtteil)
        return JsonResponse(laermpegel, safe=False)

    # Laempegel benötigt (aktuell noch) einen Punkt & einen Umkreis. Änderung möglich.
    elif column_name == 'pegel':
        umkreis = 100
        laermpegel = Laermpegel.get_learmpegel(punkt, umkreis)
        return JsonResponse(laermpegel, safe=False)

    elif column_name == 'beschaeftigte':
        beschaeftigte = Beschaeftigte.get_arbeitslosenquote(stadtteil)
        return JsonResponse(beschaeftigte, safe=False)

    elif column_name == 'durchschnittsalter':
        durchschnittsalter = Durchschnittsalter.get_durchschnittsalter(stadtteil)
        return JsonResponse(durchschnittsalter, safe=False)

    elif column_name == 'mietpreise':
        mietpreise = DurchschnittlicheMietpreise.get_mietpreise(stadtteil)
        return JsonResponse(mietpreise, safe=False)

    elif column_name == 'lkw_verbot':
        umkreis = 1000
        lkw_verbot = LkwVerbotszonen.get_verbotszone(punkt, umkreis)
        return JsonResponse(lkw_verbot, safe=False)
    '''


def search_cityPolygon(request):
    city = request.POST.get('city')
    #Beispiel für Verwendung & Ausgabe der OpenData
    '''
    punkt_in_koeln = 'POINT(6.97364225377671 50.9457393529467)'
    print("Landtagswahl: \t ",Landtagswahl.get_parteiverteilung_in_stadtteil('Altstadt/Nord'))
    print("Beschäftigte : \t ",Beschaeftigte.get_arbeitslosenquote('Altstadt-Nord'))
    print("Durchschnittsalter: \t ",Durchschnittsalter.get_durchschnittsalter('Altstadt-Nord'))
    print("Mietpreise : \t ",DurchschnittlicheMietpreise.get_mietpreise('Altstadt-Nord'))
    print("LKW Verbotszonen: \t ",LkwVerbotszonen.get_verbotszone(punkt_in_koeln, 5000)[0])
    print("Lärmpegels: \t ",Laermpegel.get_learmpegel(punkt_in_koeln, 3900))

    # Suche nach Polygon mit der osm_id
    #print(PlanetOsmPolygon.get_city_polygon('-62578', True)[0])
    '''
    if city is not None:
        city_polygons = PlanetOsmPolygon.get_city_polygon(city, False)
        # Setzt die Liste der Polygone in der Session zurück, sodass immer nur die letzte Anfrage in der Session ist
        request.session['polygons'] = []
        for elem in city_polygons:
            request.session['polygons'].append({'osm_id': elem['osm_id'],
                                                'name': elem['name'],
                                                'admin_level': elem['admin_level'],
                                                'way': elem['way']})
        request.session.modified = True
        #print(request.session['polygons'][0]['admin_level'])
        print("Polygone in Session ",len(request.session['polygons']))
        return JsonResponse(city_polygons, safe=False)


def index(request):
    # Beim initialen Laden der Seite wird die Session komplett gelöscht
    request.session.flush()
    print("flushed session")
    return render(request, 'search/index.html')


def search_filter(request):
    filter_value = request.POST.get('filter_value')
    filter_name = filter_value.split(':')[0] #Wie kriegt man den Filternamen in die Javascript Funktion?
    print(filter_value, 'filter')
    if filter_value is not None:
        # osm_id wird aus der Session ausgelesen
        osm_id = request.session['polygons'][0]['osm_id']
        circles = PlanetOsmPoint.get_filter_intersection(osm_id, filter_value)
        if circles is not None:
            return JsonResponse(circles, safe=False)
    print('none')
    return render(request, 'search/index.html', {'results': "Suche mit leerem Filterfeld ausgeführt."})


def search_marker(request):
    filter_value = request.POST.get('filter_value')
    if filter_value is not None:
        # osm_id wird aus der Session ausgelesen
        osm_id = request.session['polygons'][0]['osm_id']
        marker = PlanetOsmPoint.get_marker(osm_id, filter_value)
        if marker is not None:
            return JsonResponse(marker, safe=False)
    return render(request, 'search/index.html', {'results': "Suche mit leerem Filterfeld ausgeführt."})
