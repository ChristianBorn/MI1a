var used_filters = [];

/**
 * fügt Filter und Umkreis in die Filter-Zeile ohne die Überprüfung auf doppelt ausgewählte Filter
 * @returns {string}
 */
function getFilter() {
    var x = "";

    var i = 1;

    while (i <= 33) {

        var filter_id = i.toString();
        if (document.getElementById(filter_id).checked == true){
        //console.log(document.getElementById(filter_id).value);
        x = document.getElementById(filter_id).value;
        break;
        } else {
            var i = i +1;
        }
    }
    return x;
}

function getFilterID(){


    var i = 1;

    while (i <= 33) {

        var filter_id = i.toString();
        if (document.getElementById(filter_id).checked == true){
        //console.log(document.getElementById(filter_id).value);
        return filter_id;
        }
        else {
            i++;
        }
    }

}
/**
 * liest die Filter und die passenden Umkreise aus und überprüft ob ein Filter noch nicht in der Filterzeile steht
 * @returns {string}
 */
function getFilterProof(){
    var x = "";

    var i = 1;

    while (i <= 33) {

        var filter_id = i.toString();
        if (document.getElementById(filter_id).checked == true){
        //console.log(document.getElementById(filter_id).value);
        x = document.getElementById(filter_id).value;
        break;
        } else {
            var i = i +1;
        }
    }
    if (x !== "") {
        try {
            for (var j = 0; j <= used_filters.length; j++) {
                if (x == used_filters[j]) {
                    x = "";
                    throw "Der Filter existiert bereits!";
                }
            }
        }
        catch (err) {
                alert("Achtung: " + err);
                }
    }
    else {
        alert("Achtung: Bitte einen Filter auswählen!");
    }
    used_filters.push(x);
    console.log(used_filters);
    return x;
}



function getMin(){
    var umrkeis = "";
    var umkreis = parseInt(document.getElementById("min").value);
    if (!isNaN(umkreis)) {
        return umkreis;
    }
    else {
        alert("Bitte die Entfernung in Ziffern angeben!");
    }
}

function getMax(){
    var umkreis = "";
    var umkreis = parseInt(document.getElementById("max").value);
    if (!isNaN(umkreis)) {
        return umkreis;
    }
    else {
        alert("Bitte die Entfernung in Ziffern angeben!");
    }

}

function addFilter() {

    if (getFilterProof() == ""){    //verhindert dass etwas in die Filterzeile geschrieben wird, wenn kein Filter angeklickt wurde
        document.getElementById("markedFilter").value += "";
    }
    else {
        if (getMin() >= getMax() && getMin() != "" && getMax() != ""){  // kontrolliert ob der minimale Wert des Radius wirklick klein er als der größere Umkreis-Wert ist
            alert("Die Minimale Entfernung muss größer als die Maximale entfernung sein!")
            document.getElementById("markedFilter").value += "";
        }
        else if(getMin() == "" && getMax() == ""){ // gibt den Wert "marker" in die Filter-Zeile (an Stelle der Radius-Werte) wenn beide Radisu-Felder leer gelassen wurden
            document.getElementById("markedFilter").value += getFilter() + ":" + " marker;";
            createFilterButton(getFilter(), getFilterID());
        }
        else {  //fügt die neuen Einträge in die Filter-Zeile hinzu. --> das ist der Basisfall
            document.getElementById("markedFilter").value += getFilter() + ":" + getMin() + ", " + getMax() + ";";
            createFilterButton(getFilter(), getFilterID());
            // testGetFilterName(getFilterID());
        }
    }
}

function getCityName() {
    return document.getElementById('town').value;
}

function getFilterText() {
    var text = document.getElementById('markedFilter').value;
    if (text !== '') {
        return text
    }
    else {
        alert("Bitte mindestens einen und maximal 3 Filter auswählen!");
    }
}

function getCityOsmId() {
    var osm_id = document.getElementById('city_osm_id').value;
    if (osm_id !==  '') {
        return osm_id;
    }
    else {
        return -62578;
    }
}

/**
 * Bennent den Button der Stadtbezirksauswahl um und gibt ihm den Namen der aktuellen Suchanfrage.
 */
function changeAuswahlName(cityName = getCityName()){
    console.log(getCityName());
    document.getElementById("stadtbezirk_auswahl").innerHTML= cityName;
    console.log("Auswahlname geändert!");
}

/**
 * Fasst alle Methoden zusammen die beim Betätigen des Such-Buttons ausgelöst werden sollen.
 */
function searchOnClicks(){
    getCityPoly(getCityName());
    changeAuswahlName();
    showAuswahl();
}

