'use strict';

var empid;
var week_num;

window.onload = function() {
    empid = document.getElementById("emp");
    week_num = document.getElementById("week_num");
    checkPreferenceBoxes();
}

function checkPreferenceBoxes() {
    $.getJSON(
        'http://moneteam-1.csse.rose-hulman.edu:5000/change_preferences/' +
        empid.innerHTML, {},
        function(preferences) {
            console.log(preferences);
            preferences.forEach(function(preference) {
                var x = preference['day'] + "." + preference['hour'];
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
	var checkedBoxes = getCheckedSpots();
	console.log(checkedBoxes);
	var jsonPrefs = makeJSONfromIDs(checkedBoxes);
	console.log(jsonPrefs);
        $.getJSON(
            'http://moneteam-1.csse.rose-hulman.edu:5000/save_preferences/' + empid.innerHTML +'/' +
            JSON.stringify(jsonPrefs), {},
            function(data) {
		    console.log("array sent as string");
	    });
}

function getCheckedSpots() {
	var checkedArray = [];
	for (var d = 1; d <= 7; d++) {
		for (var h = 8; h <= 21; h++) {
			var x = d + "." + h;
			var elem = document.getElementById(x);
			console.log(elem.checked);
			if (elem.checked) {
				checkedArray.push(elem);
			}
		}
	}
	return checkedArray;
}

function makeJSONfromIDs(checkedBoxes) {
	var result = [];
	for (var i = 0; i < checkedBoxes.length; i++) {
		var current = {"week_id": week_num};
		current["day"] = parseInt(checkedBoxes[i].id.toString()[0]);
		current["hour"] = parseInt(checkedBoxes[i].id.toString().substring(2));
		//console.log(i,day,hour)
		result.push(current); 
	}
	return result;
}
