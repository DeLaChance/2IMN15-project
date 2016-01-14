$(document).ready(function() {
    var tables = getAllTables()
    for (var table in tables) {
        var api = "/api/tables/" + tables[table].name
        var name = tables[table].name.capitalizeFirst()
        createTableContainer('#tables', api, name)
    }
    setInterval(function() {
        $('.table-container').each(function(i, elem) {
            repopulateTable(elem)
        })
    }, 1000)
})