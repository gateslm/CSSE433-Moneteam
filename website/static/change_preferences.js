'use strict';

$.getJSON('http://moneteam-1.csse.rose-hulman.edu:5000/change_preferences', {}, function(preferences) {

preferences.forEach(function(preference) {
    //console.log(preferences[preference]);
    var x = preference['day'] + "." + preference['hour'];
    console.log(x)
    var element = document.getElementById(x.toString());
    console.log('Element ', element);
    element.innerHTML = '<input type="checkbox">';
    element.onchange = function() {
	console.log("On Change" + preference['day'] + " " + preference['hour']);
    } }); }); )
