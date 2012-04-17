const amile = 1609.344;

var geocoder, map, mapBounds, markers, searchLoc, nearby;

jQuery(document).ready(function() {
    var gm = google.maps;
    
    var myOptions = {
      center: new gm.LatLng(startPos[1], startPos[0]),
      zoom: 7,
      mapTypeId: gm.MapTypeId.ROADMAP
    };
    
    geocoder = new gm.Geocoder();
    markers = [];
    
    map = new gm.Map(document.getElementById("map_canvas"), myOptions);
    mapBounds = new gm.LatLngBounds();
        
    try {
        for (var i = locations.length - 1; i >= 0; i--){
            var newMarker = new gm.Marker({
                // 'animation': google.maps.Animation.DROP,
                'map': map,
                'position': new gm.LatLng(locations[i]['lat'], locations[i]['lon'])
            });
            newMarker.setTitle(locations[i]['title']);
            markers.push(newMarker);
            mapBounds.extend(newMarker.getPosition());
        }
        console.log(mapBounds.getCenter());
        map.fitBounds(mapBounds);
        // map.panBy(-20, 0);
    }
    catch (e if e instanceof ReferenceError) {
        if (window.console) console.log(e);
    }


    $("form#map_form").submit(function(event) {
        var address = $("form#map_form input:first").val();
        
        geocoder.geocode( { 'address': address}, function(results, status) 
        {
            if (status == gm.GeocoderStatus.OK) 
            {
                searchLoc = results[0].geometry.location;
                map.setCenter(searchLoc);
                var marker = new gm.Marker({
                    map: map,
                    position: searchLoc
                });
                
                for (var i=0; i < markers.length; i++) {
                    markers[i].setMap(null);
                };
                $.getJSON('/broadcasters/nearby.json', {'lon': searchLoc.lng(), 'lat': searchLoc.lat()}, function(json, textStatus) {
                    nearby = json;
                    $(json).each(function(index, element) {
                        if (console) console.log(element);
                        var newMarker = new gm.Marker({
                            map: map,
                            position:  new gm.LatLng(element.obj.addresses.studio.pos[1], element.obj.addresses.studio.pos[0])
                        });
                        newMarker.setTitle(element.obj.callsign);
                        markers.push(newMarker);
                    });
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
    
    dist_service = new gm.DistanceMatrixService();
    
    
    function dist_callback(response, status) {
        if (status == google.maps.DistanceMatrixStatus.OK) {
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
});
