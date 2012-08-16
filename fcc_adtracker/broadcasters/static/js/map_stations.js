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
    mapMaxZoom: null,
    userMarkerImage: null,
    stationMarkerImage: null,
    currentInfoWindow: null,
    DEBUG: false
};

jQuery(document).ready(function() {
    SLF.mapMaxZoom = ('mapMaxZoom' in window) ? mapMaxZoom : 14;
    var gm = google.maps, myOptions = {
        center: new gm.LatLng(startPos[1], startPos[0]),
        zoom: 8,
        maxZoom: SLF.mapMaxZoom,
        minZoom: 3,
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
        var bc = element.broadcaster;
        var snippet = $('<div class="vcard"></div>');
        snippet.append($('<h5 class="org withTip"></h5>').text(bc.callsign));
        var dl = $('<dl class="moduleSm floatedList clearfix"></dl>');
        if (bc.network_affiliate) dl.append($('<dt>Network:</dt> <dd>' + bc.network_affiliate + '</dd>'));
        if (bc.channel) dl.append($('<dt>Channel:</dt> <dd>' + bc.channel + '</dd>'));
        snippet.append(dl);
        if (element.address) {
            var addr = $('<div class="adr tip"></div>');
            $('<span class="street-address">').text(element.address.address1).appendTo(addr);
            if(element.address.address2) $('<span class="street-address">').text(element.address.address2).appendTo(addr);
            var city = $('<span class="locality"></span>').text(element.address.city);
            var state = $('<span class="region"></span>').text(element.address.state);
            var zip1 = $('<span class="postal-code"></span>').text(element.address.zip1);
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
            var pos = ('address' in element && element.address.lng != null) ? [element.address.lng, element.address.lat] : null;
            var descriptionHTML = SLF.generateDescriptionHTML(element);
            if (pos !== null) {
                var marker= SLF.addMarker(element.broadcaster.callsign, pos, descriptionHTML, SLF.stationMarkerImage);
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
        if ( SLF.locations.length == 1) {  SLF.map.setZoom(12); } else { SLF.map.fitBounds(mapBounds); }
        // SLF.updateStationSelect();
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
            url: '/stations/nearby.json',
            dataType: 'json',
            data: {'lon': SLF.selectedGeocoderResult.geometry.location.lng(), 'lat': SLF.selectedGeocoderResult.geometry.location.lat(), 'radius': radius},
            success: SLF.handleNearbySuccess,
            complete: SLF.handleNearbyComplete
        });
    };


    SLF.generateModal = function(title, body_html) {
        var modal = $('<div class="modal"></div>');
        modal.append($('<div class="modal-header"></div>').html('<button type="button" class="close" data-dismiss="modal">&times;</button><h3>' + title + '</h3>'));
        var modal_body = $('<div class="modal-body"></div>').html(body_html);
        modal.append(modal_body);
        $('body').append(modal);
        $(modal).modal({'backdrop': false, show: false });
        return modal;
    };

    $("form#map_form").submit(function(event) {
        var address = $("form#map_form input#address");
        var city = $("form#map_form input#city");
        var state = $("form#map_form #state");
        var full_address = address.val() + ' ' + city.val() + ', ' + state.text();
        SLF.geocoder.geocode( {'address': full_address}, function(results, status)
        {
            if (status == gm.GeocoderStatus.OK)
            {
                if (SLF.DEBUG) window.log('GeocoderStatus.OK results:');
                if (SLF.DEBUG) window.log(results);
                if (results.length == 1) {
                    SLF.setselectedGeocoderResult(results[0]);
                    SLF.findNearbyLocations();
                    if (results[0]['geometry']['location_type'] == gm.GeocoderLocationType.APPROXIMATE) {
                        var approx_modal = SLF.generateModal('Location is approximate.', '<p>We could not find an exact address, but we did find an approximate location.</p>');
                        $(approx_modal).modal('show');
                    }
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
                    var modal = SLF.generateModal('Multiple results were found, please choose one.', location_select);
                    $(modal).modal('show');
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

             } else if (status == gm.GeocoderStatus.ZERO_RESULTS) {
                if (SLF.DEBUG) window.log("Geocode returned 0 results");
                var noresults_modal = SLF.generateModal('We encountered an error.', '<p>The Google geocoder was unable to find your address.</p>');
                $(noresults_modal).modal('show');
            } else {
                if (SLF.DEBUG) window.log("Geocode was not successful for the following reason: " + status);
                var fail_modal = SLF.generateModal('We encountered an error.', '<p>'+ status + '</p>');
                $(fail_modal).modal('show');
            }
        });

        return false;
    });

});