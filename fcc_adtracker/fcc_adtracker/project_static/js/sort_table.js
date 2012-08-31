jQuery(document).ready(function($) {
    var table_el = $('table.sortable');
    var pagerOptions = {
        container: $(".pager"),
        page: 0,
        size: 20
    };
    var rowCount = table_el.children('tbody > tr').length;
    // if (rowCount > pagerOptions.size) {
        table_el.tablesorter({
             cssChildRow: "row-child"
        }).tablesorterPager(pagerOptions);
    // }
    // else
    // {
    //     $('.pager').hide();
    // }
});
