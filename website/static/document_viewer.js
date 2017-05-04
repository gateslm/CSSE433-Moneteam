'use strict';

var empid;

window.onload = function() {
    empid = document.getElementById("emp").innerHTML;
    loadDocuments();
}


function loadDocuments() {
    var docDiv = document.getElementById("documentViewer");
    $.getJSON(
        'http://moneteam-1.csse.rose-hulman.edu:5000/get_document_list/' +
        empid, {}, function(data) {
            console.log(data);

        });
}
