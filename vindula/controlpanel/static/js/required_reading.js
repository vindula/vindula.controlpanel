$j = jQuery.noConflict();

$j(document).ready(function(){
	
	$j('input#agree[type="checkbox"]').change(function(ev){
		if(this.checked){
			$j.ajax({    
				type: "POST",
				url: url,
				dataType: "html",
				success: function(data){
					var dom = $j(data);
					dom.find('.managePortletsFallback').remove();
					var content = dom.find('.columnMid').attr('class', 'ajax-columnMid');
			        dom.filter('script').each(function(){
			            $j.globalEval(this.text || this.textContent || this.innerHTML || '');
			        });
			        $j('.columnMid').html(content);
					ploneFormTabbing.initialize();
					$j('#portal-column-content').removeClass('transparent');
				}
			});
		}
	});
});