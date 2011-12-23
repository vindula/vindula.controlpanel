$j = jQuery.noConflict();

$j(document).ready(function(){
	
	var height = $j('#text-alert').height();
	$j('#title-alert').css('height', height+'px');
	$j('#title-alert').css('line-height',height+'px');
					
});	