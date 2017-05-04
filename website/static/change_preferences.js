'use strict';
window.onload = function() {
var empid = document.getElementById("emp");
$.getJSON('http://moneteam-1.csse.rose-hulman.edu:5000/change_preferences/'+empid.innerHTML, {}, function(preferences) {
console.log(preferences);
preferences.forEach(function(preference) {
    var x = preference['day'] + "." + preference['hour'];
    var element = document.getElementById(x.toString());
    element.innerHTML = '<input type="checkbox">';
    element.onchange = function() {
	console.log("On Change" + x);
    } }); });

}
