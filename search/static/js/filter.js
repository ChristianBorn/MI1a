

function getFilter(){
    var x = "";

    var i = 1;

    while (i <= 33) {

        var filter_id = i.toString();
        if (document.getElementById(filter_id).checked == true){
        console.log(document.getElementById(filter_id).value);
        x = document.getElementById(filter_id).value;
        break;
        } else {
            var i = i +1;
        }
    }

    return x;
}

function getMin(){
    var umrkeis = "";
    var umkreis = document.getElementById("min").value;
    return umkreis;
}

function getMax(){
    var umkreis = "";
    var umkreis = document.getElementById("max").value;
    return umkreis;
}

function addFilter() {
    console.log(getMin());
    console.log(getMax());
    console.log(getFilter());
    document.getElementById("markedFilter").value += getFilter() + ": " + getMin() + ", " + getMax() + "; ";

}