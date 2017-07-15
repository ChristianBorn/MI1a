var map;
var csrftoken;
$(document).ready(
    function init_map() {
        csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        map = L.map('mapid').setView([50.938, 6.95], 12);
        L.tileLayer(
            //local
            /*
            '/static/leaflet/tiles/{z}/{x}/{y}.png',
            {
            minZoom: 9,
            maxZoom: 16
            }*/


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
            }
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
           value == 'terminal'  ? '#766278' :
           value == 'dog_park'  ? '#EBD6ED' :
           value == 'fitness_centre'  ? '#EBD6ED' :
           value == 'park'  ? '#EBD6ED' :
           value == 'playground'  ? '#EBD6ED' :
           value == 'cinema'  ? '#EBD6ED' :
           value == 'nightclub'  ? '#EBD6ED' :
           value == 'theatre'  ? '#EBD6ED' :
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
                changeAuswahlName(data[0].name)
                for (i = 0; i < data.length; i++) {
                    if (i != 0) {
                        list+= '<a href="#" class="list-group-item list-group-item-action" onclick="getCityPoly('+data[i].osm_id+',true)">'+data[i].name+'</a>';
                    }
                    console.log(data.length);
                    var latlngs = data[i].way;
                    var polygon = L.polygon(latlngs, {color: 'red'});
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
                    alert("Bitte mindestens einen und maximal 3 Filter auswählen! Es wurden keine Treffer gefunden.");
                }
                else {
                    //var markerClusters = L.markerClusterGroup();
                    for (i = 0; i < data.length; i++) {
                        var latlngs = data[i].way;
                        var marker = L.marker(latlngs).addTo(map);
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


function getOpenData  (type_data, checked) {
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
                if (checked == true) {
                    console.log(data.length)
                    for (i = 0; i < data.length; i++) {
                        console.log(data[i]);
                        //todo: anzeige auf Karte einfügen
                    }
                }
                else {
                    console.log('clear');
                    //todo: anzeige auf Karte entfernen
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