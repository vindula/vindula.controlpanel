$j = jQuery.noConflict();

$j(document).ready(function(){
    
    var jq_height = $j('#text-alert').height(),
        js_height = $j('#text-alert')[0].offsetHeight,
        height = Math.max(jq_height, js_height);
    
    
    $j('#title-alert').css('height', height+'px');
//  $j('#title-alert').css('line-height',height+'px');
                    
}); 