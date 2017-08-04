from django.shortcuts import render
from django.http import JsonResponse
from search.models import *


# !Beispiel! für eine Controller Methode, die für open_data gedacht ist.
# übergeben / Ausgelesen wird, vom Template, eine Liste mit 2+ Elementen:
#   1. Element = angefordertes Open-Data, als Keyword. Wird über eine If-Abfrage gecheckt (s.u.)
#   Ab dem 2. Element = Anfragespezifische Werte, die benötigt werden, z.B. Punkt+Distanz o. ein Stadtteil Name
def opendata_von_stadtteil(request):
    column_name = request.POST.get('table_name').lower()
    stadtteile = request.session['polygons']
    #punkt = request.session['polygons'][0]['way']
    #punkt = 'POINT(6.97364225377671 50.9457393529467)'
    #print(column_name)
    #print(stadtteile)

    if column_name == 'lkw_verbot':
        lkw_verbot = LkwVerbotszonen.get_verbotszone()
        return JsonResponse(lkw_verbot, safe=False)

    # Laempegel benötigt (aktuell noch) einen Punkt & einen Umkreis. Änderung möglich.
    elif column_name == 'pegel':
        #laermpegel = Laermpegel.get_learmpegel()
        laermpegel = []
        #print('views',len(laermpegel))
        return JsonResponse(laermpegel, safe=False)

    # alle anderen OpenData zusammen berechnen, da gemeinsam als Tooltip angezeigt werden
    else:
        for polygon_nr, polygon in enumerate(stadtteile):
            if polygon['admin_level'] == 10 and polygon['open_data']=='undefined':
                beschaeftigte = Beschaeftigte.get_arbeitslosenquote(polygon['name'])
                durchschnittsalter = Durchschnittsalter.get_durchschnittsalter(polygon['name'])
                mietpreise = DurchschnittlicheMietpreise.get_mietpreise(polygon['name'])
                landtag = Landtagswahl.get_parteiverteilung_in_stadtteil(polygon['name'])
                if landtag and beschaeftigte and durchschnittsalter and mietpreise:
                    open_data_dict = {'wahl': landtag, 'beschaeftigte': beschaeftigte,
                                      'durchschnittsalter': durchschnittsalter,
                                      'mietpreis': mietpreise}
                    request.session['polygons'][polygon_nr]['open_data'] = open_data_dict
        request.session.modified = True
        #print(len(request.session['polygons']))
        return JsonResponse(request.session['polygons'], safe=False)


def search_cityPolygon(request):
    city = request.POST.get('city')
    osmId = request.POST.get('osmId')
    if osmId == 'true':
        osmId = True
    else:
        osmId = False

    if city is not None:
        city_polygons = PlanetOsmPolygon.get_city_polygon(city, osmId)
        # Setzt die Liste der Polygone in der Session zurück, sodass immer nur die letzte Anfrage in der Session ist
        request.session['polygons'] = []
        for elem_nr, elem in enumerate(city_polygons):
            request.session['polygons'].append({'osm_id': elem['osm_id'],
                                                'name': elem['name'],
                                                'admin_level': elem['admin_level'],
                                                'way': elem['way'], 'filter': {}, 'open_data': 'undefined',
                                               'parent_osm': elem['parent_osm'], 'parent_name': elem['parent_name'],
                                                'affil_city_name': elem['affil_city_name']})
        request.session.modified = True
        print("Polygone in Session ",len(request.session['polygons']))
        return JsonResponse(city_polygons, safe=False)
    return JsonResponse([], safe=False)


def index(request):
    # Beim initialen Laden der Seite wird die Session komplett gelöscht
    request.session.flush()
    print("flushed session")
    return render(request, 'search/index.html')

def about(request):
    return render(request, 'search/about.html')

def search_filter(request):
    filter_value = request.POST.get('filter_value')
    print(filter_value, 'filter')
    if filter_value is not None:
        # osm_id wird aus der Session ausgelesen
        osm_id = request.session['polygons'][0]['osm_id']
        session_filter_dict = request.session['polygons'][0]['filter']
        intersections = PlanetOsmPoint.get_filter_intersection(osm_id, filter_value, session_filter_dict)
        if intersections:
            request.session['polygons'][0]['filter'] = intersections[1]
            request.session.modified = True
            return JsonResponse(intersections[0], safe=False)
    return JsonResponse([], safe=False)


def search_marker(request):
    filter_value = request.POST.get('filter_value')
    if filter_value is not None:
        # osm_id wird aus der Session ausgelesen
        osm_id = request.session['polygons'][0]['osm_id']
        session_filter_dict = request.session['polygons'][0]['filter']
        marker = PlanetOsmPoint.get_marker(osm_id, filter_value, session_filter_dict)
        if marker:
            request.session['polygons'][0]['filter'] = marker[1]
            request.session.modified = True
            return JsonResponse(marker[0], safe=False)
    return JsonResponse([], safe=False)
