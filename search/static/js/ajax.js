var map;
var markerClusters;
var intersectLayer;
var csrftoken;
$(document).ready(
    function init_map() {
        csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        var tiles = L.tileLayer(
            //local
            '/static/leaflet/tiles/{z}/{x}/{y}.png',
            {
            minZoom: 9,
            maxZoom: 16
            }

            /*//old via mapbox
            'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}',
            {
            attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
            maxZoom: 18,
            //id: 'mapbox.mapbox-streets-v7',
            //id: 'mapbox.mapbox-terrain-v2',
            //id: 'mapbox.mapbox-traffic-v1',
            id: 'mapbox.satellite',
            accessToken: 'pk.eyJ1IjoicnN0b2RkZW4iLCJhIjoiY2ozdmt0ZDN3MDAydDR1cG1ybXduYjFsZiJ9.1SgNsXjR5DBwU6uEWTZF1A'
            }*/
        );

        /*var lkw_verbot_layer = L.layerGroup(getOpenData('lkw_verbot'));
        var pegel_layer = L.layerGroup(getOpenData('pegel'));
        var open_data_layer = L.layerGroup([L.marker([50.938, 6.95]), L.marker([50.939, 6.96])]);*/
        map = L.map('mapid',
            {center: [50.938, 6.95], zoom: 12});

        /*var overlayMaps = {
            'OpenData': open_data_layer,
            'LKW': lkw_verbot_layer,
            'Pegel': pegel_layer
        };

        //Button zum Ein- und Ausschalten der Opendata außerhalb der Karte anzeigen
        var layerControl = L.control.layers(null, overlayMaps, {collapsed: false});
        layerControl.addTo(map);
        layerControl._container.remove();
        document.getElementById('divMapInfo').appendChild(layerControl.onAdd(map));*/

        //tiles zur map hinzufügen
        tiles.addTo(map);

        // globales definieren von layern damit diese funktionsübergreifend gelöscht werden können
        markerClusters = L.markerClusterGroup();
        intersectLayer = L.layerGroup();

        //Maßstab zur map hinzufügen
        L.control.scale().addTo(map);

        //Speicherbutton auf Karte hinzufügen
        var printer = L.easyPrint({
      		tileLayer: tiles,
      		sizeModes: ['A4Landscape', 'A4Portrait'],
      		filename: 'Easy_Living_Map',
      		exportOnly: true,
      		hideControlContainer: true
		}).addTo(map);

    return map;}
);
/**
 * @global map
 */
function jsUcfirst(string)
{
    return string.charAt(0).toUpperCase() + string.slice(1);
}
function getColor(x) {
    var color = "";

    if (x == "bus_stop" || x == "bus_station" || x == "subway_entrance" || x == "tram_stop" || x == "terminal"){ color = "purple"; }
    else if (x == "park" || x == "recreation_ground" || x == "dog_park" || x == "playground"){ color = "green"; }
    else if (x == "fitness_centre" || x == "cinema" || x == "theatre" || x == "nightclub" || x == "restaurant"){ color = "cadetblue"; }
    else if (x == "kindergarten" || x == "school" || x == "college" || x == "university") { color = "darkred"; }
    else if (x == "doctors" || x == "clinic" || x == "dentist" || x == "hospital" || x == "social_facility" || x == "nursing_home" || x == "veterinary"){ color = "blue"; }
    else if (x == "supermarket" || x == "chemist" || x == "pharmacy" || x == "mall") { color = "darkgreen"; }
    else if (x == "place_of_worship") { color = "darkpurple";}
    else if (x == "atm" || x == "bank") { color = "orange";}
    else if (x == "station") { color = "purple";}
    else {color = "darkred";}

    return color;
}
function alphanum(a, b) {
  a = String(a).slice(94,-4);
  b = String(b).slice(94,-4);
  function chunkify(t) {
    var tz = [], x = 0, y = -1, n = 0, i, j;

    while (i = (j = t.charAt(x++)).charCodeAt(0)) {
      var m = (i == 46 || (i >=48 && i <= 57));
      if (m !== n) {
        tz[++y] = "";
        n = m;
      }
      tz[y] += j;
    }
    return tz;
  }

  var aa = chunkify(a);
  var bb = chunkify(b);

  for (x = 0; aa[x] && bb[x]; x++) {
    if (aa[x] !== bb[x]) {
      var c = Number(aa[x]), d = Number(bb[x]);
      if (c == aa[x] && d == bb[x]) {
        return c - d;
      } else return (aa[x] > bb[x]) ? 1 : -1;
    }
  }
  return aa.length - bb.length;
}
function deselect () {
    $('.selected').addClass('deselected');
    $('.selected').removeClass('selected');
}
function clearMap(m) {
    for(i in m._layers) {
        if(m._layers[i]._path != undefined || m._layers[i]._icon != undefined) {
            try {
                //m._layers[i].clearLayers();
                m.removeLayer(m._layers[i]);
            }
            catch(e) {
                console.log("problem with " + e + m._layers[i]);
            }
        }
    }
}
function clearFilters(m) {
    for(i in m._layers) {
        if(m._layers[i].options.className != undefined) {
            if(m._layers[i].options.className.startsWith('intersection')) {
                m.removeLayer(m._layers[i]);
            }
        }
        else if(m._layers[i]._icon != undefined || m._layers[i].options.iconCreateFunction != undefined) {
            try {
                m.removeLayer(m._layers[i]);
            }
            catch(e) {
                console.log("problem with " + e + m._layers[i]);
            }
        }
    }
}
$(function() {
    $('#transparent').change(function() {
      if ($('.transparent').length == 0) {
        $('.leaflet-interactive').addClass('transparent');
      }
      else {
        $('.transparent').removeClass('transparent');
      }
      console.log($('.transparent').length);
      
    })
  })
