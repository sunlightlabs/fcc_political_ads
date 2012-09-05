/* window.log taken from HTML5 boilerplate */
window.log = function f(){ log.history = log.history || []; log.history.push(arguments); if(this.console) { var args = arguments, newarr; args.callee = args.callee.caller; newarr = [].slice.call(args); if (typeof console.log === 'object') log.apply.call(console.log, console, newarr); else console.log.apply(console, newarr);}};
(function(a){function b(){}for(var c="assert,count,debug,dir,dirxml,error,exception,group,groupCollapsed,groupEnd,info,log,markTimeline,profile,profileEnd,time,timeEnd,trace,warn".split(","),d;!!(d=c.pop());){a[d]=a[d]||b;}})
(function(){try{console.log();return window.console;}catch(a){return (window.console={});}}());

jQuery(document).ready(function($) {
    if (!Modernizr.input.placeholder) {
        $(this).find('[placeholder]').each(function()
        {
            if ($(this).val() === '') // if field is empty
            {
                $(this).val( $(this).attr('placeholder') );
            }
        });
        $('[placeholder]').focus(function()
            {
                if ($(this).val() == $(this).attr('placeholder'))
                {
                    $(this).val('');
                    $(this).removeClass('placeholder');
                }
            }).blur(function()
            {
                if ($(this).val() === '' || $(this).val() == $(this).attr('placeholder'))
                {
                    $(this).val($(this).attr('placeholder'));
                    $(this).addClass('placeholder');
                }
            });

            // remove placeholders on submit
            $('[placeholder]').closest('form').submit(function()
            {
                $(this).find('[placeholder]').each(function()
                {
                    if ($(this).val() == $(this).attr('placeholder'))
                    {
                        $(this).val('');
                    }
                });
            });
    }

    /*
        Typeahead transformations for select forms
        depends on underscore.js
    */
    /*
    var transform_list = jQuery.unique($('select.suggestions'));
    transform_list.each(function(index) {
        var select_el = $(this);
        var option_dict = {}, typeahead_labels = [], initial_label = select_el.children(':selected').eq(0).val() !== '' ? select_el.children(':selected').eq(0).text() : '';
        var proxy_id = 'proxy-'+ select_el.attr('id');
        var input_proxy = $('<input id="'+ proxy_id + '" type="text" data-provide="typeahead">').val(initial_label).addClass('typeahead select_proxy');
        if (!jQuery.contains(document, input_proxy[0])) {
            $(this).children('option').each(function(index) {
                if ($(this).val() !== '') {
                    typeahead_labels.push($(this).text());
                    option_dict[$(this).text()] = $(this).val();
                }
            });
            input_proxy.data('option_dict', option_dict);
            $(input_proxy).typeahead({
                source: typeahead_labels,
                items: 14
            })
            .change(function(event) {
                var new_label = $(this).val();
                select_el.val(option_dict[new_label]);
            });
            $(this).hide();
            $(this).before(input_proxy);
        }

    });
*/

});
