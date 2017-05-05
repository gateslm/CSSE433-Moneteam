'use strict';

var empid;

window.onload = function() {
    empid = document.getElementById("emp");
    checkPreferenceBoxes();
}

function checkPreferenceBoxes() {
    $.getJSON(
        'http://moneteam-1.csse.rose-hulman.edu:5000/change_preferences/' +
        empid.innerHTML, {},
        function(preferences) {
            console.log(preferences);
            preferences.forEach(function(preference) {
                var x = preference['day'] + "." + preference[
                    'hour'];
                var element = document.getElementById(x.toString());
                element.checked = true;
                element.onchange = function() {
                    console.log("On Change" + x);
                }
            });
        });
}

function submitScheduleRequest() {
     // TODO: Do me James!!!
        var days = [1,2,3,4,5,6,7];
	var hours = [8,9,10,11,12,13,14,15,16,17,18,19,20,21];
	var checkedArray = [];
	for (d = 1; d <= 7; d++) {
		for (h = 8; h <= 21; h++) {
			var x = d + "." + h;
			var elem = document.getElementById(x);
			console.log(elem.checked);
			checkedArray.push(elem);
		}
	}


}
