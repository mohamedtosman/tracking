$(document).ready(function() {
    // Initialize the map on the "map" div with the center of the boundary cirle
    var map = L.map('map').setView([52.53, 13.403], 13);
    map.zoomControl.setPosition('bottomright');

    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}{r}.png?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery &copy; <a href="http://mapbox.com">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox.streets-basic',
        accessToken: mapbox_key
    }).addTo(map);

    // Display a cirle that defines the given boundaries in the project outline
    L.circle([52.53, 13.403], {
        color: '#000000',
        opacity: 5,
        fillOpacity: 0.2,
        radius: 3500,
        interactive: false
    }).addTo(map);

    // Initialize an icon for the marker that display moving vehicle
    var icon = L.divIcon({
        iconSize: [20, 20],
        iconAnchor: [12, 12],
        popupAnchor: [0, -6],
        className: 'icon'
    })

    // Initialize a cluster that holds multiple entries of markers of vehicles
    var clusterMarkers = L.markerClusterGroup({
        disableClusteringAtZoom: 14,
        spiderfyOnMaxZoom: false
    });
    map.addLayer(clusterMarkers);

    /*************************************************************************/
    /*************************************************************************/
    /*************************************************************************/
    /*************************************************************************/

    var markers = {};
    var namespace = '/vehicles';

    // Initialize a websocket connection
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

    // Verify our websocket connection is established
    socket.on('connect', function() {
        socket.emit('connected');
    });

    // Update vehicle markers whenever this socket is hit
    socket.on('update_location', function(data) {
        if (data.vehicle_id in markers) {
            var oldLatlgn = markers[data.vehicle_id].getLatLng()
            var newLatLng = new L.LatLng(data.lat, data.lng);
            var bearing = L.GeometryUtil.bearing(oldLatlgn, newLatLng)
            markers[data.vehicle_id].setLatLng(newLatLng);
            markers[data.vehicle_id].options.rotationAngle = bearing + 135;
        }
        else {
            markers[data.vehicle_id] = L.marker([data.lat, data.lng], {
                icon: icon,
                rotationAngle: -45
            }).bindPopup(data.vehicle_id);
            clusterMarkers.addLayer(markers[data.vehicle_id]);
        }
    });

    // Remove vehicle markers when they exit the city boundaries
    socket.on('deregister-vehicle', function(data) {
        if (data.vehicle_id in markers) {
            clusterMarkers.removeLayer(markers[data.vehicle_id]);
        }
    });
});
