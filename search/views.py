from django.shortcuts import render
from search.models import PlanetOsmPolygon, PlanetOsmPoint


# erhält per POST.get den Inhalt des Suchfeldes.
# Falls Inhalt nicht leer, wird passende Stadt zum Inhalt gesucht & returned.
def search_town(request):
    city = request.POST.get('suchanfrage')

    if city is not None and len(city) > 1:  # Einfache Überprüfung, ob übermittelter Inhalt des Suchfeldes Inhalt hat.
        # checkboxen = request.POST.getlist('checks[]')
        city_polygons = PlanetOsmPolygon.get_city_polygon(city)

        if len(city_polygons) >= 1:     # Überprüfung, ob Resulttate leer sind
            for element in city_polygons:    # temporäre Ausgabe der Ergebnisse in der Konsole
                city_name = element[0]
                city_geo_json = element[1]
                print (city_name)
                print (city_geo_json[0:50])
            # return render(request,  'search/easy_living.html')

            '''
            Gibt Liste aus Tuplen zurück. 
            Erstes Tuple Element = Stadtname, zweites Tuple Element. Polygon Koordinaten als geoJSON
            '''
            return render(request, 'search/index.html', {'results': city_polygons})

        # Lädt Seite ohne Inhalt neu.
        # @Todo: Ausgabe eines Fehler-Strings, dass nichts gefunden werden konnte.
        else:
            return render(request, 'search/index.html')

    # Keine Ausführung, da Inhalt des Suchfeldes leer
    else:
        return render(request, 'search/index.html')


