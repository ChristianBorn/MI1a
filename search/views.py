from django.shortcuts import render
from search.models import PlanetOsmPolygon, PlanetOsmPoint


# erhält per POST.get den Inhalt des Suchfeldes.
# Falls Inhalt nicht leer, wird passende Stadt zum Inhalt gesucht & returned.
def search_town(request):
    city = request.POST.get('suchanfrage')

    if city is not None and len(city) > 1:  # Einfache Überprüfung, ob übermittelter Inhalt des Suchfeldes Inhalt hat.
        # checkboxen = request.POST.getlist('checks[]')
        city_polygons = PlanetOsmPolygon.get_city_polygon(city)

        if len(city_polygons) >= 1:          # Überprüfung, ob Resulttate leer sind
            for element in city_polygons:    # temporäre Ausgabe der Ergebnisse in der Konsole
                city_name = element[0]
                city_admin_level = element[1]
                city_geo_json = element[2]
                print(city_name)
                print(city_admin_lmi1asose2017evel)
                print(city_geo_json[0:50])

            '''
            Gibt Liste aus Tuplen zurück. Einträge nach admin-level sortiert
            Erstes Tuple Element = Stadtname, 
            Zweites Tuple Element = admin_level
            Zweites Tuple Element. geoJSON Polygon-Koordinaten des Elements
            '''
            return render(request, 'search/index.html', {'results': city_polygons})

        # Gibt Fehler-String zurück: das Keine Ergebnisse gefunden
        else:
            return render(request, 'search/index.html', {'results': "Keine Ergebnisse gefunden"})

    # Gibt Fehler-String zurück: Inhalt des Suchfeldes leer.
    else:
        return render(request, 'search/index.html', {'results': "Suche mit leerem Suchfeld ausgeführt."})


