var option_div = document.getElementById("option_div");

var result_area;
var option_div;
var add_author_div;
var result_desc;
var delete_book_drop;
var trackBookToUser;
var addBorrowerDiv;
var trackBookCount;
var deleteBorrowerDrop;
var editBookDiv;
var bookCheckOut;
var bookReturn;
var editBorrowerDiv;

window.onload = function() {
    // Book button
    var add_book_button = document.getElementById("add_book");
    add_book_button.onmousedown = addBook;
    var delete_book_button = document.getElementById("delete_book");
    delete_book_button.onmousedown = deleteBook;
    var edit_book_button = document.getElementById("edit_book");
    edit_book_button.onmousedown = editBook;
    // var remove_attr_book = document.getElementById("remove_attribute");
    // remove_attr_book.onmousedown = removeAttr;
    var search_book_button = document.getElementById("search_button");
    search_book_button.onmousedown = searchBook;
    var sort_book_button = document.getElementById("sort_button");
    sort_book_button.onmousedown = sortBook;

    // Borrower button
    var add_borrower_button = document.getElementById("add_borrower");
    add_borrower_button.onmousedown = addBorrower;
    var delete_borrower_button = document.getElementById("delete_borrower");
    delete_borrower_button.onmousedown = deleteBorrower;
    var edit_borrower_button = document.getElementById("edit_borrower");
    edit_borrower_button.onmousedown = editBorrower;
    var search_borrower_button = document
        .getElementById("borrower_search_button");
    search_borrower_button.onmousedown = searchBorrower;

    // Track buttons
    var borrower_checkout_button = document.getElementById(
        "borrower_checkout");
    borrower_checkout_button.onmousedown = borrowerCheckout;
    var book_user_button = document.getElementById("book_to_user");
    book_user_button.onmousedown = bookUserCheckout;

    // Original button
    var originalButton = document.getElementById("show_original_menu");
    originalButton.onmousedown = showOriginal;
    document.getElementById("add_book_final").onmousedown = completeBook;

    // Global variables
    result_area = document.getElementById("results");
    option_div = document.getElementById("option_div");
    add_author_div = document.getElementById("add_author_div");
    result_desc = document.getElementById("result_desc");
    delete_book_drop = document.getElementById("delete_book_drop");
    trackBookToUser = document.getElementById("track_book_to_user");
    addBorrowerDiv = document.getElementById("add_borrower_div");
    trackBookCount = document.getElementById("track_book_count");
    deleteBorrowerDrop = document.getElementById("delete_borrower_drop");
    editBookDiv = document.getElementById("edit_book_div");
    bookCheckOut = document.getElementById("book_check_out_div");
    bookReturn = document.getElementById("book_return_div");
    editBorrowerDiv = document.getElementById("edit_borrower_div");

    editBorrowerDiv.style.visibility = 'hidden';
    editBorrowerDiv.style.display = 'none';

    bookCheckOut.style.visibility = 'hidden';
    bookCheckOut.style.display = "none";

    bookReturn.style.visibility = 'hidden';
    bookReturn.style.display = "none";

    editBookDiv.style.visibility = 'hidden';
    editBookDiv.style.display = 'none';

    result_area.style.visibility = 'hidden';

    add_author_div.style.visibility = 'hidden';
    add_author_div.style.display = 'none';

    delete_book_drop.style.visibility = 'hidden';
    delete_book_drop.style.display = 'none';

    trackBookToUser.style.visibility = 'hidden';
    trackBookToUser.style.display = 'none';

    addBorrowerDiv.style.visibility = 'hidden';
    addBorrowerDiv.style.display = 'none';

    trackBookCount.style.visibility = 'hidden';
    trackBookCount.style.display = 'none';

    deleteBorrowerDrop.style.visibility = 'hidden';
    deleteBorrowerDrop.style.display = 'none';
}

