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
                swal("Achtung", err, "error");
                //alert("Achtung: " + err);
                }
    }
    else if(x == "") {
        swal("Kein Filter", "Bitte einen Filter auswählen!", "error");
        //alert("Achtung: Bitte einen Filter auswählen!");
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
}

function getMax(){
    var umkreis = "";
    var umkreis = parseInt(document.getElementById("max").value);
    if (!isNaN(umkreis)) {
        return umkreis;
    }
}

function isInteger() {
    var min = document.getElementById("min").value;
    var max = document.getElementById("max").value;
    noComma = false;
    if (min.indexOf(',') != -1) {
        noComma = false;
    }
    else if (min.indexOf('.') != -1) {
        noComma = false;
    }
    else if (max.indexOf(',') != -1) {
        noComma = false;
    }
    else if (max.indexOf('.') != -1) {
        noComma = false;
    }
    else {
        noComma = true;
    }
    return noComma;
}

function checkRadius() {
    radius = false;
    var max = parseInt(document.getElementById("max").value);
    var min = parseInt(document.getElementById("min").value);
    if (!isNaN(max)) {
        radius = true;
    }
    else if (!isNaN(min)){
        radius = true;
    }
    else {
       radius = false;
    }
    return radius;
}

function checkMin() {
    var exists = false;
    var min = parseInt(document.getElementById("min").value);
    if (!isNaN(min)){
       exists = true;
    }
    return exists;
}

function checkMax() {
    var exists = false;
    var max = parseInt(document.getElementById("max").value);
    if (!isNaN(max)) {
        exists = true;
    }
    return exists;
}

function checkMinMax() {
    minMax = false;
    var max = parseInt(document.getElementById("max").value);
    var min = parseInt(document.getElementById("min").value);
    if (!isNaN(max)) {
        if (!isNaN(min)) {
            minMax = true;
        }
    }
    else {
       minMax = false;
    }
    return minMax;
}

function addFilter() {
    if (getFilterProof() == ""){    //verhindert dass etwas in die Filterzeile geschrieben wird, wenn kein Filter angeklickt wurde
        document.getElementById("markedFilter").value += "";

    }
    else if (!isInteger()) {
        swal("Fehlerhafter Eintrag", "Bitte keine Kommazahlen eintragen!", "error");
        //alert("Bitte keine Kommazahlen eintragen!");
        document.getElementById("markedFilter").value += "";
        for (var i = 0; i < used_filters.length; i++){
                if (getFilter() == used_filters[i]){
                    used_filters.splice(i, 1)
                 }
            }
    }
    else {
        if (getMin() >= getMax() && checkMinMax()){  // kontrolliert ob der minimale Wert des Radius wirklick klein er als der größere Umkreis-Wert ist
            swal("Fehlerhafter Eintrag", "Die Maximale Entfernung muss größer als die minimale Entfernung sein!", "error");
            //alert("Die Minimale Entfernung muss größer als die Maximale entfernung sein!")
            document.getElementById("markedFilter").value += "";
            for (var i = 0; i < used_filters.length; i++){  // diese Schleife kann genutzt werden wenn ein Filter wieder aus dem Array used_filters[] gelöscht werden soll.
                if (getFilter() == used_filters[i]){
                    used_filters.splice(i, 1)
                 }
            }
        }
        else if(!checkRadius()){ // gibt den Wert "marker" in die Filter-Zeile (an Stelle der Radius-Werte) wenn beide Radisu-Felder leer gelassen wurden
            document.getElementById("markedFilter").value += getFilter() + ":" + " marker;";
            createFilterButton(getFilter(), getFilterID(), 1);
            showFilter();
        }
        //nur Min wird leer gelassen
        else if(!checkMin() && checkMax()) {
            document.getElementById("markedFilter").value += getFilter() + ":" + "0, " + getMax() + ";";
            createFilterButton(getFilter(), getFilterID(), 2);
            showFilterIntersections();
        }
        //nur Max wird leer gelassen
        else if(checkMin() && !checkMax())  {
            document.getElementById("markedFilter").value += getFilter() + ":" + getMin() + ", 10000;";
            createFilterButton(getFilter(), getFilterID(), 3);
            showFilterIntersections();
        }
        else {  //fügt die neuen Einträge in die Filter-Zeile hinzu. --> das ist der Basisfall
            document.getElementById("markedFilter").value += getFilter() + ":" + getMin() + ", " + getMax() + ";";
            createFilterButton(getFilter(), getFilterID(), 4);
            // testGetFilterName(getFilterID());
            showFilterIntersections();
        }
    }
}

