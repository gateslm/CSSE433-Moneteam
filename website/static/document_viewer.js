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
                var current = res[y];
                var elementDiv = document.createElement("div");
                elementDiv.innerHTML = current[2];
                elementDiv.style="display:inline;border-style:solid;border-width:medium;padding:2px";

                var form = document.createElement("form");
                form.target = "_blank";
                form.method = "post";
                form.style="display: inline;";

                var form_input = document.createElement("input");
                form_input.type = "submit";
                form_input.value = "View Document";

                var form_hidden = document.createElement("input");
                form_hidden.type = "hidden";
                form_hidden.name = "ObjectID";
                form_hidden.value = current[1];
                form.appendChild(form_hidden);
                form.appendChild(form_input);
                form.action = "/get_a_document";

                var form_delete = document.createElement("form");
                form_delete.method = "post";
                form.style="display:inline;";

                var form_delete_input = document.createElement("input");
                form_delete_input.type = "submit";
                form_delete_input.value = "Delete Document (No Undo)";

                var form_delete_empid = document.createElement("input");
                form_delete_empid.type = "hidden";
                form_delete_empid.name = "empid";
                form_delete_empid.value = empid;

                var form_delete_hidden = document.createElement("input");
                form_delete_hidden.type = "hidden";
                form_delete_hidden.name = "ObjectID";
                form_delete_hidden.value = current[1];

                form_delete.appendChild(form_delete_empid);
                form_delete.appendChild(form_delete_hidden);
                form_delete.appendChild(form_delete_input);

                form_delete.action = "/delete_document";

                elementDiv.append(form_delete);
                elementDiv.appendChild(form);
                docDiv.appendChild(elementDiv);
           }
            });
    }