function showOriginal(e) {


    editBorrowerDiv.style.visibility = 'hidden';
    editBorrowerDiv.style.display = 'none';

    document.getElementById("edit_borrower_drop_select").innerHTML =
        '<option value="none" selected>None</option>';

    document.getElementById("title_edit").value = "";
    document.getElementById("authors_edit").value = "";
    document.getElementById("pages_edit").value = "";

    result_area.style.visibility = 'hidden';

    option_div.style.visibility = 'visible';
    option_div.style.display = 'block';

    add_author_div.style.visibility = 'hidden';
    add_author_div.style.display = 'none';

    result_desc.innerHTML = "";

    delete_book_drop.style.visibility = 'hidden';
    delete_book_drop.style.display = 'none';

    trackBookToUser.style.visibility = 'hidden';
    trackBookToUser.style.display = 'none';

    trackBookCount.style.visibility = 'hidden';
    trackBookCount.style.display = 'none';

    addBorrowerDiv.style.visibility = 'hidden';
    addBorrowerDiv.style.display = 'none';

    deleteBorrowerDrop.style.visibility = 'hidden';
    deleteBorrowerDrop.style.display = 'none';

    document.getElementById("delete_book_drop_select").innerHTML =
        '<option value="none" selected>None</option>';
		
	document.getElementById("delete_borrower_drop_select").innerHTML =
        '<option value="none" selected>None</option>';
    document.getElementById("track_book_to_user_select").innerHTML = "";

    document.getElementById("edit_book_drop_select").innerHTML =
        '<option value="none" selected>None</option>';

    document.getElementById("book_checkout_user_select").innerHTML =
        '<option value="none" selected>None</option>';

    document.getElementById("book_to_checkout_select").innerHTML =
        '<option value="none" selected>None</option>';

    document.getElementById("book_to_return_select").innerHTML =
        '<option value="none" selected>None</option>';

    bookCheckOut.style.visibility = 'hidden';
    bookCheckOut.style.display = "none";

    bookReturn.style.visibility = 'hidden';
    bookReturn.style.display = "none";

    editBookDiv.style.visibility = 'hidden';
    editBookDiv.style.display = 'none';
}

function addBook(e) {
    // Complete
    result_area.style.visibility = 'visible';
    option_div.style.visibility = 'hidden';
    option_div.style.display = 'none';
    add_author_div.style.visibility = 'visible';
    add_author_div.style.display = 'block';
}

function deleteBook(e) {
    result_area.style.visibility = 'visible';
    option_div.style.visibility = 'hidden';
    option_div.style.display = 'none';
    delete_book_drop.style.visibility = 'visible';
    delete_book_drop.style.display = 'block';
    $(function() {
        $.getJSON("http://localhost:5000/get_book_isbn", {}, function(
            data) {
            var book_drop = document.getElementById(
                "delete_book_drop_select");
            for (var y = 0; y < data.result.length; y++) {
                book_drop.options[book_drop.options.length] =
                    new Option(data.result[y], data.result[y]);
            }
            var book_delete_confirm = document.getElementById(
                "book_delete_button");
            book_delete_confirm.onmousedown =
                deleteBookWithISBN;
        });
    });
}