function getCityName() {
    var failed = "failed";
    var city = document.getElementById('town').value;
    console.log(city);
    if (city == "") {
        swal("Leere Suche", "Bitte etwas in das Suchfeld eintragen!", "error");
        return failed;
    }
    else {
        return city;
    }
}

function getFilterText() {
    var text = document.getElementById('markedFilter').value;
    if (text !== '') {
        return text
    }
    else {
        swal("Keine Filter", "Bitte mindestens einen Filter auswählen!", "error");
        //alert("Bitte mindestens einen Filter auswählen!");
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
    document.getElementById("stadtbezirk_auswahl").innerHTML= cityName + "<span class=\"caret\"></span>";
    console.log("Auswahlname geändert!");
}

function changeStadtebeneName (city) {
    document.getElementById("stadtebene_hoch").innerHTML= city;
}

/**
 * Fasst alle Methoden zusammen die beim Betätigen des Such-Buttons ausgelöst werden sollen.
 */
function searchOnClicks(){
    var city = getCityName();
    if (city == "failed") {
        return;
    }
    clearMap(map);
    disableAllFilters();
    //enableAllFilters();
    deleteLayer(map, markerClusters);
    deleteLayer(map, intersectLayer);
    deleteLayer(map, stadtteilLayer);

    getCityPoly(getCityName(), osmId=false);
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
    //document.getElementById("stadtebene_hoch_div").style.visibility="visible";
    document.getElementById("input_marked_filter_div").style.display="block";

    document.getElementById("transparent_div").style.visibility="visible";
    document.getElementById("clearmap").style.visibility="visible";
}

function showOpenData() {
    document.getElementById("opendata_div").style.visibility="visible";
 /*   $(function() {
        $('#opendata_toggle').bootstrapToggle("off");
    })*/
    document.getElementById("lkw_verbot_div").style.visibility="visible";
    document.getElementById("laermpegel_div").style.visibility="visible";
}

function showFilterIntersections() {
    document.getElementById("filter_output_div").style.visibility="visible";
    document.getElementById("use_filter_div").style.visibility="visible";
}

function showFilter() {
    document.getElementById("filter_output_div").style.visibility="visible";
}

function hideFilter() {
    document.getElementById("filter_output_div").style.visibility="hidden";
}

function hideIntersections() {
    document.getElementById("use_filter_div").style.visibility="hidden";
}

function toggleTransparency() {
    var toggle = document.getElementById("transparent").checked;
    if (toggle) {
        setTransparency();
    }
}

function disableAllFilters() {
    for (var i=1; i < 34; i++) {
        document.getElementById(i).parentElement.classList.add("dropdownDisabled");
        document.getElementById(i).classList.add("dropdownDisabled");
        document.getElementById(i).nextSibling.classList.add("dropdownDisabled");
        document.getElementById(i).disabled = true;
    }
}

function enableFilter(value) {
    var filterID = getFilterValue(value);
    try {
    document.getElementById(filterID).parentElement.classList.remove("dropdownDisabled");
    document.getElementById(filterID).classList.remove("dropdownDisabled");
    document.getElementById(filter_id).nextSibling.classList.remove("dropdownDisabled");
    document.getElementById(filterID).disabled = false;
    //document.getElementById(filterID).parentElement.style.opacity="1.0";
    }
    catch(err) {}
}

function enableAllFilters() {
    for (var i=1; i < 34; i++) {
        document.getElementById(i).disabled = false;
        document.getElementById(i).style.opacity="1.0";
    }
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

function getFilterValue(x) {
    var amenity = 0;

    if (x == "bus_stop"){ amenity = 1; }
    else if (x == "bus_station"){ amenity = 2; }
    else if (x == "station"){ amenity = 3; }
    else if (x == "subway_entrance"){ amenity = 4; }
    else if (x == "tram_stop"){ amenity = 5; }
    else if (x == "terminal"){ amenity = 6; }
    else if (x == "park"){ amenity = 7; }
    else if (x == "recreation_ground"){ amenity = 8; }
    else if (x == "dog_park"){ amenity = 9; }
    else if (x == "playground"){ amenity = 10; }
    else if (x == "fitness_centre"){ amenity = 11; }
    else if (x == "cinema"){ amenity = 12; }
    else if (x == "theatre"){ amenity = 13; }
    else if (x == "nightclub"){ amenity = 14; }
    else if (x == "kindergarten"){ amenity = 15; }
    else if (x == "school"){ amenity = 16; }
    else if (x == "college"){ amenity = 17; }
    else if (x == "university"){ amenity = 18; }
    else if (x == "doctors"){ amenity = 19; }
    else if (x == "clinic"){ amenity = 20; }
    else if (x == "dentist"){ amenity= 21; }
    else if (x == "hospital"){ amenity = 22; }
    else if (x == "social_facility"){ amenity = 23; }
    else if (x == "nursing_home"){ amenity = 24; }
    else if (x == "veterinary"){ amenity = 25; }
    else if (x == "place_of_worship"){ amenity = 26; }
    else if (x == "supermarket"){ amenity = 27; }
    else if (x == "chemist"){ amenity = 28; }
    else if (x == "pharmacy"){ amenity = 29; }
    else if (x == "mall"){ amenity = 30; }
    else if (x == "bank"){ amenity = 31; }
    else if (x == "atm"){ amenity = 32; }
    else if (x == "restaurant"){ amenity = 33; }

    return amenity;
}


function testGetFilterName(filter_id){
    console.log("TestGetFilterName: Ausgewählter Filter:" + getFilterName(filter_id));
}

function createFilterButton(name, filter, radiusCase){
    var button = document.createElement("BUTTON");
    button.className= "btn chosen-filter";
    var newID= filter + "button";
    button.id = newID;
    // var filter_name = document.getElementById("filter"
    var t = "";
    if (radiusCase == 1) {
        t = document.createTextNode(getFilterName(filter));
    }
    else if (radiusCase == 2) {
        t = document.createTextNode(getFilterName(filter)+ ": 0" + " - " + getMax());
    }
    else if (radiusCase == 3) {
        t = document.createTextNode(getFilterName(filter)+ ": " + getMin() + " - 10000");
    }
    else {
        t = document.createTextNode(getFilterName(filter)+ ": " + getMin() + " - " + getMax());
    }
    button.appendChild(t);
    document.getElementById('input_marked_filter_div').appendChild(button);
    button.onclick = function() {
        document.getElementById(newID).remove();
        removeFilterFromTextarea(name);
        filter = checkExistingFilter();
        //check if there is no filter left
        if (filter == "noFilter") {
            hideFilter(),
            hideIntersections();
        }
        //check if there is no filter with radius left
        if (filter == "noIntersection") {
            hideIntersections();
        }
    }
}

function checkExistingFilter() {
    var result = "";
    var intersection = false;
    var textarea_text = document.getElementById("markedFilter").value;
    var filter = textarea_text.split(";");
    for (var i=0; i < filter.length-1; i++) {
        hasNumber = /\d/.test(filter);
        if (hasNumber) {
            intersection = true;
        }
    }
    if (textarea_text == "") {
        return result = "noFilter";
    }
    else if (textarea_text != "" && !intersection) {
        return result = "noIntersection";
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
            console.log("Zu löschendes Element: " + res[i] + ", " + res);
            res.splice(i, 1);
        }
    }
    console.log(res);
    document.getElementById("markedFilter").value = "";
    for (var i=0; i < res.length; i++) {
        document.getElementById("markedFilter").value += res[i];
    }

    for (var i = 0; i < used_filters.length; i++){
        if (filter_name == used_filters[i]){
            used_filters.splice(i, 1)
        }
    }

}


function enterpressalert(e, textarea){
    var code = (e.keyCode ? e.keyCode : e.which);
    if(code == 13) { //Enter keycode
        e.preventDefault();
        searchOnClicks();
    }
}

/*function test() {
    changeStadtebeneName("test");
}*/
