document.addEventListener("DOMContentLoaded", () => {
    var name_series = document.querySelector("#nameseries");
    var pos_series = document.querySelector("#posseries");
    var if_series = document.querySelector("#aseries").value;
    name_series.disabled = true;
    pos_series.disabled = true;
    name_series.parentElement.hidden = true;
    pos_series.parentElement.hidden = true;

    if (if_series === "True") {
        pos_series.disabled = false;
        name_series.disabled = false;
        name_series.parentElement.hidden = false;
        pos_series.parentElement.hidden = false;
    }
    
    document.querySelector("#aseries").onchange = function() {
        var selection = this.value
        name_series.disabled = true;
        pos_series.disabled = true;
        name_series.parentElement.hidden = true;
        pos_series.parentElement.hidden = true;
        
        if (selection === "True") {
            pos_series.disabled = false;
            name_series.disabled = false;
            name_series.parentElement.hidden = false;
            pos_series.parentElement.hidden = false;
        } else if (selection === "False") {
            name_series.disabled = true;
            pos_series.disabled = true;
            name_series.parentElement.hidden = true;
            pos_series.parentElement.hidden = true;
        }

    }
})