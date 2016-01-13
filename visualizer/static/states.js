$(document).ready(function() {
    getStates()
    setInterval(function() {
        getStates()
    }, 250)
})

function getStates() {
    jQuery.ajax({
        url: '/state/',
        success: function (data) {
            json = JSON.parse(data)
            $("#occupied").html(json.occupied)
            $("#free").html(json.free)
            $("#reserved").html(json.reserved)
        },
        async: false
    });
}