
function getTable(selector, url) {
    $.get(url, function(data) {
        var json = JSON.parse(data)
        var table = createTable(json)
        $(selector).html(table, "data")
    })
}

function getAllTables(callback) {
    var json;
    jQuery.ajax({
        url: '/api/sqlite_sequence',
        success: function (data) {
            json = JSON.parse(data)
        },
        async: false
    });
    return json;
}

function showTables(json) {
    for (var k in json) {
        var name = json[k].name
        appendTable("#tables", name)
    }
}

function clearTables() {
    $("#tables").html("")
}

$(document).ready(function() {
    appendTable("#tables", 'billing')
    setInterval(function() {
        repopulateTable('billing')
    }, 1000)

})

function appendTable(target, name) {
    jQuery.ajax({
        url: '/billing/',
        success: function (data) {
            var json = JSON.parse(data)
            var title = "<h3 data-title='" + name + "'>" + name + " (" + json.length + ")" + "</h3>\n<hr>\n"
            var table = createTable(name, json)
            $(target).append(title + table)
        },
        async: false
    });
}

function repopulateTable(name) {
    jQuery.ajax({
        url: '/billing/',
        success: function (data) {
            var json = JSON.parse(data)
            $("[data-title='" + name + "']").html(name + " (" + json.length + ")")
            var rows = $("[data-name='" + name + "'] tbody").find("tr")

            // Update existing rows
            for (var j = 0; j < rows.length && j < json.length; j++) {
                var obj = json[j]
                var row = ""
                for(var k in obj) {
                    row += "<td> " + obj[k] + " </td>\n"
                }
                $(rows[j]).html(row)
            }

            // Handle remaining rows
            if (rows.length > json.length) {
                for (var j = json.length; j < rows.length; j++) {
                    $(rows[j]).remove()
                }
            }

            // Handle remaining data
            if (json.length > rows.length) {
                for (var j = rows.length; j < json.length; j++) {
                    var obj = json[j]
                    var row = "<tr>\n"
                    for(var k in obj) {
                        row += "<td> " + obj[k] + " </td>\n"
                    }
                    row += "</tr>\n"
                    $("[data-name='" + name + "'] tbody").append(row)
                }
            }
        },
        async: false
    });
}

function createTable(name, json, tableClass) {
    if (json.length == 0)
        return "<span class='faded'>No data available</span>"

    var table = "<table data-name='" + name + "' class='" + tableClass + "'>\n"

    // Table head
    var thead = "\t<thead>\n"
    for (var k in json[0]) {
        thead += "\t\t<th>" + k + "</th>\n"
    }
    thead += "\t</thead>\n"

    // Table body
    var tbody = "\t<tbody>\n"
    for(var i = 0; i < json.length; i++) {
        var obj = json[i]
        var row = "\t\t<tr>\n"
        for(var k in obj) {
            row += "\t\t\t<td> " + obj[k] + " </td>\n"
        }
        row += "\t\t</tr>\n"
        tbody += row
    }

    // Concatenating
    tbody += "\t</tbody>\n"
    table += thead + tbody + "</table>"

    return table
}