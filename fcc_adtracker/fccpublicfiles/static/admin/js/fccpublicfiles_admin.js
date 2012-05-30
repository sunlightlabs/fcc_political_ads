jQuery(document).ready(function($) {

    $('.typeahead').each(function(index, element) {
        var name = $(this).attr('name');

        $.getJSON('/admin/fccpublicfiles/field_json/', {'fieldname': name }, function(json, textStatus) {
            var data = json;
            $('#id_' + name).data('source',data);
        });
    });


});
