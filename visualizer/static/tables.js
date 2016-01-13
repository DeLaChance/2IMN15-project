// Extend string with function
String.prototype.capitalizeFirst = function() {
    return this.charAt(0).toUpperCase() + this.slice(1)
}

/** Create table container. */
function createTableContainer(target, api, name) {
    jQuery.ajax({
        url: api,
        success: function (data) {
            var json = JSON.parse(data)
            var wrapperStart = "<div class='table-container' data-api='" + api + "'>";
            var wrapperEnd = "</div>";
            var title = "<h3 data-title='" + name + "'>" + name + " (" + json.length + ")" + "</h3>\n<hr>\n"
            var table = createTable(name, json)
            $(target).append(wrapperStart + title + table + wrapperEnd)
        },
        async: false
    });
}

/** Repopulates table. */
function repopulateTable(container) {
    var container = $(container)
    var api = container.data('api')
    var name = container.data('title')
    jQuery.ajax({
        url: api,
        success: function (data) {
            var json = JSON.parse(data)
            $("[data-title='" + name + "']").html(name + " (" + json.length + ")")
            var rows = container.find("tbody tr")

            // If table does not exist yet
            if (rows.length == 0 && json.length > 0) {
                location.reload()
            }

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

/** Retrieve a list of all table names. */
function getAllTables() {
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

/** Create table from json */
function createTable(name, json) {
    if (json.length == 0)
        return "<span class='faded'>No data available</span>"

    var table = "<table>\n"

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