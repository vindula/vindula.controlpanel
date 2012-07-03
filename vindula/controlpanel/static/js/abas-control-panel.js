$j = jQuery.noConflict();
$j(document).ready(function(){
		$j('#div-usuarios').hide();
		$j('#div-redessociais').hide();
		$j('#div-outros').hide();
		$j('#div-logins').hide();
		$j('#div-layout').show();
	
	
	$j('#layout').click(function(){
		$j('#div-usuarios').hide();
		$j('#div-redessociais').hide();
		$j('#div-outros').hide();
		$j('#div-layout').show();
        $j('#div-logins').hide();
			
		$j('#usuarios').removeClass('selected');
		$j('#redessociais').removeClass('selected');
		$j('#outros').removeClass('selected');
		$j('#layout').addClass('selected');
		$j('#logins').removeClass('selected');
	});
	
	$j('#usuarios').click(function(){
		$j('#div-layout').hide();
		$j('#div-usuarios').show();
		$j('#div-redessociais').hide();
		$j('#div-outros').hide();
		$j('#div-logins').hide();
		
		$j('#layout').removeClass('selected');
		$j('#usuarios').addClass('selected');
		$j('#redessociais').removeClass('selected');
		$j('#outros').removeClass('selected');
		$j('#logins').removeClass('selected');
	});
	
	$j('#redessociais').click(function(){
		$j('#div-layout').hide();
		$j('#div-usuarios').hide();
		$j('#div-redessociais').show();
		$j('#div-outros').hide();
		$j('#div-logins').hide();
		
		$j('#layout').removeClass('selected');
		$j('#usuarios').removeClass('selected');
		$j('#redessociais').addClass('selected');
		$j('#outros').removeClass('selected');
		$j('#logins').removeClass('selected');
	});
	
	$j('#outros').click(function(){
		$j('#div-layout').hide();
		$j('#div-usuarios').hide();
		$j('#div-redessociais').hide();
		$j('#div-outros').show();
		$j('#div-logins').hide();
		
		$j('#layout').removeClass('selected');
		$j('#usuarios').removeClass('selected');
		$j('#redessociais').removeClass('selected');
		$j('#outros').addClass('selected');
		$j('#logins').removeClass('selected');
	});
	
	$j('#logins').click(function(){
        $j('#div-layout').hide();
        $j('#div-usuarios').hide();
        $j('#div-redessociais').hide();
        $j('#div-outros').hide();
        $j('#div-logins').show();
        
        $j('#layout').removeClass('selected');
        $j('#usuarios').removeClass('selected');
        $j('#redessociais').removeClass('selected');
        $j('#outros').removeClass('selected');
        $j('#logins').addClass('selected');
    });
	
	});
