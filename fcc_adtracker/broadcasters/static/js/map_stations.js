var SLF = {
    geocoder: null,
    map: null,
    markers: null,
    locations: null,
    selectedGeocoderResult: null,
    userMarker: null,
    nearby: null,
    list_elem: null,
    amile: function () { return 1609.344; },
    userMarkerImage: null,
    stationMarkerImage: null,
    currentInfoWindow: null,
    DEBUG: false
};

jQuery(document).ready(function() {
    var gm = google.maps, myOptions = {
        center: new gm.LatLng(startPos[1], startPos[0]),
        zoom: 8,
        mapTypeId: gm.MapTypeId.ROADMAP,
        scaleControl: true
    };
    SLF.geocoder = new gm.Geocoder();
    SLF.map = new gm.Map(document.getElementById("map_canvas"), myOptions);
    SLF.markers = {};
    SLF.userMarkerImage = new gm.MarkerImage(userMarker_url, gm.Size(19, 32));
    SLF.stationMarkerImage = new gm.MarkerImage(stationMarker_url, gm.Size(19, 32));
    SLF.list_elem = $("ul#locations");

    SLF.locations = initialLocations || [];

    SLF.removeStationMarkers = function () {
        for (var key in SLF.markers) { SLF.markers[key].setMap(); }
        SLF.markers = {};
    };
    
    SLF.attachInfoWindow = function (marker, content, open) {
        var infowindow = new gm.InfoWindow({ content: content });
        gm.event.addListener(marker, 'click', function() { 
            if (SLF.currentInfoWindow !== null) SLF.currentInfoWindow.close();
            infowindow.open(marker.get('map'), marker); 
            SLF.currentInfoWindow = infowindow;
        });
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
        var snippet = $('<div class="vcard"></div>');
        snippet.append($('<h5 class="org withTip">').text(element.callsign));
        var dl = $('<dl class="moduleSm floatedList clearfix"></dl>');
        if (element.network_affiliate) dl.append($('<dt>Network:</dt> <dd>' + element.network_affiliate + '</dd>'));
        if (element.channel) dl.append($('<dt>Channel:</dt> <dd>' + element.channel + '</dd>'));
        snippet.append(dl);
        if (element.addresses.length > 1) {
            var addr = $('<div class="adr tip"></div>');
            $('<span class="street-address">').text(element.addresses[1].address1).appendTo(addr);
            if(element.addresses[1].address2) $('<span class="street-address">').text(element.addresses[1].address2).appendTo(addr);
            var city = $('<span class="locality"></span>').text(element.addresses[1].city);
            var state = $('<span class="region"></span>').text(element.addresses[1].state);
            var zip1 = $('<span class="postal-code"></span>').text(element.addresses[1].zip1);
            snippet.append(addr.append(city, ', ', state, ' ', zip1));
        }
        if (element.distance) {
            snippet = snippet.append('<p class="distance">' + Number(element.distance).toPrecision(3) + ' miles (approx.)</p>');
        }
        return snippet[0];
    };
    
    SLF.revealList = function() {
        var li_els = SLF.list_elem.children('li');
        $(li_els).each(function(index, element) {
            $(element).delay(index*100).fadeIn('slow');
        });
    };
    
    SLF.updateStationSelect = function() {
        var station_sel = $('select#station');
        var selected = $('select#station :selected');
        station_sel.empty();
        station_sel.append('<option value="">-----------</option>');
        for (var i=0; i < SLF.locations.length; i++) {
            var opt = $('<option></option>').text(SLF.locations[i].callsign + ' (' + SLF.locations[i].network_affiliate + ')').attr('value', SLF.locations[i].callsign);
            if (selected.val() === opt.val()) opt.attr('selected', 'selected');
            station_sel.append(opt);
        }
    };
    
    SLF.revealMarkers = function(callback) {
        for(var key in SLF.markers) { 
            SLF.markers[key].setMap(SLF.map);
        }
        callback();
    };
    
    SLF.updateMapApp = function () {
        SLF.removeStationMarkers();
        SLF.list_elem.empty();
        var mapBounds = new gm.LatLngBounds();
        if (SLF.userMarker !== null) mapBounds.extend(SLF.userMarker.getPosition());
        for (var i=0; i < SLF.locations.length; i++) {
            var element = SLF.locations[i];
            var pos = (element.addresses[1] && element.addresses[1].pos) ? element.addresses[1].pos : null;
            var descriptionHTML = SLF.generateDescriptionHTML(element);
            if (pos !== null) {
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
        if( SLF.locations.length === 0) SLF.list_elem.append($('<li>').text('No results found with those search parameters!'));
        if (  SLF.locations.length == 1) {  SLF.map.setZoom(12); } else { SLF.map.fitBounds(mapBounds); }
        SLF.updateStationSelect();
    };
    
    SLF.handleNearbySuccess = function(data, textStatus) {
        if (SLF.DEBUG) window.log('handleNearbySuccess: ' + textStatus);
        SLF.locations = data;
        if (SLF.locations instanceof Array) SLF.updateMapApp();
    };
    
    SLF.handleNearbyComplete = function(jqXHR, textStatus) {
        if (SLF.DEBUG) window.log('handleNearbyComplete: ' + textStatus);
    };
    
    SLF.setselectedGeocoderResult = function(location) {
        if (SLF.userMarker !== null) SLF.userMarker.setMap(null);
        SLF.selectedGeocoderResult = location;
        SLF.map.setCenter(SLF.selectedGeocoderResult.geometry.location);
        var marker = new gm.Marker({
            map: SLF.map,
            position: SLF.selectedGeocoderResult.geometry.location,
            icon: SLF.userMarkerImage,
            animation: gm.Animation.DROP
        });
        SLF.attachInfoWindow(marker, SLF.selectedGeocoderResult.formatted_address);
        marker.setTitle(SLF.selectedGeocoderResult.formatted_address);
        SLF.userMarker = marker;
    };
    
    SLF.findNearbyLocations = function() {
        var radius = $("form#map_form select#radius").val();                    
        if (SLF.DEBUG) window.log('SLF.findNearbyLocations with radius: ' + radius);
        $.ajax({
            url: '/broadcasters/nearby.json',
            dataType: 'json',
            data: {'lon': SLF.selectedGeocoderResult.geometry.location.lng(), 'lat': SLF.selectedGeocoderResult.geometry.location.lat(), 'radius': radius},
            success: SLF.handleNearbySuccess,
            complete: SLF.handleNearbyComplete
        });
    };
    
    
    $("form#map_form").submit(function(event) {
        var address = $("form#map_form input#address");
        var city = $("form#map_form input#city");
        var state = $("form#map_form input#state");
        var full_address = address.val() + ' ' + city.val() + ', ' + state.val();
        SLF.geocoder.geocode( {'address': full_address}, function(results, status) 
        {
            if (status == gm.GeocoderStatus.OK) 
            {
                if (SLF.DEBUG) window.log('GeocoderStatus.OK results:');
                if (SLF.DEBUG) window.log(results);
                if (results.length == 1) {
                    SLF.setselectedGeocoderResult(results[0]);
                    SLF.findNearbyLocations();
                }
                else
                {
                    var location_select = $('<ul class="nav nav-list">');
                    for (var i=0; i < results.length; i++) {
                        var anchor = $('<a href="#"></a>').text(results[i].formatted_address);
                        if (SLF.DEBUG) window.log(anchor);
                        $(anchor).data('location', results[i]);
                        location_select.append( $('<li> </li>').append(anchor) );
                    }
                    var modal = $('<div class="modal">');
                    modal.append($('<div class="modal-header">').html('<h3>Multiple results were found, please choose one.</h3>'));
                    var modal_body = $('<div class="modal-body">').html(location_select);
                    modal.append(modal_body);
                    $('body').append(modal);
                    $(modal).modal({'backdrop': false});
                    location_select.on('click', 'li a', function(event) {
                        if (SLF.DEBUG) window.log($(this).data('location'));
                        $(modal).modal('hide').detach();
                        var addr_parts = $(this).data('location').formatted_address.split(',');
                        address.val($.trim(addr_parts[0]));
                        city.val($.trim(addr_parts[1]));
                        SLF.setselectedGeocoderResult($(this).data('location'));
                        SLF.findNearbyLocations();
                        return false;
                    });
                }

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
        SLF.updateMapApp(SLF.locations);
    }
    catch (e) {
        if (SLF.DEBUG) window.log(e);
    }

});