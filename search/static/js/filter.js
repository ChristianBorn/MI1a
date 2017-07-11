

function getFilter(){
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
        return x;
    }
    else {
        alert("Bitte einen Filter auswählen!");
    }
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
    console.log(getMin());
    console.log(getMax());
    console.log(getFilter());
    document.getElementById("markedFilter").value += getFilter() + ":" + getMin() + ", " + getMax() + ";";

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
