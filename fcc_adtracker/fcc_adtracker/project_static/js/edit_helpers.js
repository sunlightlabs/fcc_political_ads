/*
    For front-end edit pages, currently:
        * political buy edit pages.
    Depends on:
        * URI.js
        * chosen.jquery.min.js
*/
jQuery(document).ready(function($) {
    // Depends on URI.js
    function updatedPopupUrl(add_url_element, p_args) {
        var target_uri = $(add_url_element).uri();
        var arg_obj = target_uri.query(true);
        $.extend(arg_obj, p_args);
        target_uri.search(arg_obj);
    }

    function jq_to_htmlstring(jq_obj) {
        return $('<div>').append(jq_obj).html();
    }

    // Add url args to advertiser_signatory_form
    var add_adversig_el = $('#add_id_advertiser_signatory');
    updatedPopupUrl(add_adversig_el, {'advertiser_id': $('#id_advertiser').val()});

    jQuery.unique($('select.suggestions')).each(function(index) {
        var original_select = this;
        var addRelated_el = $(original_select).next('a.add-on');
        if (addRelated_el.length != 0) {
            var uri = addRelated_el.uri();
            $(original_select).data('add_uri', uri);
            addRelated_el.detach();
            $(original_select).chosen({
                no_results_text: jq_to_htmlstring(addRelated_el)
            });
            $(document).on('django:dismissaddanotherpopup', function(event) {
                $(original_select).trigger("liszt:updated");
                chosen.results_hide();
            });
            var chosen = $(original_select).data('chosen');
            chosen.search_field.keyup(function(event) {
                var input_val = chosen.search_field.val();
                updatedPopupUrl(addRelated_el, {'search': input_val});
                chosen.results_none_found = jq_to_htmlstring(addRelated_el);
                var results_len = chosen.search_results.children('li:visible').not('.no-results').length;
                chosen.no_results_clear();
                if (results_len === 0) chosen.no_results(input_val);
            });
        }
        else {
            $(original_select).chosen();
        }
    });

    $(document).on('change', '#id_advertiser', function(event) {
        var uri = $(this).data('add_uri');
        var chosen = $('#id_advertiser_signatory').data('chosen');
        var add_el = $(chosen.results_none_found);
        updatedPopupUrl(add_el, {'advertiser_id': $('#id_advertiser').val()});
        chosen.results_none_found = jq_to_htmlstring(add_el);
        $(this).data('chosen', chosen);
    });

    /*
        Update spots helper
    */
    if (update_spots_url !== undefined) {
        var spots_table = $('table.politicalspots');
        $('table.politicalspots, #politicalspot-add').on('django:dismissaddanotherpopup', function(event) {
            var target_el = $(spots_table);
            log('dismissaddanotherpopup event');
            $.get(update_spots_url, function(data, textStatus, jqXHR) {
                var new_content = $(data);
                target_el.fadeOut(500, function() {
                    target_el.replaceWith(new_content);
                    new_content.fadeIn(500);
                });
            });
        });
    }
});