function deleteBorrower(e) {
    // Completed
    result_area.style.visibility = 'visible';
    option_div.style.visibility = 'hidden';
    option_div.style.display = 'none';
    deleteBorrowerDrop.style.visibility = 'visible';
    deleteBorrowerDrop.style.display = 'block';
    $(function() {
        $.getJSON("http://localhost:5000/get_borrowers_username", {},
            function(data) {
                var borrower_drop = document.getElementById(
                    "delete_borrower_drop_select");
                for (var y = 0; y < data.result.length; y++) {
                    borrower_drop.options[borrower_drop.options.length] =
                        new Option(data.result[y], data.result[y]);
                }
                var borrower_delete_confirm = document.getElementById(
                    "delete_borrower_drop_button");
                borrower_delete_confirm.onmousedown = function(e) {
                    var selectedDelete = document.getElementById(
                        "delete_borrower_drop_select").value;
                    console.log(selectedDelete);
                    if (selectedDelete == "none") {
                        alert("Select a borrower to delete");
                    } else {
                        $(function() {
                            $.getJSON(
                                "http://localhost:5000/delete_borrower/" +
                                selectedDelete, {},
                                function(data) {
                                    alert(data.result);
                                    if (data.result ==
                                        'Deleted borrower'
                                    ) {
                                        document.getElementById(
                                                "delete_borrower_drop_select"
                                            ).innerHTML =
                                            '<option value="none" selected>None</option>';
                                        showOriginal
                                            (e);
                                    }
                                });
                        });
                    }
                };
            });
    });
}

function deleteBookWithISBN(e) {
    // Complete
    var selectedDelete = document.getElementById("delete_book_drop_select").value;
    console.log(selectedDelete);
    if (selectedDelete == "none") {
        alert("Select a book to delete");
    } else {
        $(function() {
            $.getJSON("http://localhost:5000/delete_book/" +
                selectedDelete, {},
                function(data) {
                    alert(data.result);
                    if (data.result == 'Deleted book') {
                        document.getElementById(
                                "delete_book_drop_select").innerHTML =
                            '<option value="none" selected>None</option>';
                        showOriginal(e);
                    }
                });
        });
    }
}

function editBook(e) {
    // Completed
    result_area.style.visibility = 'visible';
    option_div.style.visibility = 'hidden';
    option_div.style.display = 'none';
    editBookDiv.style.visibility = 'visible';
    editBookDiv.style.display = 'block';
    $(function() {
        $.getJSON("http://localhost:5000/get_book_isbn", {}, function(
            data) {
            var book_edit = document.getElementById(
                "edit_book_drop_select");
            for (var y = 0; y < data.result.length; y++) {
                (book_edit.options[book_edit.options.length] =
                    new Option(data.result[y], data.result[y]))
                .setAttribute("onmousedown", "fillEditFields()");
            }
        });
    });
}

function editBorrower(e) {
    // Completed
    result_area.style.visibility = 'visible';
    option_div.style.visibility = 'hidden';
    option_div.style.display = 'none';
    editBorrowerDiv.style.visibility = 'visible';
    editBorrowerDiv.style.display = 'block';
    $(function() {
        $.getJSON("http://localhost:5000/get_all_borrowers_usernames", {},
            function(data) {
                var borrower_edit = document.getElementById(
                    "edit_borrower_drop_select");
                console.log(data.result);
                for (var y = 0; y < data.result.length; y++) {
                    (borrower_edit.options[borrower_edit.options.length] =
                        new Option(data.result[y], data.result[y])
                    ).setAttribute
                        ("onmousedown", "fillEditBorrowerFields()");
                }
            });
    });

}



function checkoutBookForBorrower() {
    result_area.style.visibility = 'visible';
    option_div.style.visibility = 'hidden';
    option_div.style.display = 'none';
    bookCheckOut.style.visibility = 'visible';
    bookCheckOut.style.display = "block";
    var bookCheckoutUserSelect = document.getElementById(
        "book_checkout_user_select");
    var bookToCheckoutSelect = document.getElementById(
        "book_to_checkout_select");

    $(function() {
        $.getJSON('http://localhost:5000/get_all_borrowers_usernames', {},
            function(data) {
                for (var i = 0; i < data.result.length; i++) {
                    bookCheckoutUserSelect.options[
                            bookCheckoutUserSelect.options.length] =
                        new Option(data.result[i], data.result[i]);
                }
            });
        $.getJSON('http://localhost:5000/get_book_isbn', {}, function(
            data) {
            for (var j = 0; j < data.result.length; j++) {
                bookToCheckoutSelect.options[
                        bookToCheckoutSelect.options.length] =
                    new Option(data.result[j], data.result[j]);
            }
        });
    });
}

