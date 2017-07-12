from django.shortcuts import render
from django.http import JsonResponse
from search.models import *
import json


# !Beispiel! für eine Controller Methode, die für open_data gedacht ist.
# übergeben / Ausgelesen wird, vom Template, eine Liste mit 2+ Elementen:
#   1. Element = angefordertes Open-Data, als Keyword. Wird über eine If-Abfrage gecheckt (s.u.)
#   Ab dem 2. Element = Anfragespezifische Werte, die benötigt werden, z.B. Punkt+Distanz o. ein Stadtteil Name
def opendata_von_stadtteil(request):
    werte = request.POST.getList('blabla')

    # Landtag benötigt nur ein Stadtteil. werte[1] würde Stadtteil Namen enthalten
    if werte[0] == 'landtag':
        stadtteil = werte[1]
        laermpegel = Landtagswahl.get_parteiverteilung_in_stadtteil(stadtteil)
        return JsonResponse(laermpegel, safe=False)

    # Laempegel benötigt (aktuell noch) einen Punkt & einen Umkreis. Änderung möglich.
    elif werte[0] == 'pegel':
        punkt = werte[1]
        umkreis = werte[2]
        laermpegel = Landtagswahl.get_parteiverteilung_in_stadtteil(punkt, umkreis)
        return JsonResponse(laermpegel, safe=False)


def search_cityPolygon(request):
    city = request.POST.get('city')

    ''' Beispiel für Verwendung & Ausgabe der OpenData
    punkt_in_koeln = 'POINT(6.97364225377671 50.9457393529467)'
    print("Landtagswahl: \t ",Landtagswahl.get_parteiverteilung_in_stadtteil('Altstadt/Nord'))
    print("Beschäftigte : \t ",Beschaeftigte.get_arbeitslosenquote('Altstadt-Nord'))
    print("Durchschnittsalter: \t ",Durchschnittsalter.get_durchschnittsalter('Altstadt-Nord'))
    print("Mietpreise : \t ",DurchschnittlicheMietpreise.get_mietpreise('Altstadt-Nord'))
    print("LKW Verbotszonen: \t ",LkwVerbotszonen.get_verbotszone(punkt_in_koeln, 5000)[0])
    #print("Lärmpegels: \t ",Laermpegel.get_learmpegel(punkt_in_koeln, 3900))'''

    # Suche nach Polygon mit der osm_id
    #print(PlanetOsmPolygon.get_city_polygon('-62578', True)[0])

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
        #print(len(request.session['polygons']))
        return JsonResponse(city_polygons, safe=False)

def index(request):
    # Beim initialen Laden der Seite wird die Session komplett gelöscht
    request.session.flush()
    print("flushed session")
    return render(request, 'search/index.html')

# erhält per POST.get den Inhalt des Suchfeldes.
# Falls Inhalt nicht leer, wird passende Stadt zum Inhalt gesucht & returned.
def search_town(request):
    render_results = {}         # finales dict, in dem alle Key-Value Paare stehen.
    city = request.POST.get('suchanfrage')
    print("\n open data beispiele \n")
    #test_open_data()


    print ("\n\n ----- \n Ausgabe Stadtsuche JSON ")
    if city is not None and len(city) > 1:  # Einfache Überprüfung, ob übermittelter Inhalt des Suchfeldes Inhalt hat.
        city_polygons = PlanetOsmPolygon.get_city_polygon(city, False)
        city_polygon_json_list = []
        if len(city_polygons) >= 1:          # Überprüfung, ob Resulttate leer sind

            for element in city_polygons:    # temporäre Ausgabe der Ergebnisse in der Konsole
                city_name = element.name
                city_admin_level = element.admin_level
                city_geo_json = element.way
                print(city_name)
                print(city_admin_level)
                print(city_geo_json[:50])
                city_polygon_json_list.append(django_object_to_json(element, ('admin_level', 'boundary', 'name', 'way')))

                # Test der Umkreissuche mit defalut-Weten für Restaurants in Köln zwischen 1000 und 3000m Enfernung
                print('--- Polygone für Umkreissuche in ', city_name, '---')
                circles = PlanetOsmPoint.get_osm_points_in_district(element.osm_id)
                polygon_filter = list()
                for polygon in circles:
                    json_dump = json.dumps(
                        json.loads(django_object_to_json(polygon, ('osm_id', 'way', 'amenity', 'leisure', 'highway',
                                                                   'railway', 'aeroway', 'tourism', 'shop', 'name'))))
                    polygon_filter.append(json_dump)

            for filter_j in polygon_filter:
                print(json.dumps(json.loads(filter_j), sort_keys=True, indent=4))

            for city_j in city_polygon_json_list:
                print (json.dumps(json.loads(city_j), sort_keys=True, indent=4))

            with open('JSONData.json', 'w') as f:
                for city_j in city_polygon_json_list:
                    json.dump(json.loads(city_j), f)
            '''
            Gibt Liste aus JSON Objekten zurück. Einträge nach admin-level sortiert
            '''
            render_results['results'] = city_polygons
            return render(request, 'search/index.html', {'results': render_results})

        # Gibt Fehler-String zurück: das Keine Ergebnisse gefunden
        else:
            return render(request, 'search/index.html', {'results': "Keine Ergebnisse gefunden"})

    # Gibt Fehler-String zurück: Inhalt des Suchfeldes leer.
    else:
        return render(request, 'search/index.html', {'results': "Suche mit leerem Suchfeld ausgeführt."})


#Beispiel-Methode für OpenData Anfragen
def test_open_data():
    pkt_in_altstadt = '{"type":"Point","coordinates":[6.95478224980598,50.9420811600325]}'
    stadtteil = "Altstadt-Nord"
    arbeitslosen = Beschaeftigte.get_arbeitslosenquote(stadtteil)
    jugendarbeitslose = Beschaeftigte.get_jugendarbeitslosenquote(stadtteil)
    buildings = PlanetOsmPoint.get_buildings_in_city('hospital', pkt_in_altstadt, 500, 5000)
    miete = DurchschnittlicheMietpreise.get_mietpreise(stadtteil)
    alter = Durchschnittsalter.get_durchschnittsalter(stadtteil)
    #pegel = Laermpegel.get_learmpegel(pkt_in_altstadt, 3500)
    #verbotszone = LkwVerbotszonen.get_verbotszone(pkt_in_altstadt, 3500)

    ls = [miete, alter, buildings, arbeitslosen, jugendarbeitslose]
    for sublist in ls:
        print ("------",str(sublist),"--------")
        for element in sublist[:1]:
            print(json.dumps(json.loads(django_object_to_json(element, ())), sort_keys=True, indent=4))


def search_filter(request):
    filter_value = request.POST.get('filter_value')
    print(filter_value, 'filter')
    if filter_value is not None:
        # osm_id wird aus der Session ausgelesen
        osm_id = request.session['polygons'][0]['osm_id']
        circles = PlanetOsmPoint.get_filter_intersection(osm_id, filter_value)
        if circles is not None:
            return JsonResponse(circles, safe=False)
    print('none')
    return JsonResponse([], safe=False)
