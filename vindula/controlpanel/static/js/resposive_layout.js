$j = jQuery.noConflict();

$j(document).ready(function(){
	
	var width = $j(window).width(),
	    column_content = $j('#portal-column-content', $document),
	    column_one = $j('#portal-column-one', $document),
	    column_two = $j('#portal-column-two', $document);
	
	if (width) {
		var $document = $j(this);
		
		//Tamanho,em pixels, usado para tablets
		if (width >= 634 && width <= 861) {

			//S— vou reordenar as colunas caso houver as 2
			if (column_one.length && column_two.length) {
				column_one.insertAfter(column_content);
			}
		}
	}
	
	$j(window).resize(function(){
		width = $j(window).width();
		
		if (width) {
			
			//Tamanho,em pixels, usado para tablets
			if (width >= 634 && width <= 861) {
				
				//S— vou reordenar as colunas caso houver as 2
				if (column_one.length && column_two.length) {
					column_one.insertAfter(column_content);
				}
				//Coloco a coluna da esquerda de volta para a esquerda
				else if (column_one.length) {
					column_one.insertBefore(column_content);
				}
			}
			
			//Tamanho,em pixels, usado para smartphones
			else if (width < 634) {
				
				//S— vou reordenar as colunas caso houver as 2
				if (column_one.length) {
					column_one.insertAfter(column_content);
				}
			}
			
			//Tamanho,em pixels, usado para telas maiores
			else {
				
				//S— vou reordenar as colunas caso houver as 2
				if (column_one.length) {
					column_one.insertBefore(column_content);
				}
			}
		}
	});
});