function returnBookFromBorrower() {
    result_area.style.visibility = 'visible';
    option_div.style.visibility = 'hidden';
    option_div.style.display = 'none';
    bookReturn.style.visibility = 'visible';
    bookReturn.style.display = "block";


    var returnBookSelect = document.getElementById("book_to_return_select");
    $(function() {
        $.getJSON('http://localhost:5000/get_books_checked_out', {},
            function(data) {
                for (var i = 0; i < data.result.length; i++) {
                    returnBookSelect.options[
                            returnBookSelect.options.length] =
                        new Option(data.result[i], data.result[i]);
                }
            });
    });
}

function returnFinalBook() {
    var returnBookSelect = document.getElementById("book_to_return_select");
    if (returnBookSelect.value == "none") {
        alert("Field not selected");
    } else {
        $(function() {
            $.getJSON("http://localhost:5000/borrower_return/" +
                returnBookSelect.value.split(",")[1] + "/" +
                returnBookSelect.value.split(",")[0], {},
                function(data) {
                    alert("Book returned out");
                    showOriginal(null);
                });
        });
    }
}


// ----------------------------------------------------------------------------------------

function checkOutFinalBook() {
    var bookCheckoutUserSelect = document.getElementById(
        "book_checkout_user_select");
    var bookToCheckoutSelect = document.getElementById(
        "book_to_checkout_select");
    if (bookToCheckoutSelect.value == "none" || bookCheckoutUserSelect.value ==
        "none") {
        alert("Field(s) not selected");
    } else {
        $(function() {
            $.getJSON("http://localhost:5000/borrower_checkout/" +
                bookCheckoutUserSelect.value + "/" +
                bookToCheckoutSelect.value, {},
                function(data) {
                    alert("Book checked out");
                    showOriginal(null);
                });
        });
    }
}


function fillEditBorrowerFields() {
    // Completed
    var selectedValueToEdit = document.getElementById(
        "edit_borrower_drop_select").value;
    $(function() {
        $.getJSON("http://localhost:5000/get_edit_borrower/" +
            selectedValueToEdit, {},
            function(data) {
                var n = document.getElementById("name_edit");
                var a = document.getElementById("phone_edit");
                n.value = "";
                a.value = "";
                n.value = data.result[0];
                a.value = data.result[1];
                document.getElementById("edit_borrower_final").onmousedown =
                    function(e) {
                        var nv = n.value;
                        var phone_value = a.value;
                        if (nv.trim() != "" && phone_value.trim() !=
                            "") {
                            $(function() {
                                $.getJSON(
                                    'http://localhost:5000/commit_edit_borrower/' +
                                    selectedValueToEdit +
                                    '/' + nv + '/' +
                                    phone_value, {},
                                    function(data) {
                                        if (data.Updated_count ==
                                            1) {
                                            alert(
                                                "Borrower updated"
                                            );
                                            n.value =
                                                "";
                                            a.value =
                                                "";
                                            document.getElementById(
                                                    "edit_borrower_drop_select"
                                                ).value =
                                                'none';
                                            showOriginal
                                                (e);
                                        } else {
                                            alert(
                                                "Error updating document. Number of documents updated: " +
                                                data
                                                .Updated_count
                                            );
                                        }
                                    });
                            });
                        } else {
                            alert(
                                "Field(s) are empty. All fields must be filled"
                            );
                        }
                    };
            });
    });
}

