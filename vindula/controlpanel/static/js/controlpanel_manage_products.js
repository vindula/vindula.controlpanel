$j = jQuery.noConflict();

$j(document).ready(function(){
        
    for(var i = 1; i <= $j('table#table_products tr').length; i++)
    {
        element = $j('table#table_products tr').eq(i)
        if (i % 2 != 0)
          element.attr('class', 'cor1')
    }
	
});

