function use_maps(params) {
    

var map;
var markersArray = [];
function initialize() {


    function placeMarker(location) {
        // first remove all markers if there are any
        deleteOverlays();

        var marker = new google.maps.Marker({
            position: location,
            map: map
        });

        // add marker in markers array
        markersArray.push(marker);

        map.setCenter(location);
    }

    // Deletes all markers in the array by removing references to them
    function deleteOverlays() {
        if (markersArray) {
            for (i in markersArray) {
                markersArray[i].setMap(null);
            }
            markersArray.length = 0;
        }
    }

    var markers = [];
    var map = new google.maps.Map(document.getElementById('map-canvas'), {
        center: { lat: 50.443207, lng: 30.485513 },
        mapTypeId: google.maps.MapTypeId.ROADMAP,

        disableDefaultUI: true
    });

    // add a click event handler to the map object
    google.maps.event.addListener(map, "rightclick", function (event) {
        // place a marker
        placeMarker(event.latLng);

        // display the lat/lng in your form's lat/lng fields
        document.getElementById("latFld").textContent = event.latLng.lat();
        document.getElementById("lngFld").textContent = event.latLng.lng();
    });


    var defaultBounds = new google.maps.LatLngBounds(
        new google.maps.LatLng(50.3902, 30.0759),
        new google.maps.LatLng(50.4474, 30.2631));
    map.fitBounds(defaultBounds);
}

google.maps.event.addDomListener(window, 'load', initialize);

}