var SLF = {
    geocoder: null,
    map: null,
    markers: null,
    searchLoc: null,
    nearby: null,
    list_elem: null,
    amile: function () { return 1609.344; },
    userMarkerImage: null,
    stationMarkerImage: null,
    DEBUG: false
};

jQuery(document).ready(function() {
    var gm = google.maps, myOptions = {
        center: new gm.LatLng(startPos[1], startPos[0]),
        zoom: 8,
        mapTypeId: gm.MapTypeId.ROADMAP
    };
    SLF.geocoder = new gm.Geocoder();
    SLF.map = new gm.Map(document.getElementById("map_canvas"), myOptions);
    SLF.markers = {};
    SLF.userMarkerImage = new gm.MarkerImage(userMarker_url, gm.Size(19, 32));
    SLF.stationMarkerImage = new gm.MarkerImage(stationMarker_url, gm.Size(19, 32));
    SLF.list_elem = $("ul#locations");
    
    SLF.removeStationMarkers = function () {
        for ( var key in SLF.markers) { SLF.markers[key].setMap(); }
        SLF.markers = {};
    };
    
    SLF.attachInfoWindow = function (marker, content, open) {
        var infowindow = new gm.InfoWindow({ content: content });
        gm.event.addListener(marker, 'click', function() { infowindow.open(marker.get('map'), marker); });
        if (open) infowindow.open(marker.get('map'), marker);
    };
    
    SLF.addMarker = function(id, pos, infoContent, markerImage) {
        var marker = new gm.Marker({
            position:  new gm.LatLng(pos[1], pos[0]),
            draggable: false,
            icon: markerImage
        });
        SLF.markers[id] = marker;
        marker.setTitle(id);
        SLF.attachInfoWindow(marker, infoContent);
        return marker;
    };
    
    SLF.generateDescriptionHTML = function(element) {
        var snippet = $('<div></div>');
        snippet.append($('<h3>').text(element.callsign));
        if (element.addresses.length > 1) {
            var addr = $('<div class="postal-address">');
            $("<p>").text(element.addresses[1].address1).appendTo(addr);
            if(element.addresses[1].address2) $("<p>").text(element.addresses[1].address2).appendTo(addr);
            var city = $('<span></span>').text(element.addresses[1].city);
            var state = $('<span></span>').text(element.addresses[1].state);
            var zip1 = $('<span></span>').text(element.addresses[1].zip1);
            $("<p>").append(city.html() + ", " + state.html() + " " + zip1.html()).appendTo(addr);
            snippet.append(addr);
        }
        if (element.distance) {
            snippet = snippet.append('<p class="distance">' + Number(element.distance).toPrecision(3) + ' miles (approx.)</p>');
        }
        return snippet.html();
    };
    
    SLF.revealList = function() {
        var li_els = SLF.list_elem.children('li');
        $(li_els).each(function(index, element) {
            $(element).delay(index*100).fadeIn('slow');
        });
    };
    
    SLF.revealMarkers = function(callback) {
        for(var key in SLF.markers) { 
            SLF.markers[key].setMap(SLF.map);
        }
        callback();
    };
    
    SLF.updateMapApp = function (location_list) {
        SLF.removeStationMarkers();
        SLF.list_elem.empty();
        var mapBounds = new gm.LatLngBounds();
        for (var i=0; i < location_list.length; i++) {
            var element = location_list[i];
            var pos = (element.addresses[1] && element.addresses[1].pos) ? element.addresses[1].pos : null;
            var descriptionHTML = SLF.generateDescriptionHTML(element);
            if (pos !== null) {
                if (SLF.DEBUG) window.log(element.callsign + ' pos ' + pos);
                var marker= SLF.addMarker(element.callsign, pos, descriptionHTML, SLF.stationMarkerImage);
                mapBounds.extend(marker.getPosition());
            }
            var elem = $('<li></li>').append(descriptionHTML);
            elem.hide();
            SLF.list_elem.append(elem);
            // elem.delay(i*100).fadeIn('slow');
        }
        gm.event.addListenerOnce(SLF.map, 'bounds_changed', function() {
            SLF.revealMarkers(SLF.revealList);    
        });
        if ( location_list.length == 1) {  SLF.map.setZoom(12); } else { SLF.map.fitBounds(mapBounds); }
    };
    
    SLF.handleNearbySuccess = function(data, textStatus) {
        nearby = data;
        SLF.updateMapApp(nearby);
    };
    
    SLF.handleNearbyComplete = function(jqXHR, textStatus) {
        if (SLF.DEBUG) window.log('handleNearbyComplete: ' + textStatus);
    };
    
    
    $("form#map_form").submit(function(event) {
        var address = $("form#map_form input#address").val();
        SLF.geocoder.geocode( {'address': address}, function(results, status) 
        {
            if (status == gm.GeocoderStatus.OK) 
            {
                SLF.searchLoc = results[0].geometry.location;
                SLF.map.setCenter(SLF.searchLoc);
                var marker = new gm.Marker({
                    map: SLF.map,
                    position: SLF.searchLoc,
                    icon: SLF.userMarkerImage,
                    animation: gm.Animation.DROP
                });
                SLF.attachInfoWindow(marker, address);
                marker.setTitle(address);
                var radius = $("form#map_form select#radius").val();
                
                $.ajax({
                    url: '/broadcasters/nearby.json',
                    dataType: 'json',
                    data: {'lon': SLF.searchLoc.lng(), 'lat': SLF.searchLoc.lat(), 'radius': radius},
                    success: SLF.handleNearbySuccess,
                    complete: SLF.handleNearbyComplete
                });

             } else {
                if (SLF.DEBUG) window.log("Geocode was not successful for the following reason: " + status);
            }
        });
        
        return false;
    });
    
    /*
        Get to the action.
    */ 
    try {
        SLF.updateMapApp(locations);
    }
    catch (e) {
        if (SLF.DEBUG) window.log(e);
    }

});