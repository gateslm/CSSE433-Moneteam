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
        empid, {},
        function(data) {
            console.log(data);
            var res = data.res;
            for (var y = 0; y < res.length; y++) {
                current = res[y];
                var elementDiv = document.createElement("div");
                elementDiv.innerHTML = res[2];
                var form = document.createElement("form");
                form.target = "_blank";
                form.method = "get";
                var form_input = document.createElement("input");
                form_input.type = "submit";
                form_input.value = "View Document";
                var form_hidden = document.createElement("input");
                form_hidden.type = "hidden";
                form_hidden.name = "ObjectID";
                form_hidden.value = res[1];
                form.appendChild(form_hidden);
                form.appendChild(form_input);
                form.action = "/get_a_document";
                elementDiv.appendChild(form);
                docDiv.appendChild(elementDiv);

            });
    }