function fillEditFields() {
    // Completed
    var selectedValueToEdit = document.getElementById("edit_book_drop_select").value;
    $(function() {
        $.getJSON("http://localhost:5000/get_edit_book/" +
            selectedValueToEdit, {},
            function(data) {
                var n = document.getElementById("title_edit");
                var a = document.getElementById("authors_edit");
                var pg = document.getElementById("pages_edit");
                n.value = "";
                a.value = "";
                pg.value = "";
                n.value = data.result[0];
                a.value = data.result[1];
                pg.value = data.result[2];
                document.getElementById("edit_book_final").onmousedown =
                    function(e) {
                        var nv = n.value;
                        var a_list = a.value.split(",");
                        var valid = true;
                        for (var x = 0; x < a_list.length; x++) {
                            a_list[x] = a_list[x].trim();
                            valid = valid && a_list[x].trim() != "";
                        }
                        pgv = pg.value;
                        if (nv.trim() != "" && pgv.trim() != "" &&
                            valid) {
                            $(function() {
                                $.getJSON(
                                    'http://localhost:5000/commit_edit_book/' +
                                    selectedValueToEdit +
                                    '/' + nv + '/' +
                                    a_list + '/' + pgv, {},
                                    function(data) {
                                        if (data.Updated_count ==
                                            1) {
                                            alert(
                                                "Book updated"
                                            );
                                            n.value =
                                                "";
                                            a.value =
                                                "";
                                            pg.value =
                                                "";
                                            document.getElementById(
                                                    "edit_book_drop_select"
                                                ).value =
                                                'none';
                                            showOriginal
                                                (e);
                                        } else {
                                            alert(
                                                "Error updating document. Number of documents updated: " +
                                                data
                                                .Updated_count
                                            );
                                        }
                                    });
                            });
                        } else {
                            alert(
                                "Field(s) are empty. All fields must be filled"
                            );
                        }
                    };
            });
    });
}

function removeAttr(e) {
    result_area.style.visibility = 'visible';
    option_div.style.visibility = 'hidden';
    option_div.style.display = 'none';
    alert("Remove book attr");
}

function searchBook(e) {
    // Complete
    result_area.style.visibility = 'visible';
    option_div.style.visibility = 'hidden';
    option_div.style.display = 'none';
    var selectSearch = document.getElementById("book_search_select").value;
    var searchValue = document.getElementById("book_search_input").value;
    $(function() {
        $.getJSON('http://localhost:5000/search_book/' + selectSearch +
            '/' +
            searchValue, {},
            function(data) {
                return displaySearchResults(data);
            });
        return "hi";
    });
}

function displaySearchResults(data) {
    // Complete
    result_desc.innerHTML = "<pre>" + data.final.replace(/u'/g, "'").replace(
        /},/g, "},\n") + "</pre>";
}

function sortBook(e) {
    // Complete
    result_area.style.visibility = 'visible';
    option_div.style.visibility = 'hidden';
    option_div.style.display = 'none';
    var selected = document.getElementById("book_sort_select").value;
    $(function() {
        $.getJSON("http://localhost:5000/sort_book/" + selected, {},
            function(data) {
                displaySearchResults(data);
            });
    });
}

function addBorrower(e) {
    result_area.style.visibility = 'visible';
    option_div.style.visibility = 'hidden';
    option_div.style.display = 'none';
    addBorrowerDiv.style.visibility = 'visible';
    addBorrowerDiv.style.display = 'block';
    document.getElementById("add_borrower_final").onmousedown = function(e) {
        var name = document.getElementById("name_add");
        var username = document.getElementById("username_add");
        var phone = document.getElementById("phone_add");
        if (name.value.trim() != "" && username.value.trim() != "" && phone
            .value.trim() != "") {
            $(function() {
                $.getJSON('http://localhost:5000/check_username/' +
                    username.value.trim(), {},
                    function(data) {
                        if (data.result == "true") {
                            $(function() {
                                $.getJSON(
                                    'http://localhost:5000/add_borrower/' +
                                    name.value.trim() +
                                    '/' + username.value
                                    .trim() +
                                    '/' + phone.value
                                    .trim(), {},
                                    function(data) {
                                        console.log(
                                            data
                                            .Insert_output
                                        );
                                    });
                            });
                            showOriginal(e);
                        } else if (data.result == "false") {
                            alert("Username exists");
                        }
                    })
            });
        } else {
            alert("Field(s) are empty. All fields must be filled");
        }
    };
    alert("Add borrower");
}

