$j = jQuery.noConflict();

function loadAll(){
	loadSmartColorPickers();
	launchCKInstances();
	goTop();
	
	var common_content_filter = '#content=*,dl.portalMessage.error,dl.portalMessage.info';
	$j('a.editPermissions').prepOverlay({
		subtype: 'ajax',
		formselector: 'form[name="edit_form"]',
		filter: common_content_filter,
		noform: 'close',
		width: '50%'
    });
}

//pega o form do elemento input
function getSuperForm(el){
	var form = el.parentElement;
	if (form.tagName != 'FORM')
	{
		form = getSuperForm(form);
	}
	
	return form;
}

//vai para o topo da pagina
function goTop(){
	window.scrollTo(0, 0);
}

$j(document).ready(function(){
	loadAll();
	
	$j('.portletItemPrefs .head').click(function() {
		$j(this).next().toggle('slow');
		var div_seta = $j(this).find('div.seta');
		div_seta.toggleClass('seta-left');
		div_seta.toggleClass('seta-top');
		return false;
	});
	
	var topic_selected = $j('.subTopic .selected').parents('dd').find('#topic');
	topic_selected.addClass('selectedHead');

	$j('.portletItemPrefs .head').each(function(){
		var topic = $j(this);
		if (!topic.hasClass('selectedHead'))
		{
			var div_seta = topic.find('div.seta');
			div_seta.toggleClass('seta-left');
			div_seta.toggleClass('seta-top');
			topic.next().hide();
		}
	})
		
	$j(".subTopicAjax").live('click', function(){
		var url = $j(this).attr('name');
		removeEditor();
		
		$j('.selected').removeClass('selected');
		$j('.selectedHead').removeClass('selectedHead');
		$j(this).addClass('selected');
		var topic_selected = $j('.subTopic .selected').parents('dd').find('#topic');
		topic_selected.addClass('selectedHead');
		
		$j('#portal-column-content').addClass('transparent');
		goTop();
		
		$j.ajax({    
			type: "get",
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
				loadAll();
			}
		});
	})

	$j(".ajax-columnMid #content form input[type='submit']").live('click', function(){
		/* Atualiza os textarea que usa o CKEditor */
		CKupdate();
		
		/* get some values from elements on the page: */
		var button_clicked = this;
		var form = getSuperForm(this);
		var url = form.action;
		var select_list = $j(form).find('select');
		var params = {};
		
		$j('#portal-column-content').addClass('transparent');
		goTop();
		
		// FONTE: http://be.twixt.us/jquery/formSubmission.php
		$j(form)
		.find("input:checked, input[type='text'], input[type='hidden'], input[type='password'], option:selected, textarea")
		.each(function() {
			var name = this.name || this.parentNode.name || this.id || this.parentNode.id;
			if ((this.type == 'checkbox' || name.split(':').length == 2) && params[this.name]) {
				if (params[name] instanceof Array){
					params[name].push(this.value);
				}
				else{
					var old_value =  params[name]
					params[name] = new Array();
					params[name].push(old_value);
					params[name].push(this.value);
				}
			}
			else{
				params[ name ] = this.value;
			}
		});
		
		params[button_clicked.name] = button_clicked.value;
		
		select_list.each(function(){
			if (this.multiple)
			{
				var name_select = this.name || this.parentNode.name || this.id || this.parentNode.id;
				var options = $j(this)
				.find('option')
				.each(function(){
					if (params[name_select] instanceof Array){
						params[name_select].push(this.value);
					}
					else{
						params[name_select] = new Array();
						params[name_select].push(this.value);
					}
				});
			}
		});

		/* Send the data using post and put the results in a div */
		removeEditor();
		$j.ajax({
			traditional: true,
			type: "post",
			url: url,
			dataType: "text",
			data: params,
			success: function(data) {
				var dom = $j(data);
				dom.find('.managePortletsFallback').remove();
				var content = dom.find('.columnMid').attr('class', 'ajax-columnMid');
		        dom.filter('script').each(function(){
		            $j.globalEval(this.text || this.textContent || this.innerHTML || '');
		        });
		        $j('.columnMid').html(content);
				ploneFormTabbing.initialize();
				$j('#portal-column-content').removeClass('transparent');
				loadAll();
			}
		});
		
		//cancel the submit button default behaviours
        return false;
	});
});