function setTransparency() {
    console.log($('.transparent').length);
    $('.leaflet-interactive').addClass('transparent');
}
function getCityPoly (cityName, osmId=false ) {
    $.ajax(
        './search/cityPolygon',
        {
            cache: false,
            dataType: "json",
            data: {
                csrfmiddlewaretoken: csrftoken,
                city: cityName,
                osmId: osmId
            },
            method: 'POST',
            success: function (data, textStatus, jqXHR) {
                // wenn vorhanden dann alte elemente löschen, damit nicht mehrfach entstehen
                if (typeof layerControl !== 'undefined') {
                    layerControl._container.remove();
                }

                //Berechnen der Werte der Ein-und Auszublendenden OpenData
                lkw_verbot_layer = L.layerGroup(getOpenData('lkw_verbot'));
                //pegel_layer = L.layerGroup(getOpenData('pegel'));
                open_data_layer = L.layerGroup(getOpenData('opendata'));

                var overlayMaps = {
                    'OpenData': open_data_layer,
                    'LKW': lkw_verbot_layer,
                    //'Pegel': pegel_layer
                };

                //Button zum Ein- und Ausschalten der Opendata außerhalb der Karte anzeigen
                layerControl = L.control.layers(null, overlayMaps, {collapsed: false});
                layerControl.addTo(map);
                //layerControl._container.remove();
                //document.getElementById('divMapInfo').appendChild(layerControl.onAdd(map));

                // hierarchische Suche ohne Erfolg
                
                $('#stadtauswahl').text('');
                if (data.length == 0) {
                    swal("Suche erfolglos", "Die Suche war nicht erfolgreich. Bitte die Schreibweise im Suchfeld überprüfen.", "error");
                    return;
                }
                // Wenn nur ein Ergebnis in Ergebnismenge
                if (data.length == 1) {
                $('#stadtauswahl').html('<a href="javascript:void(0)" class="list-group-item list-group-item-action" style="pointer-events: none;">Keine Stadtteile unter aktuellem Ergebnis</a>');
                }
                var sortList = []
                // erfolgreiche Suche im Suchfeld
                changeAuswahlName(data[0].name);
                deselect();
                //löschen der alten Filter
                // @todo: löschen aller Filter bei anderen Stadtteilen/Städten
                if (map.hasLayer(markerClusters)) {
                    markerClusters.clearLayers();
                    map.removeLayer(markerClusters);
                }
                if (map.hasLayer(intersectLayer)) {
                    intersectLayer.clearLayers();
                    map.removeLayer(intersectLayer);
                }
                // Check, ob der Transparenz-Button Aktiv ist
                var transparencyActive = false;
                if ($('.transparent').length > 0){
                    console.log('transparent');
                    transparencyActive = true;
                }
                console.log(transparencyActive);
                for (i = 0; i < data.length; i++) {
                    if (i != 0) {
                        sortList.push('<a href="javascript:void(0)" class="list-group-item list-group-item-action" onclick="getCityPoly(' + data[i].osm_id + ',true)">' + data[i].name + '</a>');
                    }
                    var latlngs = data[i].way;
                    var polygon = L.polygon(latlngs, {color: 'red', className: 'cityPoly selected'});
                    // Falls der Transparenz-Button aktiv ist, wird den neuen Polygonen die Transparenz-Klasse mitgegeben
                    if (transparencyActive == true) {
                        polygon.setStyle({className: 'cityPoly selected transparent'});
                    }
                    var tooltip = L.tooltip({
                        sticky: true,
                        direction: 'top'
                    })
                        .setContent(jsUcfirst(data[i].name));
                    polygon.bindTooltip(tooltip);
                    polygon.on('click', function () {
                            map.fitBounds(this.getBounds());
                            });
                    polygon.addTo(map);

                    //reinzoomen bei ersten Element (mit höchstem admin_level)
                    if (i == 0) {
                        map.fitBounds(polygon.getBounds());
                    }
                }

            // erfolgreiche hierarchische Suche und befüllen des DropDownMenüs
            //changeAuswahlName();
            showAuswahl();
            showOpenData();
            sortList.sort(alphanum);
            $('#stadtauswahl').append(sortList.join(''));
            $('html, body').animate({
                scrollTop:$('#mapid').offset().top*0.7
                },'slow');

            },
            error: function (jqXHR, textStatus, errorThrown) {
                swal("Error", "Error: " + errorThrown + "\nStatus: " + textStatus + "\njqXHR: " + JSON.stringify(jqXHR), "error")
                /*alert("Error: " + errorThrown
                    + "\nStatus: " + textStatus
                    + "\njqXHR: " + JSON.stringify(jqXHR)
                );*/
            },
            complete: function (jqXHR, textStatus) {}
        }
    );
}

