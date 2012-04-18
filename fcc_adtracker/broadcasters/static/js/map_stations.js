const amile = 1609.344;

var SLL = {
    geocoder: null,
    map: null,
    markers: null,
    searchLoc: null,
    nearby: null
};

jQuery(document).ready(function() {
    var gm = google.maps;
    var myOptions = {
      center: new gm.LatLng(startPos[1], startPos[0]),
      zoom: 8,
      mapTypeId: gm.MapTypeId.ROADMAP
    };
    
    SLL.geocoder = new gm.Geocoder();
    SLL.map = new gm.Map(document.getElementById("map_canvas"), myOptions);
    SLL.markers = {};
    
    var locations_list = $("ul#locations");
    
    SLL.removeStationMarkers = function () {
        for each( mkr in SLL.markers) { mkr.setMap(); }
        SLL.markers = {};
    }
    
    SLL.attachInfoWindow = function (marker, content) {
        var infowindow = new gm.InfoWindow({
            content: content
        });
        gm.event.addListener(marker, 'click', function() {
            infowindow.open(marker.get('map'), marker);
        });
    }
    
    SLL.updateMapApp = function (location_list) {
        SLL.removeStationMarkers();
        locations_list.empty();
        var mapBounds = new gm.LatLngBounds();
        for (var i=0; i < location_list.length; i++) {
            var element = location_list[i];
            var pos = (element['addresses']['studio'] && element['addresses']['studio']['pos']) ? element['addresses']['studio']['pos'] : null;
            if (pos !== null) {
                var marker = new gm.Marker({
                    map: SLL.map,
                    position:  new gm.LatLng(pos[1], pos[0])
                });
                SLL.markers[element.callsign] = marker;
                marker.setTitle(element.callsign);
                SLL.attachInfoWindow(marker, element.html);
                mapBounds.extend(marker.getPosition());
            };
            var elem = $('<li>' + element.html + '</li>');
            if (element.distance) {
                elem.append('<p class="distance">' + element.distance + ' miles (approx.)</p>');
            }
            locations_list.append(elem);
        };
        SLL.map.fitBounds(mapBounds);
    }
    
    SLL.handleNearbySuccess = function(data, textStatus) {
        console.log(textStatus);
        nearby = data;
        SLL.updateMapApp(nearby);
    }
    
    SLL.handleNearbyComplete = function(jqXHR, textStatus) {
        if (window.console) { console.log('handleNearbyComplete: ' + textStatus); }
    }
    
    
    try {
        SLL.updateMapApp(locations);
    }
    catch (e if e instanceof ReferenceError) {
        if (window.console) console.log(e);
    }


    $("form#map_form").submit(function(event) {
        var address = $("form#map_form input#address").val();
        SLL.geocoder.geocode( {'address': address}, function(results, status) 
        {
            if (status == gm.GeocoderStatus.OK) 
            {
                SLL.searchLoc = results[0].geometry.location;
                SLL.map.setCenter(SLL.searchLoc);
                var marker = new gm.Marker({
                    map: SLL.map,
                    position: SLL.searchLoc
                });
                marker.setTitle(address);
                var radius = $("form#map_form select#radius").val();
                
                $.ajax({
                    url: '/broadcasters/nearby.json',
                    dataType: 'json',
                    data: {'lon': SLL.searchLoc.lng(), 'lat': SLL.searchLoc.lat(), 'radius': radius},
                    success: SLL.handleNearbySuccess,
                    complete: SLL.handleNearbyComplete
                });
                
                                
                // dist_service.getDistanceMatrix(
                //   {
                //     origins: [searchLoc],
                //     destinations: dest_sets[0],
                //     travelMode: google.maps.TravelMode.DRIVING,
                //     avoidHighways: false,
                //     avoidTolls: false
                //   }, dist_callback);
                
            } else {
                if(console) console.log("Geocode was not successful for the following reason: " + status);
            }
        });
        
        return false;
    });
    
/*
    dist_service = new gm.DistanceMatrixService();
    function dist_callback(response, status) {
        if (status == gm.DistanceMatrixStatus.OK) {
            var origins = response.originAddresses;
            var destinations = response.destinationAddresses;

            for (var i = 0; i < origins.length; i++) {
                var results = response.rows[i].elements;
                for (var j = 0; j < results.length; j++) {
                    var element = results[j];
                    var distance = element.distance.text;
                    var duration = element.duration.text;
                    var from = origins[i];
                    var to = destinations[j];
                    dist_results.push(element);
                    if (console) {
                        console.log(to + ' ' + element.distance.value/amile + ' miles: ' + duration);
                    };
                }
            }
        }
    }
*/
});