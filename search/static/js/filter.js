


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
    var umkreis = document.getElementById("min").value;
    if (!isNaN(umkreis)) {
        return umkreis;
    }
    else {
        alert("Bitte die Entfernung in Ziffern angeben!");
    }
}

function getMax(){
    var umkreis = "";
    var umkreis = document.getElementById("max").value;
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
        if (getMin() >= getMax() && getMin() != "" && getMax() != ""){  // kontrolliert ob der minimale Wert des Rasius wirklick klein er als der größere Umkreis-Wert ist
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
function changeAuswahlName(){
    console.log(getCityName());
    document.getElementById("stadtbezirk_auswahl").innerHTML= getCityName();
    console.log("Auswahlname geändert!");
}

/**
 * Fasst alle Methoden zusammen die beim Betätigen des Such-Buttons ausgelöst werden sollen.
 */
function searchOnClicks(){
    getCityPoly(getCityName());
    changeAuswahlName();

}

// function createFilterButton(name, filter){
//     var button = document.createElement("BUTTON");
//     button.type = "button";
//     var t = document.createTextNode(document.getElementById(filter).textContent);
//     button.appendChild(t);
//     button.className= "btn";
//     button.id = filter;
//     button.innerHTML = document.getElementById(filter);
//     // button.onclick = func;
//     document.getElementById('input_marked_filter').appendChild(button);
// }