function getCityFilterMarker  (filter, intersection=false) {
    $.ajax(
        './search/cityFilterMarker',
        {
            cache: false,
            dataType: "json",
            data: {
                csrfmiddlewaretoken: csrftoken,
                filter_value: filter
            },
            method: 'POST',
            success: function (data, textStatus, jqXHR) {
                console.log(data.length);
                //console.log(typeof data);
                if (typeof data === 'string') {
                    swal("Suche erfolglos", "Es wurde kein "+getAmenity(data)+" in dem ausgewählten Bereich gefunden. Bitte "+getAmenity(data)+" aus den Filtern entfernen.", "error")
                    //alert("Es wurde kein(e) "+getAmenity(data)+" in dem ausgewählten Bereich gefunden. Bitte "+getAmenity(data)+" aus den Filtern entfernen.");
                }
                else if (data.length === 0) {
                    swal("Suche erfolglos", "Es wurde kein Filter in dem ausgewählten Bereich gefunden.", "error")
                    //alert("Es wurde kein Filter in dem ausgewählten Bereich gefunden.")
                }
                else {
                    // löschen der alten Filter
                    //clearFilters(map);
                    if (map.hasLayer(markerClusters)) {
                        markerClusters.clearLayers();
                        map.removeLayer(markerClusters);
                    }
                    // intersections an dieser Stelle löschen nur wenn false, da sonst durch ansynchronen Aufruf
                    // zum falschen Zeitpunkt gelöscht wird
                    if (intersection == false) {
                        if (map.hasLayer(intersectLayer)) {
                            intersectLayer.clearLayers();
                            map.removeLayer(intersectLayer);
                        }
                    }

                    //var markerClusters = L.markerClusterGroup({ chunkedLoading: false });
                    for (i = 0; i < data.length; i++) {
                        var latlngs = data[i].way;
                        var markerStyle = L.AwesomeMarkers.icon({icon: getCityFilterMarkerIcon(data[i].amenity), markerColor: getCityFilterMarkerColor(data[i].amenity), prefix:'fa'});
                        var marker = L.marker(latlngs, {icon: markerStyle, className: 'marker'});
                        var amenity = getAmenity(data[i].amenity);
                        var name = data[i].name;
                        var marker_text = "";

                        if (name != null) {
                            marker_text = "Name: "+name+"; Art: "+amenity;
                        }
                        else {
                            marker_text = "Art: "+amenity;
                        }

                        marker.bindPopup(marker_text);
                        marker.on('mouseover', function (e) {
                            this.openPopup();
                        });
                        marker.on('mouseout', function (e) {
                            this.closePopup();
                        });
                        markerClusters.addLayer( marker );
                    }
                    map.addLayer( markerClusters );
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                swal("Error", "Error: " + errorThrown + "\nStatus: " + textStatus + "\njqXHR: " + JSON.stringify(jqXHR), "error")
                /*alert("Error: " + errorThrown
                    + "\nStatus: " + textStatus
                    + "\njqXHR: " + JSON.stringify(jqXHR)
                );*/
            },
            complete: function (jqXHR, textStatus) {}
        }
    );
}


function getCityFilter  (filter) {
    $.ajax(
        './search/cityFilterIntersects',
        {
            cache: false,
            dataType: "json",
            data: {
                csrfmiddlewaretoken: csrftoken,
                filter_value: filter
            },
            method: 'POST',
            success: function (data, textStatus, jqXHR) {
                console.log(data.length);
                if (typeof data === 'string') {
                    swal("Suche erfolglos", "Es wurde kein(e) "+getAmenity(data)+" in dem ausgewählten Bereich gefunden. Bitte "+getAmenity(data)+" aus den Filtern entfernen.", "error");
                    //alert("Es wurde kein(e) "+getAmenity(data)+" in dem ausgewählten Bereich gefunden. Bitte "+getAmenity(data)+" aus den Filtern entfernen.");
                }
                else if (data.length == 0) {
                    swal("Suche erfolglos", "Es wurde keine passende Fläche gefunden, die Filter überschneiden sich nicht. Bitte die Entfernungen ändern oder andere Filter wählen", "error")
                    //alert("Es wurde keine passende Fläche gefunden, die Filter überschneiden sich nicht. Bitte die Entfernungen ändern oder andere Filter wählen");
                }
                else {
                    deselect();

                    //löschen der alten Schnittmengen. Einzeln aufgerufen da sonst falscher Zeitpunkt des Löschens
                    // aufgrund asynchronen Aufrufs
                    //clearFilters(map);
                    if (map.hasLayer(intersectLayer)) {
                        intersectLayer.clearLayers();
                        map.removeLayer(intersectLayer);
                    }

                    getCityFilterMarker(filter, true);
                    for (i = 0; i < data.length; i++) {
                        var latlngs = data[i].way;
                        var polygon = L.polygon(latlngs, {color: getColor(getFilter()), className: 'intersection selected'});//.addTo(map);//.bringToBack();
                        polygon.addTo(intersectLayer).bringToBack();
                    }
                    map.addLayer(intersectLayer);
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                swal("Error", "Error: " + errorThrown + "\nStatus: " + textStatus + "\njqXHR: " + JSON.stringify(jqXHR), "error")
                /*alert("Error: " + errorThrown
                    + "\nStatus: " + textStatus
                    + "\njqXHR: " + JSON.stringify(jqXHR)
                );*/
            },
            complete: function (jqXHR, textStatus) {}
        }
    );
}


function getOpenData  (type_data) {
    $.ajax(
        './search/OpenData',
        {
            cache: false,
            dataType: "json",
            data: {
                csrfmiddlewaretoken: csrftoken,
                table_name: type_data
            },
            method: 'POST',
            success: function (data, textStatus, jqXHR) {
                if (type_data === 'lkw_verbot') {
                    lkw_verbot_layer.clearLayers();
                    console.log('Zeichne Polygone für LKW-Verbot:', data.length);
                    for (i = 0; i < data.length; i++) {
                        var latlngs = data[i].rings;
                        var polygon = L.polygon(latlngs, {color: 'black'});
                        var tooltip = L.tooltip({
                            sticky: true,
                            direction: 'top'
                        }).setContent(jsUcfirst("LKW-Verbotszone"));
                        polygon.bindTooltip(tooltip);
                        //var popup = L.popup({closeOnClick: true, className: 'map-popup'});
                        //polygon.bindPopup(popup);
                        polygon.addTo(lkw_verbot_layer);
                    }
                }
                else if (type_data === 'pegel') {
                    pegel_layer.clearLayers();
                    console.log('Zeichne Polygone für Lärmpegel:', data.length);
                    for (i = 0; i < data.length; i++) {
                        var latlngs = data[i].rings;
                        if (data.dezibel === '55') {
                            var color = '#99c4d8';
                        }
                        else if (data.dezibel === '70') {
                            var color = '#0047ab';
                        }
                        else {
                            var color = '#093253';
                        }

                        var polygon = L.polygon(latlngs, {color: color});
                        var tooltip = L.tooltip({
                            sticky: true,
                            direction: 'top'
                        }).setContent(jsUcfirst("Lärmpegel: " + data[i].dezibel));
                        polygon.bindTooltip(tooltip);
                        var popup = L.popup({closeOnClick: true, className: 'map-popup'});
                        polygon.bindPopup(popup);
                        polygon.addTo(pegel_layer);
                    }
                }

                else {
                    open_data_layer.clearLayers();
                    for (i = 0; i < data.length; i++) {
                        var latlngs = data[i].way;
                        var polygon = L.polygon(latlngs, {className: 'deselected'});
                        var tooltip = L.tooltip({sticky: true, direction: 'top'}).setContent(jsUcfirst(data[i].name));
                        polygon.bindTooltip(tooltip);

                        if (data[i].admin_level == '10' && data[i].open_data != 'undefined') {
                            //console.log(data[i].open_data);
                            if (data[i].open_data.mietpreis[0]['mietpreis'] != 'unbekannt') {
                                var miete = data[i].open_data.mietpreis[0]['mietpreis'] + ' €'
                            }
                            else {
                                var miete = data[i].open_data.mietpreis[0]['mietpreis']
                            }
                            var tooltip_text = 'Stadtteil: ' + data[i].name + '</br>Jugendarbeitslosenquote: ' + data[i].open_data.beschaeftigte[0]['jugendarbeitslosenquote'] + ' %' + '</br>Arbeitslosenquote: ' + data[i].open_data.beschaeftigte[0]['arbeitslosenquote'] + ' %' + '</br>Durchschnittsmietpreis: ' + miete + '</br>Durchschnittsalter: ' + data[i].open_data.durchschnittsalter[0]['durchschnittsalter'] + ' Jahre' + '</br>Landtagswahlergebnis: ' + '</br>-SPD: ' + data[i].open_data.wahl[0]['gesamt_spd'] + ' %' + '</br>-CDU: ' + data[i].open_data.wahl[0]['gesamt_cdu'] + ' %' + '</br>-Grüne: ' + data[i].open_data.wahl[0]['gesamt_gruene'] + ' %' + '</br>-FDP: ' + data[i].open_data.wahl[0]['gesamt_fdp'] + ' %' + '</br>-Die Linke: ' + data[i].open_data.wahl[0]['gesamt_die_linke'] + ' %' + '</br>-AfD: ' + data[i].open_data.wahl[0]['gesamt_afd'] + ' %' + '</br>-NPD: ' + data[i].open_data.wahl[0]['gesamt_npd'] + ' %' + '</br>-Piraten: ' + data[i].open_data.wahl[0]['gesamt_piraten'] + ' %';
                            var popup = L.popup({
                                closeOnClick: true,
                                className: 'map-popup'
                            }).setContent(tooltip_text);
                            polygon.bindPopup(popup);
                        }
                        else {
                            var tooltip_text = 'Für dieses Polygon sind keine OpenData verfügbar.';
                            var popup = L.popup({
                                closeOnClick: true,
                                className: 'map-popup'
                            }).setContent(tooltip_text);
                            polygon.bindPopup(popup);
                        }
                        polygon.addTo(open_data_layer);
                    }
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                swal("Error", "Error: " + errorThrown + "\nStatus: " + textStatus + "\njqXHR: " + JSON.stringify(jqXHR), "error")
                /*alert("Error: " + errorThrown
                    + "\nStatus: " + textStatus
                    + "\njqXHR: " + JSON.stringify(jqXHR)
                );*/
            },
            complete: function (jqXHR, textStatus) {}
        }
    );
}

function getAmenity (x) {
    var amenity = "";

    if (x == "bus_stop"){ amenity = "Bushaltestelle"; }
    else if (x == "bus_station"){ amenity = "Busbahnhof"; }
    else if (x == "station"){ amenity = "Bahnhof"; }
    else if (x == "subway_entrance"){ amenity = "U-Bahn"; }
    else if (x == "tram_stop"){ amenity = "Straßenbahn"; }
    else if (x == "terminal"){ amenity = "Flughafen"; }
    else if (x == "park"){ amenity = "Park"; }
    else if (x == "recreation_ground"){ amenity = "Erholungsgebiet"; }
    else if (x == "dog_park"){ amenity = "Hundepark"; }
    else if (x == "playground"){ amenity = "Spielplatz"; }
    else if (x == "fitness_centre"){ amenity = "Fitnessstudio"; }
    else if (x == "cinema"){ amenity = "Kino"; }
    else if (x == "theatre"){ amenity = "Theater"; }
    else if (x == "nightclub"){ amenity = "Nachtclub"; }
    else if (x == "kindergarten"){ amenity = "Kindergarten"; }
    else if (x == "school"){ amenity = "Schule"; }
    else if (x == "college"){ amenity = "Hochschule"; }
    else if (x == "university"){ amenity = "Universität"; }
    else if (x == "doctors"){ amenity = "Arztpraxis"; }
    else if (x == "clinic"){ amenity = "Klinik"; }
    else if (x == "dentist"){ amenity= "Zahnarzt"; }
    else if (x == "hospital"){ amenity = "Krankenhaus"; }
    else if (x == "social_facility"){ amenity = "Soziale Einrichtung"; }
    else if (x == "nursing_home"){ amenity = "Pfelgeheim"; }
    else if (x == "veterinary"){ amenity = "Tierarzt"; }
    else if (x == "place_of_worship"){ amenity = "Andachtsort"; }
    else if (x == "supermarket"){ amenity = "Supermarkt"; }
    else if (x == "chemist"){ amenity = "Drogerie"; }
    else if (x == "pharmacy"){ amenity = "Apotheke"; }
    else if (x == "mall"){ amenity = "Einkaufszentrum"; }
    else if (x == "bank"){ amenity = "Bank"; }
    else if (x == "atm"){ amenity = "Geldautomat"; }
    else if (x == "restaurant"){ amenity = "Restaurant"; }

    return amenity;
}

function getCityFilterMarkerColor (x) {
    var color = "";

    if (x == "bus_stop" || x == "bus_station" || x == "subway_entrance" || x == "tram_stop" || x == "terminal"){ color = "purple"; }
    else if (x == "park" || x == "recreation_ground" || x == "dog_park" || x == "playground"){ color = "green"; }
    else if (x == "fitness_centre" || x == "cinema" || x == "theatre" || x == "nightclub" || x == "restaurant"){ color = "cadetblue"; }
    else if (x == "kindergarten" || x == "school" || x == "college" || x == "university") { color = "red"; }
    else if (x == "doctors" || x == "clinic" || x == "dentist" || x == "hospital" || x == "social_facility" || x == "nursing_home" || x == "veterinary"){ color = "blue"; }
    else if (x == "supermarket" || x == "chemist" || x == "pharmacy" || x == "mall") { color = "darkgreen"; }
    else if (x == "place_of_worship") { color = "darkpurple";}
    else if (x == "atm" || x == "bank") { color = "orange";}
    else if (x == "station") { color = "purple";}
    else {color = "darkred";}

    return color;
}

function getCityFilterMarkerIcon (x) {
    var icon = "";

    if (x == "bus_stop" || x == "bus_station") { icon = "bus"; }
    else if (x == "terminal") { icon = "plane";}
    else if (x == "subway_entrance") { icon = "subway";}
    else if (x == "tram_stop"){ icon = "train"; }
    else if (x == "station") { icon = "train";}
    else if (x == "park" || x == "recreation_ground"){ icon = "leaf"; }
    else if (x == "playground") { icon = "child";}
    else if (x == "dog_park") { icon = "paw";}
    else if (x == "fitness_centre" || x == "cinema" || x == "theatre" || x == "nightclub"){ icon = "star"; }
    else if (x == "restaurant") { icon = "cutlery";}
    else if (x == "kindergarten") { icon = "child";}
    else if (x == "school" || x == "college" || x == "university") { icon = "graduation-cap"; }
    else if (x == "doctors" || x == "clinic" || x == "dentist" || x == "hospital" || x == "social_facility" || x == "nursing_home"){ icon = "plus"; }
    else if (x == "veterinary") { icon = "paw";}
    else if (x == "supermarket" || x == "chemist" || x == "pharmacy" || x == "mall") { icon = "shopping-cart"; }
    else if (x == "place_of_worship") { icon = "users";}
    else if (x == "atm" || x == "bank") { icon = "eur";}
    else {icon = "question";}

    return icon;
}