function showAuswahl() {
    document.getElementById("stadtbezirk_auswahl").style.visibility="visible";

    document.getElementById("filter1").style.display="block";
    document.getElementById("filter2").style.display="block";
    document.getElementById("filter3").style.display="block";
    document.getElementById("filter4").style.display="block";
    document.getElementById("filter5").style.display="block";
    document.getElementById("filter6").style.display="block";
    document.getElementById("inputmin_div").style.display="block";
    document.getElementById("inputmax_div").style.display="block";
    document.getElementById("min_div").style.display="block";
    document.getElementById("max_div").style.display="block";
    document.getElementById("add-filter_div").style.display="block";
    document.getElementById("input_marked_filter_div").style.display="block";
    document.getElementById("filter_output_div").style.display="block";
    document.getElementById("use_filter_div").style.display="block";

    document.getElementById("beschaeftigte_div").style.visibility="visible";
    document.getElementById("laermpegel_div").style.visibility="visible";
    document.getElementById("landtagswahl_div").style.visibility="visible";
    document.getElementById("lkw_verbot_div").style.visibility="visible";
    document.getElementById("landuse_div").style.visibility="visible";
}

function getFilterName(x) {
    var result = "";

    if (x == 1){ result = "Bushaltestelle"; }
    else if (x == 2){ result = "Busbahnhof"; }
    else if (x == 3){ result = "Bahnhof"; }
    else if (x == 4){ result = "U-Bahn"; }
    else if (x == 5){ result = "Straßenbahn"; }
    else if (x == 6){ result = "Flughafen"; }
    else if (x == 7){ result = "Park"; }
    else if (x == 8){ result = "Erholungsgebiet"; }
    else if (x == 9){ result = "Hundepark"; }
    else if (x == 10){ result = "Spielplatz"; }
    else if (x == 11){ result = "Fitnessstudio"; }
    else if (x == 12){ result = "Kino"; }
    else if (x == 13){ result = "Theater"; }
    else if (x == 14){ result = "Nachtclub"; }
    else if (x == 15){ result = "Kindergarten"; }
    else if (x == 16){ result = "Schule"; }
    else if (x == 17){ result = "Hochschule"; }
    else if (x == 18){ result = "Universität"; }
    else if (x == 19){ result = "Arztpraxis"; }
    else if (x == 20){ result = "Klinik"; }
    else if (x == 21){ result = "Zahnarzt"; }
    else if (x == 22){ result = "Krankenhaus"; }
    else if (x == 23){ result = "Soziale Einrichtung"; }
    else if (x == 24){ result = "Pfelgeheim"; }
    else if (x == 25){ result = "Tierarzt"; }
    else if (x == 26){ result = "Andachtsort"; }
    else if (x == 27){ result = "Supermarkt"; }
    else if (x == 28){ result = "Drogerie"; }
    else if (x == 29){ result = "Apotheke"; }
    else if (x == 30){ result = "Einkaufszentrum"; }
    else if (x == 31){ result = "Bank"; }
    else if (x == 32){ result = "Geldautomat"; }
    else if (x == 33){ result = "Restaurant"; }

    return result;
}


function testGetFilterName(filter_id){
    console.log("TestGetFilterName: Ausgewählter Filter:" + getFilterName(filter_id));
}

function createFilterButton(name, filter){
    var button = document.createElement("BUTTON");
    button.className= "btn chosen-filter";
    var newID= filter + "button";
    button.id = newID;
    // var filter_name = document.getElementById("filter"
    var t = document.createTextNode(getFilterName(filter)+ ": " + getMin() + " - " + getMax());
    button.appendChild(t);
    document.getElementById('input_marked_filter_div').appendChild(button);
    button.onclick = function() {
        document.getElementById(newID).remove();
        removeFilterFromTextarea(name);
    }

}

function removeFilterFromTextarea(filter_name) {
    console.log("zu löschender Filter: " + filter_name);
    var textarea_text = document.getElementById("markedFilter").value;
    console.log(textarea_text);
    var res = textarea_text.split(";");
    console.log(res);
    for (var i=0; i < res.length-1; i++){
        res[i]= res[i] + ";";
    }
    console.log(res);
    for (var i=0; i < res.length; i++){
        if (res[i].startsWith(filter_name)){
            console.log(res[i]);
            res.splice(i, i+1)
        }
    }
    console.log(res);
    document.getElementById("markedFilter").value = "";
    for (var i=0; i < res.length; i++) {
        document.getElementById("markedFilter").value += res[i];
    }

}

/*function removeFilterButton(filter_id) {
    document.getElementById(filter_id).remove;
}*/
    /*var elem = document.getElementById(filter_id);
    elem.parentNode.removeChild(elem);*/
