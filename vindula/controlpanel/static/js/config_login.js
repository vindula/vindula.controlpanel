$j = jQuery.noConflict();

function checaRadio(){
	if ($j('#tipoLogin_2').is(':checked'))
	{
		$j('#ativaRedirect').attr('checked', 'checked');
		$j('#archetypes-fieldname-ativaRedirect').hide();
	}
	if ($j('#tipoLogin_1').is(':checked'))
	{
		$j('#archetypes-fieldname-ativaRedirect').show()
	}
}

$j(document).ready(function(){
	checaRadio();
	$j(':radio').click(function(){
		checaRadio();
	})
});