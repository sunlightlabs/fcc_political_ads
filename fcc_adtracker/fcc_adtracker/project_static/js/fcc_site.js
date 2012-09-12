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
});
