$j = jQuery.noConflict();

$j(document).ready(function(){
	$j('#cnpj').attr('maxlength','18')
	$j('#phone_number').attr('maxlength','14')
	$j('#postal_code').attr('maxlength','9')
	
	$j('#cnpj').keydown(function(){
		Mascara(this,Cnpj);
	});
	$j('#cnpj').keypress(function(){
		Mascara(this,Cnpj);
	});
	$j('#cnpj').keyup(function(){
		Mascara(this,Cnpj);
	});
	
	$j('#phone_number').keydown(function(){
		Mascara(this,Telefone);
	});
	$j('#phone_number').keypress(function(){
		Mascara(this,Telefone);
	});
	$j('#phone_number').keyup(function(){
		Mascara(this,Telefone);
	});
	
	$j('#postal_code').keydown(function(){
		Mascara(this,Cep);
	});
	$j('#postal_code').keypress(function(){
		Mascara(this,Cep);
	});
	$j('#postal_code').keyup(function(){
		Mascara(this,Cep);
	});
					
});	