
var used_filters = [];


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
                    throw "filter already exists";
                }
            }
        }
        catch (err) {
                alert("Input is " + err);
                }
    }
    else {
        alert("Bitte einen Filter auswählen!");
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


    if (getFilterProof() == ""){
        document.getElementById("markedFilter").value += "";
    }
    else {
        if (getMin() >= getMax()){
            alert("Die Minimale Entfernung muss größer als die Maximale entfernung sein!")
            document.getElementById("markedFilter").value += "";
        }
        else {
            document.getElementById("markedFilter").value += getFilter() + ":" + getMin() + ", " + getMax() + ";";
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
