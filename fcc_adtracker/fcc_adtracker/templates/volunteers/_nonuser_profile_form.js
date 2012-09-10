{% load static from staticfiles %}
<script type="text/javascript">
    $(document).ready(function() {
        var submitted = false;
        var submit_btn = $('#noaccount_signup input[type=submit]');
        submit_btn.removeAttr('disabled');
        $('#noaccount_signup').validator({
            'position': 'bottom left',
            'messageClass': 'alert-error'
        }).submit(function(event) {
            var formObj = $(this);
            var isValid = formObj.data("validator").checkValidity();
            if (submitted == false && isValid) {
                submitted = true;
                submit_btn.attr('disabled', 'disabled');
                var data = formObj.serialize();
                jQuery.post("{% url noaccount_signup %}", data, function(resp, textStatus) {
                    var output;
                    if ('content' in resp) {
                        output = $(resp.content);
                    }
                    else {
                    output = $('<p class="alert alert-success">');
                        output.text(resp.message);
                    }
                    output.hide();
                    formObj.slideUp('fast', function() {
                        formObj.after(output);
                        output.slideDown();
                    });
                });
            }
            event.preventDefault();
            return false;
        });

        var stateSelect = $('select#state');

        if (length in stateSelect && stateSelect.length != 0) {
            stateSelect.live('change', function(event) {
                var val = $(this).val();
                jQuery.getJSON('/stations/json/by-state/' + val + '/all.json',
                function(data, textStatus, jqXHR) {
                    if (textStatus == 'success') {
                        var broadcastersEl = $('#noaccount_signup [name=broadcasters]');
                        if (broadcastersEl.is('input')) {
                            var selectEl = $('<select name="broadcasters" multiple size="10"></select>');
                            broadcastersEl.replaceWith(selectEl);
                            broadcastersEl = selectEl;
                        }
                        else
                        {
                            broadcastersEl.empty();
                        }
                        for (var i=0; i < data.length; i++) {
                            var optionEl = $('<option>')
                            optionEl.val(data[i]['callsign']);
                            var labelText = '';
                            if ('combined_name' in data[i]) {
                                labelText = data[i]['combined_name'];
                            }
                            else
                            {
                                labelText = data[i]['callsign'];
                            }
                            optionEl.text(labelText)
                            broadcastersEl.append(optionEl);
                        };
                    };
                });
            });
        };
    });
</script>