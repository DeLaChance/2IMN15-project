$(document).ready(function() {
    var api = "/api/billing"
    var name = "Invoices"
    createTableContainer('#tables', api, name)
    setInterval(function() {
        $('.table-container').each(function(i, elem) {
            repopulateTable(elem)
        })
    }, 1000)
})