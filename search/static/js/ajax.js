var map;
var csrftoken;
$(document).ready(
    function init_map() {
        csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        map = L.map('mapid').setView([50.938, 6.95], 12);
        L.tileLayer(
            //local

            '/static/leaflet/tiles/{z}/{x}/{y}.png',
            {
            minZoom: 9,
            maxZoom: 16
            }


            //old via mapbox
            /*
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
        ).addTo(map);
        //var marker = L.marker([50.938, 6.95]).addTo(map);
        //var poly = L.polygon([[[50.9690877834368,7.00925780777239],[50.9682048669575,7.00911972076204],[50.9673558646356,7.00871076633736],[50.9665734058739,7.00804666038754],[50.9658875641941,7.00715292413179],[50.9653247009086,7.00606390335322],[50.9649064513392,7.00482144850962],[50.9646488926526,7.00347330644385],[50.9645619254045,7.00207128549944],[50.9646488926526,7.00066926455503],[50.9649064513392,6.99932112248925],[50.9653247009086,6.99807866764565],[50.9658875641941,6.99698964686708],[50.9665734058739,6.99609591061134],[50.9673558646356,6.99543180466152],[50.9682048669575,6.99502285023683],[50.9690877834368,6.99488476322648],[50.9699706831334,6.99502285023683],[50.9708196376624,6.99543180466152],[50.9716020248969,6.99609591061134],[50.9722877822047,6.99698964686708],[50.9728505611183,6.99807866764565],[50.9732687391606,6.99932112248925],[50.9735262500543,7.00066926455503],[50.9736132005197,7.00207128549944],[50.9735262500543,7.00347330644385],[50.9732687391606,7.00482144850962],[50.9728505611183,7.00606390335322],[50.9722877822047,7.00715292413179],[50.9716020248969,7.00804666038754],[50.9708196376624,7.00871076633736],[50.9699706831334,7.00911972076204],[50.9690877834368,7.00925780777239]],[[50.9690877834368,7.02363085231831],[50.9655736869431,7.02289622789339],[50.9622988310278,7.02074241805917],[50.959486464264,7.0173162013965],[50.9573283439166,7.01285106890887],[50.9559716414413,7.00765131199632],[50.9555088864332,7.00207128549944],[50.9559716414413,6.99649125900256],[50.9573283439166,6.99129150209],[50.959486464264,6.98682636960237],[50.9622988310278,6.98340015293971],[50.9655736869431,6.98124634310549],[50.9690877834368,6.98051171868057],[50.9726016140884,6.98124634310549],[50.9758757437098,6.98340015293971],[50.9786871183376,6.98682636960237],[50.9808442465492,6.99129150209],[50.9822002227305,6.99649125900256],[50.9826627118967,7.00207128549944],[50.9822002227305,7.00765131199632],[50.9808442465492,7.01285106890887],[50.9786871183376,7.0173162013965],[50.9758757437098,7.02074241805917],[50.9726016140884,7.02289622789339],[50.9690877834368,7.02363085231831]]]).addTo(map);
    }
);
/**
 * @global map
 */
function jsUcfirst(string)
{
    return string.charAt(0).toUpperCase() + string.slice(1);
}
function getColor(value) {
    return value == 'bus_stop'  ? '#C7ABCA' :
           value == 'station'  ? '#A684AA' :
           value == 'subway_entrance'  ? '#B6A6B8' :
           value == 'tram_stop'  ? '#EFC7F3' :
           value == 'terminal'  ? '#D3CCF8' :
           value == 'dog_park'  ? '#76B38A' :
           value == 'fitness_centre'  ? '#75D6AF' :
           value == 'park'  ? '#BFF6D1' :
           value == 'playground'  ? '#9ACFAB' :
           value == 'cinema'  ? '#3CA57B' :
           value == 'nightclub'  ? '#3EE4A2' :
           value == 'theatre'  ? '#A5CEBE' :
           value == 'recreation_ground'  ? '#EBD6ED' :
                      '#FFEDA0';
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
                var list = "";
                $('#stadtauswahl').text('');
                if (data.length == 1) {
                $('#stadtauswahl').html('<a href="#" class="list-group-item list-group-item-action" style="pointer-events: none;">Keine Stadtteile unter aktuellem Ergebnis</a>');
                }
                changeAuswahlName(data[0].name);
                for (i = 0; i < data.length; i++) {
                    if (i != 0) {
                        list+= '<a href="#" class="list-group-item list-group-item-action" onclick="getCityPoly('+data[i].osm_id+',true)">'+data[i].name+'</a>';
                    }
                    console.log(data.length);
                    var latlngs = data[i].way;
                    var polygon = L.polygon(latlngs, {color: 'red', className: 'cityPoly', opacity:0.99});
                    var tooltip = L.tooltip({sticky: true,
                                            direction: 'top'})
                        .setContent(jsUcfirst(data[i].name))
                    polygon.bindTooltip(tooltip);
                    var popup = L.popup({closeOnClick: true,
                                        className: 'map-popup'})
                        .setContent('Lorem Ipsum dolor sit amet');
                    polygon.bindPopup(popup);
                    polygon.addTo(map);
                    if (i == 0) {
                        map.fitBounds(polygon.getBounds());
                    }
                }$('#stadtauswahl').append(list);
                $('html, body').animate({
        scrollTop:$('#mapid').offset().top*0.7
    },'slow');
            },
            error: function (jqXHR, textStatus, errorThrown) {
                alert("Error: " + errorThrown
                    + "\nStatus: " + textStatus
                    + "\njqXHR: " + JSON.stringify(jqXHR)
                );
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
                filter_value: filter,
            },
            method: 'POST',
            success: function (data, textStatus, jqXHR) {
                console.log(data.length);
                if (data.length == 0) {
                    alert("Bitte mindestens einen und maximal 3 Filter auswählen! Es wurden keine Treffer gefunden.");
                }
                else {
                    for (i = 0; i < data.length; i++) {
                        var latlngs = data[i].way;
                        var polygon = L.polygon(latlngs, {color: getColor(getFilter())}).addTo(map);
                    }
                }
            },
            /*success: function (data, textStatus, jqXHR) {
                console.log(data);
                var latlongs = makePoints(data[0].way); // todo: funktioniert nicht für Ringe, da doppeltes Polygon, muss anders gesplittet werden
                var polygon = L.polygon(latlongs, {color: 'red'}).addTo(map);
                map.fitBounds(polygon.getBounds())
            },*/
            error: function (jqXHR, textStatus, errorThrown) {
                alert("Error: " + errorThrown
                    + "\nStatus: " + textStatus
                    + "\njqXHR: " + JSON.stringify(jqXHR)
                );
            },
            complete: function (jqXHR, textStatus) {}
        }
    );
}

