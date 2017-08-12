var map;
var markerClusters;
var intersectLayer;
var stadtteilLayer;
var lkw_verbot_layer;
var open_data_layer;
var pegel_layer;
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
            });
        var satellite_tiles = L.tileLayer(
            //old via mapbox
            'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}',
            {
            attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
            maxZoom: 18,
            //id: 'mapbox.mapbox-streets-v7',
            //id: 'mapbox.mapbox-terrain-v2',
            //id: 'mapbox.mapbox-traffic-v1',
            id: 'mapbox.satellite',
            accessToken: 'pk.eyJ1IjoicnN0b2RkZW4iLCJhIjoiY2ozdmt0ZDN3MDAydDR1cG1ybXduYjFsZiJ9.1SgNsXjR5DBwU6uEWTZF1A'
            });

        /*var lkw_verbot_layer = L.layerGroup(getOpenData('lkw_verbot'));
        var pegel_layer = L.layerGroup(getOpenData('pegel'));
        var open_data_layer = L.layerGroup([L.marker([50.938, 6.95]), L.marker([50.939, 6.96])]);*/
        var baseMaps = {
            'Karte': tiles,
            'Satellite': satellite_tiles
        };
        map = L.map('mapid', {
            center: [50.938, 6.95],
            zoom: 12,
            layers: [tiles]
        });

        //tiles zur map hinzufügen
        tiles.addTo(map);
        L.control.layers(baseMaps).addTo(map);

        //definieren von layern für Marker und Filter
        markerClusters = L.markerClusterGroup();
        intersectLayer = L.featureGroup();
        stadtteilLayer = L.featureGroup();

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

        // Karte klickbar machen
        map.on('contextmenu', function(e) {
            //alert("Lat, Lon : " + e.latlng.lat + ", " + e.latlng.lng);
            getPolyByCoords(e.latlng.lat, e.latlng.lng);
            //var gjLayer = L.geoJson(statesData);
            //var results = leafletPip.pointInLayer([e.latlng.lng, e.latlng.lat], gjLayer);
        });

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
    var color = "#e9993b";

    return color;
}
function alphanum(a, b, lenOsmId) {
  a = String(a).replace(/<(?:.|\n)*?>/gm, '').replace(/.* - /gm,'');
  b = String(b).replace(/<(?:.|\n)*?>/gm, '').replace(/.* - /gm,'');
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
/*function clearMap(m) {
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
}*/

function hideHirarchy() {
    document.getElementById("stadtbezirk_auswahl").style.visibility="hidden";
    document.getElementById("stadtebene_hoch_div").style.visibility="hidden";
}

function clearMap(map) {
    map.eachLayer(function(layer) {
        if( !(layer instanceof L.TileLayer) && (layer._path != undefined || layer._icon != undefined) ) {
            //console.log(layer.name);
            try {
                map.removeLayer(layer);
                //layer.clearLayers();
            }
            catch(e) {
                console.log("problem with " + e);
            }
        }
    });
    hideHirarchy();
}

/*function clearFilters(m) {
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
}*/
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
function clickPoly (event) {
    getCityPoly(event.target.options.osmId, true);
    map.fitBounds(this.getBounds());
}
function disableToggle (id) {
    $(id).bootstrapToggle('off');
    $(id).prop('disabled', true);
    $(id).parent().addClass('disabled');
    $(id).siblings('.toggle-group').children().each(function() {
        $(this).addClass('disabled');
        });
    /*$(id).prop('title', 'Keine Daten verfügbar');
    $(id).tooltip();*/
}
function enableToggle (id) {
    $(id).bootstrapToggle('off');
    $(id).prop('disabled', false);
    $(id).parent().removeClass('disabled');
    $(id).siblings('.toggle-group').children().each(function() {
        $(this).removeClass('disabled');
        });
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
                //kein Ergebnis bei Suche
                $('#stadtauswahl').text('');
                if (data.length == 0) {
                    swal("Suche erfolglos", "Die Suche war nicht erfolgreich. Bitte die Schreibweise im Suchfeld überprüfen.", "error");
                    return;
                }
                console.log(data[0]);
                disableAllFilters();
                deleteLayer(map, open_data_layer);
                deleteLayer(map, pegel_layer);
                //Ein-und Auszublenden der  OpenData
                pegel_layer = L.layerGroup();
                document.getElementById('laermpegel').checked = false;
                if (data[0].admin_level != '10' && data[0].admin_level != '9') {
                    disableToggle('#laermpegel');
                    disableToggle('#opendata_toggle');
                }
                else {
                    enableToggle('#laermpegel');
                    enableToggle('#opendata_toggle');
                    enableToggle('#lkw_verbot');
                }


                //berechnen der OpenData
                open_data_layer = L.layerGroup(getOpenData('opendata'));
                lkw_verbot_layer = L.layerGroup(getOpenData('lkw_verbot'));

                // Wenn nur ein Ergebnis in Ergebnismenge
                var sortList = []
                // erfolgreiche Suche im Suchfeld
                if (data[0].ambiguous == undefined) {
                    changeAuswahlName(data[0].name);
                }
                else {
                    changeAuswahlName('Mehrere gleiche Orte in Treffermenge');
                }
                deselect();
                // Filter werden freigeschaltet
                for (j = 0; j < data[0].osm_data_filter.length; j++) {
                    enableFilter(data[0].osm_data_filter[j]);
                }
                for (i=0; i < data.length; i++) {
                    if (data[0].ambiguous == undefined) {    
                        if (i != 0) {
                            if (data[i].affil_city_name.length != 0) {
                                var dropdownEntry = data[i].affil_city_name + ' - ' + data[i].name;
                            }
                            else {
                                var dropdownEntry = data[i].name
                            }
                            sortList.push('<a href="javascript:void(0)" class="list-group-item list-group-item-action" onclick="getCityPoly(' + data[i].osm_id + ',true)">' + dropdownEntry + '</a>');
                        }
                    }
                    else {
                        if (data[i].affil_city_name.length != 0) {
                            var dropdownEntry = data[i].affil_city_name + ' - ' + data[i].name;
                        }
                        else {
                            var dropdownEntry = data[i].name
                        }
                        sortList.push('<a href="javascript:void(0)" class="list-group-item list-group-item-action" onclick="getCityPoly(' + data[i].osm_id + ',true)">' + dropdownEntry + '</a>');
                    }
                    var latlngs = data[i].way;
                    // erstes Elemen in Date wird selected
                    if (i == 0 & data[0].ambiguous == undefined) {
                        var polyClassName = 'cityPoly selected';
                    }
                    else {
                        var polyClassName = 'cityPoly deselected';
                    }
                    var polygon = L.polygon(latlngs, {color: '#2d5e92', className: polyClassName, 'osmId': data[i].osm_id});
                    // Falls der Transparenz-Button aktiv ist, wird den neuen Polygonen die Transparenz-Klasse mitgegeben
                    // Check, ob der Transparenz-Button Aktiv ist
                    if ($('#transparent').parent().hasClass('btn-success')){
                        polyClassName = polyClassName+' transparent'
                        polygon.setStyle({className: polyClassName});
                        }
                    var tooltip = L.tooltip({
                        sticky: true,
                        direction: 'top'
                    })
                        .setContent(jsUcfirst(data[i].name));
                    polygon.bindTooltip(tooltip);
                    polygon.on('click', clickPoly);
                    polygon.addTo(stadtteilLayer);
                    // Falls etwas aus dem Dropdown oder Up-Button gewählt wird, wird hierauf gezoomt
                    if (i == 0 & osmId == true) {
                        map.fitBounds(polygon.getBounds());
                    }
                }
                stadtteilLayer.addTo(map);
                //Falls ein Stadtteil ausgewählt wurde, wird auf den Stadtteil gezoomt.
                if (data.length == 1 & data[0].ambiguous == undefined) {
                    $('#stadtauswahl').html('<a href="javascript:void(0)" class="list-group-item list-group-item-action" style="pointer-events: none;">Keine Stadtteile unter aktuellem Ergebnis</a>');
                    map.fitBounds(polygon.getBounds());
                }
                //Im Falle einer Suche wird auf das gesamte Ergebnis gezoomt
                else if (data.length > 1 & osmId == false) {
                    map.fitBounds(stadtteilLayer.getBounds());
                }
                // erfolgreiche hierarchische Suche und befüllen des DropDownMenüs
                showAuswahl();
                if (data[0].ambiguous != undefined) {
                    $('#stadtbezirk_auswahl').addClass('warning');
                    $('#stadtbezirk_auswahl').children('span').removeClass('caret').addClass('glyphicon glyphicon-warning-sign');
                }
                else if ($('#stadtbezirk_auswahl').hasClass('warning')) {
                    $('#stadtbezirk_auswahl').removeClass('warning');
                }
                showOpenData();
                sortList.sort(alphanum);
                if (data[0].parent_osm != 0 & data[0].ambiguous == undefined) {
                    var onclickHigher = "getCityPoly("+data[0].parent_osm+",true)";
                    changeStadtebeneName(data[0].parent_name);
                    $("#stadtebene_hoch").attr("onclick",onclickHigher);
                    document.getElementById("stadtebene_hoch_div").style.visibility="visible";
                    if (data[0].affil_city_name != data[0].name) {
                            changeAuswahlName(data[0].affil_city_name + ' - ' + data[0].name);
                    }  
                }
                else {
                    document.getElementById("stadtebene_hoch_div").style.visibility="hidden";
                }
                if (data[0].affil_city_name.toLowerCase() != 'köln') {
                    disableToggle('#laermpegel');
                    disableToggle('#opendata_toggle');
                    disableToggle('#lkw_verbot');
                }
                if (data[0].name == 'Köln') {
                    enableToggle('#lkw_verbot');
                }
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
                    deleteLayer(map, markerClusters);
                    // intersections an dieser Stelle löschen nur wenn false, da sonst durch ansynchronen Aufruf
                    // zum falschen Zeitpunkt gelöscht wird
                    if (intersection == false) {
                        deleteLayer(map, intersectLayer);
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
                    deleteLayer(map, intersectLayer);

                    getCityFilterMarker(filter, true);
                    for (i = 0; i < data.length; i++) {
                        var latlngs = data[i].way;
                        var polygon = L.polygon(latlngs, {color: getColor(getFilter()), className: 'intersection selected'});
                        polygon.addTo(intersectLayer);
                    }
                    map.addLayer(intersectLayer);
                    intersectLayer.bringToBack();
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
                    deleteLayer(map, lkw_verbot_layer);
                    //console.log('Zeichne Polygone für LKW-Verbot:', data.length);
                    for (i = 0; i < data.length; i++) {
                        var latlngs = data[i].rings;
                        var polygon = L.polygon(latlngs, {color: '#50555c'});
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
                    deleteLayer(map, pegel_layer);
                    //console.log('Zeichne Polygone für Lärmpegel:', data.length);
                    if (data == 'undefined' || data == 'empty') {
                        //document.getElementById('laermpegel').disabled = true;
                        disableToggle('#laermpegel');
                        //document.getElementById('laermpegel').style.opacity="1.0";
                        swal('Für diesen Suchbereich sind keine Lärmpegel verfügbar.', 'error')
                    }
                    else {
                        //zeichnen der rings als polygon
                        if (data[0].length > 0) {
                            for (i = 0; i < data[0].length; i++) {
                                var latlngs = data[0][i].rings;
                                if (data[0][i].dezibel === 55) {
                                    //var color = '#99c4d8';
                                    var classname_dezibel = dezibel_55;
                                }
                                else if (data[0][i].dezibel === 70) {
                                    //var color = '#0047ab';
                                    var classname_dezibel = dezibel_70;
                                }
                                else {
                                    //var color = '#093253';
                                    var classname_dezibel = dezibel_other;
                                }
                                var polygon = L.polygon(latlngs, {color: color, className: classname_dezibel});
                                var tooltip = L.tooltip({
                                    sticky: true,
                                    direction: 'top'
                                }).setContent(jsUcfirst("Lärmpegel: " + data[0][i].dezibel));
                                polygon.bindTooltip(tooltip);
                                /*var popup = L.popup({closeOnClick: true, className: 'map-popup'});
                                polygon.bindPopup(popup);*/
                                polygon.addTo(pegel_layer);
                                //console.log('polygon laermpegel');
                            }
                        }
                        // zeichnen der path als polylines
                        if (data[1].length > 0) {
                            for (i = 0; i < data[1].length; i++) {
                                var latlngs = data[1][i].path;
                                if (data[1][i].dezibel === 55) {
                                    var color = '#f6a68d';
                                }
                                else if (data[1][i].dezibel === 70) {
                                    var color = '#e92f15';
                                }
                                else {
                                    var color = '#941e0d';
                                }
                                var polygon = L.polyline(latlngs, {color: color, className: 'deselected'});
                                var tooltip = L.tooltip({
                                    sticky: true,
                                    direction: 'top'
                                }).setContent(jsUcfirst("Lärmpegel: " + data[1][i].dezibel));
                                polygon.bindTooltip(tooltip);
                                /*var popup = L.popup({closeOnClick: true, className: 'map-popup'});
                                polygon.bindPopup(popup);*/
                                polygon.addTo(pegel_layer);
                                //console.log('laermpegel polyline');
                            }
                        }
                        pegel_layer.addTo(map);
                    }
                }
                else {
                    //löschen der alten OpenDataanzeige, da sonst überzeichnet wird
                    deleteLayer(map, open_data_layer);
                    $(function() {
                        $('#opendata_toggle').bootstrapToggle("off");
                    });
                    document.getElementById('opendata_toggle').checked = false;
                    var anzahl_fehlende_open_data = 0;
                    for (i = 0; i < data.length; i++) {
                        var latlngs = data[i].way;
                        var polygon = L.polygon(latlngs, {className: 'deselected'});
                        /*var tooltip = L.tooltip({sticky: true, direction: 'top'}).setContent(jsUcfirst(data[i].name));
                        polygon.bindTooltip(tooltip);*/

                        if (data[i].admin_level == '10' && data[i].open_data != 'undefined') {
                            //console.log(data[i].open_data);
                            if (data[i].open_data.mietpreis[0]['mietpreis'] != 'unbekannt') {
                                var miete = data[i].open_data.mietpreis[0]['mietpreis'] + ' €'
                            }
                            else {
                                var miete = data[i].open_data.mietpreis[0]['mietpreis']
                            }
                            var tooltip_text = '<div style="text-align:center; font-weight: bold;">' + data[i].name + '</div>' +
                                                'Jugendarbeitslosenquote: ' + data[i].open_data.beschaeftigte[0]['jugendarbeitslosenquote'] + ' %' +
                                                '</br>Arbeitslosenquote: ' + data[i].open_data.beschaeftigte[0]['arbeitslosenquote'] + ' %' +
                                                '</br>Durchschnittsmietpreis: ' + miete +
                                                '</br>Durchschnittsalter: ' + data[i].open_data.durchschnittsalter[0]['durchschnittsalter'] + ' Jahre' +
                                                '</br></br>Landtagswahlergebnis: ' +
                                                    '</br><div class="partyMarker" style="background-color: #e3000f;"></div>SPD: ' + data[i].open_data.wahl[0]['gesamt_spd'] + ' %' +
                                                    '</br><div class="partyMarker" style="background-color: black;"></div>CDU: ' + data[i].open_data.wahl[0]['gesamt_cdu'] + ' %' +
                                                    '</br><div class="partyMarker" style="background-color: #46962B;"></div>Grüne: ' + data[i].open_data.wahl[0]['gesamt_gruene'] + ' %' +
                                                    '</br><div class="partyMarker" style="background-color: #ffed00;"></div>FDP: ' + data[i].open_data.wahl[0]['gesamt_fdp'] + ' %' +
                                                    '</br><div class="partyMarker" style="background-color: #DF0404;"></div>Die Linke: ' + data[i].open_data.wahl[0]['gesamt_die_linke'] + ' %' +
                                                    '</br><div class="partyMarker" style="background-color: #009EE0;"></div>AfD: ' + data[i].open_data.wahl[0]['gesamt_afd'] + ' %' +
                                                    '</br><div class="partyMarker" style="background-color: brown;"></div>NPD: ' + data[i].open_data.wahl[0]['gesamt_npd'] + ' %' +
                                                    '</br><div class="partyMarker" style="background-color: #f80;"></div>Piraten: ' + data[i].open_data.wahl[0]['gesamt_piraten'] + ' %';
                            var tooltip = L.tooltip({
                                closeOnClick: true,
                                direction: 'top'
                            }).setContent(tooltip_text);
                            polygon.bindTooltip(tooltip);
                        }
                        else {
                            var tooltip_text = 'Für diesen Suchbereich sind keine OpenData verfügbar.';
                            var tooltip = L.tooltip({
                                closeOnClick: true
                            }).setContent(tooltip_text);
                            polygon.bindTooltip(tooltip);
                            anzahl_fehlende_open_data += 1;
                        }
                        polygon.addTo(open_data_layer);

                        // wenn zu keinem polygon OpenData vorhanden sind, Funktion des Schalters ausgrauen
                        if (anzahl_fehlende_open_data === data.length) {
                            //document.getElementById('opendata_toggle').disabled = true;
                            //$('#opendata_toggle').bootstrapToggle('disable');
                            //document.getElementById('opendata_toggle').checked = false;
                            //document.getElementById('opendata_toggle').disabled = true;
                            $('#opendata_toggle').parent().addClass('disabled');
                            $('#opendata_toggle').siblings('.toggle-group').children().each(function() {
                            $(this).addClass('disabled');
                            });
                        }
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

function getPolyByCoords(lat, lng) {
    $.ajax(
        './search/PolyByCoords',
        {
            cache: false,
            dataType: "json",
            data: {
                csrfmiddlewaretoken: csrftoken,
                lat_point: lat,
                lng_point: lng
            },
            method: 'POST',
            success: function (data, textStatus, jqXHR) {
                if (data[1] != 'undefined') {
                    document.getElementById('town').value = data[0];
                    clearMap(map);
                    disableAllFilters();
                    deleteLayer(map, markerClusters);
                    deleteLayer(map, intersectLayer);
                    deleteLayer(map, stadtteilLayer);
                    getCityPoly(data[1], true);
                }
                else {
                    //console.log('punkt kann nicht zugeordnet werden');
                    swal("Suche erfolglos", "Die Suche war nicht erfolgreich. Bitte einen anderen Punkt auswählen.", "error");

                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                swal("Error", "Error: " + errorThrown + "\nStatus: " + textStatus + "\njqXHR: " + JSON.stringify(jqXHR), "error")
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

function showLayer(map, layer, button_id) {
    if (document.getElementById(button_id).checked) {
        layer.addTo(map);
    }
    else {
        //layer.clearLayers();
        if (map.hasLayer(layer)) {
            map.removeLayer(layer);
        }
    }
}

function deleteLayer(map, layer){
    if (map.hasLayer(layer)) {
        layer.clearLayers();
        map.removeLayer(layer);
    }
}

function berechneOpenData(button_id, OpenData, layer) {
    if (document.getElementById(button_id).checked) {
        getOpenData(OpenData);
        //showLayer(map, pegel_layer, button_id);
    }
    else {
        //layer.clearLayers();
        deleteLayer(map, layer);
    }
}