from bs4 import element
from django.shortcuts import render
from django.http import JsonResponse
from search.models import *
import json



def search_cityPolygon(request):
    city = request.POST.get('city')
    data = []
    if city is not None:
        city_polygons = PlanetOsmPolygon.get_city_polygon(city, False)
        if len(city_polygons) >= 1:
           for element in city_polygons:
                data.append({'name': element.name, 'admin_level': element.admin_level, 'way': element.way})
    return JsonResponse(data, safe=False)



# erhält per POST.get den Inhalt des Suchfeldes.
# Falls Inhalt nicht leer, wird passende Stadt zum Inhalt gesucht & returned.
def search_town(request):
    render_results = {}         # finales dict, in dem alle Key-Value Paare stehen.
    city = request.POST.get('suchanfrage')
    print("\n open data beispiele \n")
    #test_open_data()

    if request.POST.get('submitfilter'):
        print(get_polygons_for_filter(request))

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


def get_polygons_for_filter(request):
    print('--- Polygone für Umkreissuche in Köln (default Stadt) ---')
    render_results = dict()
    if request.POST.get('submitfilter'):
        polygon_filter = list()
        filter_lines = request.POST.get('submitfilter').split('\n')
        for filter_row in filter_lines:
            filter_data = filter_row.split(':')
            type_filter = filter_data[0]
            radius = filter_data[1].split(',')
            inner_radius = int(radius[0])
            outer_radius = int(radius[1])
            circles = PlanetOsmPoint.get_osm_points_in_district(type_filter=type_filter, inner_radius=inner_radius,
                                                                outer_radius=outer_radius) #default-Werte in models angegeben
            for polygon in circles:
                json_dump = json.dumps(json.loads(django_object_to_json(polygon, ('osm_id', 'name', 'way', 'amenity', 'leisure', 'highway',
                                                                                  'railway', 'aeroway', 'tourism', 'shop'))))
                print(json_dump)
                polygon_filter.append(json_dump)

        for filter_j in polygon_filter:
            print(json.dumps(json.loads(filter_j), sort_keys=True, indent=4))

        render_results['filter'] = circles
        return render(request, 'search/index.html', {'filter': render_results})

    else:
        return render(request, 'search/index.html', {'filter': "Suche mit leeren Filtern ausgeführt."})