function getCityFilterMarker  (filter) {
    $.ajax(
        './search/cityFilterMarker',
        {
            cache: false,
            dataType: "json",
            data: {
                csrfmiddlewaretoken: csrftoken,
                filter_value: filter,
            },
            method: 'POST',
            success: function (data, textStatus, jqXHR) {
                console.log(data.length);
                if (data.length == 0) {
                    alert("Bitte mindestens einen Filter auswählen! Es wurden keine Treffer gefunden.");
                }
                else {
                    //var markerClusters = L.markerClusterGroup({ chunkedLoading: true });
                    var markerClusters = L.markerClusterGroup();
                    for (i = 0; i < data.length; i++) {
                        var latlngs = data[i].way;
                        var marker = L.marker(latlngs);
                        var amenity = getAmenity(data[i].amenity)
                        var name = data[i].name
                        var marker_text = ""

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
                alert("Error: " + errorThrown
                    + "\nStatus: " + textStatus
                    + "\njqXHR: " + JSON.stringify(jqXHR)
                );
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
                table_name: type_data,
            },
            method: 'POST',
            success: function (data, textStatus, jqXHR) {
                if (type_data === 'lkw_verbot') {
                    console.log('Zeichne Polygone für LKW-Verbot', data.length);
                    for (i = 0; i < data.length; i++) {
                        var latlngs = data[i].rings;
                        var polygon = L.polygon(latlngs, {color: 'black'});
                        var tooltip = L.tooltip({sticky: true, direction: 'top'}).setContent(jsUcfirst("LKW-Verbotszone"))
                        polygon.bindTooltip(tooltip);
                        var popup = L.popup({closeOnClick: true, className: 'map-popup'});
                        polygon.bindPopup(popup);
                        polygon.addTo(map);
                    }
                }
                else if (type_data === 'pegel'){
                    console.log('Zeichne Polygone für Lärmpegel:', data.length);
                    for (i = 0; i < data.length; i++) {
                        var latlngs = data[i].rings;
                        if (data.dezibel === '55') {var color = '#99c4d8';}
                        else if (data.dezibel === '70') {var color = '#0047ab';}
                        else {var color = '#093253';}

                        var polygon = L.polygon(latlngs, {color: color});
                        var tooltip = L.tooltip({sticky: true, direction: 'top'}).setContent(jsUcfirst("Lärmpegel: "+data[i].dezibel))
                        polygon.bindTooltip(tooltip);
                        var popup = L.popup({closeOnClick: true, className: 'map-popup'});
                        polygon.bindPopup(popup);
                        polygon.addTo(map);
                    }
                }

                else {
                    for (i = 0; i < data.length; i++) {
                        console.log(data[i])
                    }
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                alert("Error: " + errorThrown
                    + "\nStatus: " + textStatus
                    + "\njqXHR: " + JSON.stringify(jqXHR)
                );
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