var SLL = {
    geocoder: null,
    map: null,
    markers: null,
    searchLoc: null,
    nearby: null,
    list_elem: null,
    amile: function() { return 1609.344; },
    userMarkerImage: null,
    stationMarkerImage: null
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
    SLL.userMarkerImage = new gm.MarkerImage(userMarker_url, gm.Size(19,32));
    SLL.stationMarkerImage = new gm.MarkerImage(stationMarker_url, gm.Size(19,32));
    
    SLL.list_elem = $("ul#locations");
    
    SLL.removeStationMarkers = function () {
        for each( mkr in SLL.markers) { mkr.setMap(); }
        SLL.markers = {};
    }
    
    SLL.attachInfoWindow = function (marker, content, open) {
        var infowindow = new gm.InfoWindow({ content: content });
        gm.event.addListener(marker, 'click', function() { infowindow.open(marker.get('map'), marker); });
        if (open) { infowindow.open(marker.get('map'), marker); };
    }
    
    SLL.addMarker = function(id, pos, infoContent, markerImage) {
        var marker = new gm.Marker({
            position:  new gm.LatLng(pos[1], pos[0]),
            draggable: false,
            icon: markerImage
        });
        SLL.markers[id] = marker;
        marker.setTitle(id);
        SLL.attachInfoWindow(marker, infoContent);
        return marker;
    };
        
    SLL.revealList = function() {
        console.log('revealList');
        var li_els = SLL.list_elem.children('li');
        $(li_els).each(function(index, element) {
            $(element).delay(index*100).fadeIn('slow');
        });
    };
    
    SLL.revealMarkers = function(callback) {
        for each( mkr in SLL.markers) { 
            mkr.setMap(SLL.map);
        }
        callback();
    };
    
    SLL.updateMapApp = function (location_list) {
        SLL.removeStationMarkers();
        SLL.list_elem.empty();
        var mapBounds = new gm.LatLngBounds();
        for (var i=0; i < location_list.length; i++) {
            var element = location_list[i];
            var pos = (element['addresses']['studio'] && element['addresses']['studio']['pos']) ? element['addresses']['studio']['pos'] : null;
            if (pos !== null) {
                var marker= SLL.addMarker(element.callsign, pos, element.html, SLL.stationMarkerImage);
                mapBounds.extend(marker.getPosition());
            };
            var elem = $('<li>' + element.html + '</li>');
            if (element.distance) {
                elem.append('<p class="distance">' + element.distance + ' miles (approx.)</p>');
            }
            elem.hide();
            SLL.list_elem.append(elem);
            // elem.delay(i*100).fadeIn('slow');
        };
        gm.event.addListenerOnce(SLL.map, 'bounds_changed', function() {
            SLL.revealMarkers(SLL.revealList);    
        });
        SLL.map.fitBounds(mapBounds);
    }
    
    SLL.handleNearbySuccess = function(data, textStatus) {
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
                    position: SLL.searchLoc,
                    icon: SLL.userMarkerImage,
                    animation: gm.Animation.DROP
                });
                SLL.attachInfoWindow(marker, address);
                marker.setTitle(address);
                var radius = $("form#map_form select#radius").val();
                
                $.ajax({
                    url: '/broadcasters/nearby.json',
                    dataType: 'json',
                    data: {'lon': SLL.searchLoc.lng(), 'lat': SLL.searchLoc.lat(), 'radius': radius},
                    success: SLL.handleNearbySuccess,
                    complete: SLL.handleNearbyComplete
                });

             } else {
                if(console) console.log("Geocode was not successful for the following reason: " + status);
            }
        });
        
        return false;
    });

});