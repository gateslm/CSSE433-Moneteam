'use strict';

var preferences = [
    {
	"week_id": 1,
	"day": 1,
	"hour": 9
    }
];

preferences.forEach(function(preference) {
    var element = document.getElementById(preference['day'] + "." + preference['hour']);
    element.innerHTML = '<input type="checkbox">';
    element.onchange = function() {
	console.log("On Change" + preference['day'] + " " + preference['hour']);
    }
});
