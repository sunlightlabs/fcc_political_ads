const amile = 1609.344;
var pa_stations_file = 'js/pa_tvstations.js'

var geocoder, map, userLoc, dist_service, dist_results, features;

jQuery(document).ready(function() {
    var gm = google.maps;
    
    var myOptions = {
      center: new gm.LatLng(41.04433523326895, -77.77560713125001),
      zoom: 7,
      mapTypeId: gm.MapTypeId.ROADMAP
    };
    
    geocoder = new gm.Geocoder();
    
    
    map = new gm.Map(document.getElementById("map_canvas"),
        myOptions);
    
/*
    $.getJSON(pa_stations_file, function(data) {
        features = [];
        
        $.each(data['features'], function(key, val) {
            var newMarker = new gm.Marker({
                // 'animation': google.maps.Animation.DROP,
                'map': map,
                'position': new gm.LatLng(val['geometry'][1], val['geometry'][0])
            });
            newMarker.setTitle(val['properties']['combined_address_studio']);
            val['marker'] = newMarker;
            features.push(val);
            $("#locations ul").append("<li id='" + val['properties']['tv_station'].toLowerCase() + "'><h3 class='station'>" + val['properties']['tv_station'] + "</h3><address>" + val['properties']['combined_address_studio'] + "</address></li>");
            all_destinations = jQuery.map(features, function(val, i) { return val['marker'].getPosition()});
            var num_sets = Math.ceil(all_destinations.length/25);
            dest_sets = []
            for (var i=0; i < num_sets; i++) {
                dest_sets[i] = all_destinations.splice(0,25);
            };
            
          });
    });
*/
    
    $("form#map_form").submit(function(event) {
        var address = $("form#map_form input:first").val();
        
        geocoder.geocode( { 'address': address}, function(results, status) 
        {
            dist_results = [];
            if (status == gm.GeocoderStatus.OK) 
            {
                // dest_sets = [all_destinations.splice(0,25),  all_destinations];
                userLoc = results[0].geometry.location;
                map.setCenter(userLoc);
                var marker = new gm.Marker({
                    map: map,
                    position: userLoc
                });
                                
                dist_service.getDistanceMatrix(
                  {
                    origins: [userLoc],
                    destinations: dest_sets[0],
                    travelMode: google.maps.TravelMode.DRIVING,
                    avoidHighways: false,
                    avoidTolls: false
                  }, dist_callback);
                
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
