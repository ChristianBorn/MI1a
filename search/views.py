from django.shortcuts import render
from search.models import *
import json


# erhält per POST.get den Inhalt des Suchfeldes.
# Falls Inhalt nicht leer, wird passende Stadt zum Inhalt gesucht & returned.
def search_town(request):
    render_results = {}         # finales dict, in dem alle Key-Value Paare stehen.
    city = request.POST.get('suchanfrage')
    print("\n open data beispiele \n")
    test_open_data()
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
                city_polygon_json_list.append(django_object_to_json(element))

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
            print(json.dumps(json.loads(django_object_to_json(element)), sort_keys=True, indent=4))