function searchBorrower(e) {
    // Completed
    result_area.style.visibility = 'visible';
    option_div.style.visibility = 'hidden';
    option_div.style.display = 'none';
    var selectSearch = document.getElementById("borrower_search_select").value;
    var searchValue = document.getElementById("borrower_input").value;
    $(function() {
        $.getJSON('http://localhost:5000/search_borrower/' +
            selectSearch + '/' + searchValue, {},
            function(data) {
                return displaySearchResults(data);
            });
    });
}

function borrowerCheckout(e) {
    result_area.style.visibility = 'visible';
    option_div.style.visibility = 'hidden';
    option_div.style.display = 'none';
    trackBookCount.style.visibility = 'visible';
    trackBookCount.style.display = 'block';

    var track_book_count = document.getElementById("track_book_count_button");

    $(function() {
        $.getJSON('http://localhost:5000/get_users_count', {}, function(
            data) {
            var track_book_count_select = document.getElementById(
                "track_book_count_select");
            for (var y = 0; y < data.result.length; y++) {
                console.log(data.result);
                track_book_count_select.options[
                        track_book_count_select.options.length] =
                    new Option(data.result[y][1], data.result[y]
                        [0]);
            }
            var button = document.getElementById(
                "track_book_count_button");
            button.onmousedown = function(e) {
                if (track_book_count_select.value != "") {
                    alert("Book checked out to: " +
                        track_book_count_select.value);
                }
            };
        });
    });
}


function bookUserCheckout(e) {
    // Complete
    result_area.style.visibility = 'visible';
    option_div.style.visibility = 'hidden';
    option_div.style.display = 'none';
    trackBookToUser.style.display = 'block';
    trackBookToUser.style.visibility = 'visible';

    var track_book_to_userSelect = document.getElementById(
        "track_book_to_user_select");
    $(function() {
        $.getJSON('http://localhost:5000/get_books_checked_out', {},
            function(data) {
                for (var y = 0; y < data.result.length; y++) {
                    track_book_to_user_select.options[
                        track_book_to_user_select.options.length
                    ] = new Option(data.result[y][1], data.result[
                        y][0]);
                }
                var button = document.getElementById(
                    "track_book_to_user_show");
                button.onmousedown = function(e) {
                    if (track_book_to_userSelect.value != "" &&
                        track_book_to_userSelect.value != " ") {
                        console.log(track_book_to_userSelect.value);
                        alert("Book checked out to :" +
                            track_book_to_userSelect.value);
                    }
                };
            });
    });
}

function completeBook(e) {
    // Complete
    var t = document.getElementById("title_add");
    var a = document.getElementById("authors_add");
    var a_list = a.value.split(",");
    var valid = true;
    for (var x = 0; x < a_list.length; x++) {
        a_list[x] = a_list[x].trim();
        valid = valid && a_list[x].trim() != "";
    }
    var i = document.getElementById("isbn_add");
    var p = document.getElementById("pages_add");
    if (t.value.trim() != "" && i.value.trim() != "" && p.value.trim() != "" &&
        valid) {
        $(function() {
            $.getJSON('http://localhost:5000/check_isbn/' + i.value.trim(), {},
                function(data) {
                    if (data.result == "true") {
                        $(function() {
                            $.getJSON(
                                'http://localhost:5000/add_book/' +
                                t.value + '/' + a_list +
                                '/' +
                                i.value + '/' + p.value, {},
                                function(data) {
                                    console.log(data.Insert_output);
                                });
                        });
                        showOriginal(e);
                    } else if (data.result == "false") {
                        alert("ISBN exists");
                    }
                });
            return "failed";
        });
    } else {
        alert("Field(s) are empty. All fields must be filled");
    }
}
