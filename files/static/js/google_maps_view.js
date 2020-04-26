
function initMap() {
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 30,
        center: { lat: -33.9, lng: 151.2 }
    });
    setMarkers(map);
}

var data = {{data_for_js  | safe }};

function setMarkers(map) {

    for (var i = 0; i < data.length; i++) {
        var el = data[i];
        var marker = new google.maps.Marker({
            position: { lat: el[1], lng: el[2] },
            map: map,
            title: el[0],
        });
    }
}