'use strict';

$.getJSON('http://localhost:5000/change_preferences', {}, function(preferences) {
console.log(preferences);
preferences.forEach(function(preference) {
    var x = preference['day'] + "." + preference['hour'];
    var element = document.getElementById(x.toString());
    element.innerHTML = '<input type="checkbox">';
    element.onchange = function() {
	console.log("On Change" + x);
    } }); });
