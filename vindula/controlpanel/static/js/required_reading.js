$j = jQuery.noConflict();

$j(document).ready(function(){
	
	$j('input#agree[type="checkbox"]').change(function(ev){
		if(this.checked){
			var form_action = $(this).parents('form'),
				url = $('input#url').val(),
				uid_el = this.value;

			$j.ajax({    
				type: "POST",
				url: url,
				dataType: "html",
				data: {'read': true},
				success: function(data){
					var dom = $j(data),
						content = dom.find('#content-required-reading');
			        $j('#content-required-reading').html(content.contents());
			        
			        var panel = $('div.required-read-panel');
			        
			        if (panel) {
			        	var qtd_docs_el = $('.qtd-docs', panel),
			        		qtd_docs = qtd_docs_el.text(),
			        	    item = $('li#'+uid_el, panel);
			        	
			        	if (qtd_docs) { 
			        		qtd_docs = parseInt(qtd_docs);
			        		qtd_docs = qtd_docs - 1;
			        		
			        		if(qtd_docs == 1) {
				                qtd_docs_el.parent().html('Você tem <strong tal:content="python:len(documents)" class="qtd-docs">'+qtd_docs+'</strong> leitura obrigatória');
			        		}else if(qtd_docs == 0) {
				                qtd_docs_el.parents('.required-read-panel').remove();
			        		}else {
			        			qtd_docs_el.text(qtd_docs);
			        		}
			            }
			        	
			        	if (item) {
			        		item.remove();
			        	}
			        }
			        
				}
			});
		}
	});
});