
function getTable(selector, url) {
    $.get(url, function(data) {
        var json = JSON.parse(data)
        var table = createTable(json)
        $(selector).html(table, "data")
    })
}

function getAllTables(callback) {
    $.get('/api/sqlite_sequence', function(data) {
        var json = JSON.parse(data)
        callback(json)
    })
}

$(document).ready(function() {

    getAllTables(function(json) {
        for (var k in json) {
            var name = json[k].name
            var amount = json[k].seq
            appendTable("#tables", name, amount)
        }
    });
})

function appendTable(target, name, amount) {
    console.log(target, name, amount)
    $.get('/api/' + name, function(data) {
        var json = JSON.parse(data)
        var title = "<h3>" + name + " (" + amount + ")" + "</h3>\n<hr>\n"
        var table = createTable(json)
        $(target).append(title + table)
     })
}

//updateTable('#parkingspots', '/api/parkingspots')
////updateTable('#reservations', '/api/reservations')
//updateTable('#reservations', '/api/null')

function createTable(json, tableClass) {
    if (json.length == 0)
        return "<span class='faded'>No data available</span>"

    var table = "<table class='" + tableClass + "'>\n"

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