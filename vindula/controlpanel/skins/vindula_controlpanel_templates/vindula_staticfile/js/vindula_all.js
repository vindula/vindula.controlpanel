/**
 * Copyright Vindula Inc.
 * 
 * Licensed under the Apache License, Version 2.0
 * http://www.apache.org/licenses/LICENSE-2.0
 */

/*
 * try { window.Vindula || (function(window) {
 * 
 * alert('asjkdnasjkdajk');
 * 
 * }); } catch (e) { new Image().src = "https:\/\/www.facebook.com\/" +
 * 'common/scribe_endpoint.php?c=jssdk_error&m=' +
 * encodeURIComponent('{"error":"LOAD", "extra": {"name":"' + e.name +
 * '","line":"' + (e.lineNumber || e.line) + '","script":"' + (e.fileName ||
 * e.sourceURL || e.script) + '","stack":"' + (e.stackTrace || e.stack) +
 * '","message":"' + e.message + '"}}'); }
 */

(function($){
	
	var api = {
	config : {}, 
	init : function(options) {
		this.config = options;
		this.like();
		this.comment();
		this.rating();
		this.share();
		this.favorite();
		this.follow();
		this.access();

	},
	load : function(action,height,parameters,get_parameters){
			var obj = this.config.obj,
				conf = this.config,
				make_url =  this.make_url;
			$(obj).find('.vd-'+action).each(function() {
				var iframe = $('<iframe />'),
				//Parametros de Configuração
				parameter, local_parameters = [], get_local_parameters = {}, get_parameter;
				
				for (var i=0;i<parameters.length;i++){
					parameter = parameters[i];		
					local_parameters[i] = $(this).attr('data-'+parameter);
				}
				if (get_parameters){
					for (var i=0;i<get_parameters.length;i++){
						get_parameter = get_parameters[i]
						get_local_parameters[get_parameter] = $(this).attr('data-'+get_parameter);
					}	
				}
				
				url = make_url(action,local_parameters,get_local_parameters);
				
				iframe.addClass('new-'+action);
				iframe.attr('src',url);
				iframe.height(height);
				iframe.width(conf.width);
					
				$(this).append(iframe);
			});
		
	},
	make_url : function(action,parameters,get_parameters) {
		var url,parameter,
			conf = api.config;
		url = conf.dominio.concat(conf.path_app,'social/',action,'/',conf.user_token,'/'); 
		
		for (var i=0;i<parameters.length;i++){
			parameter = parameters[i];
			url = url.concat(parameter,'/');
		}
		
		if (get_parameters){
			url = url.concat('?');
			for (var get_parameter in get_parameters){
				url = url.concat(get_parameter,'=',get_parameters[get_parameter], '&');
			}
		}

		return url;
	}, 
	like : function() {
		// Constantes
		var action = 'like',
			height = 65,
			parameters = ['type','uid'];
			
		this.load(action,height,parameters);
	},
	comment : function() {
		// Constantes
		var action = 'comment',
			height = 200,
			parameters = ['type','uid'];
			
		this.load(action,height,parameters);
	},
	rating : function() {
		// Constantes
		var action = 'rating',
			height = 70,
			parameters = ['type','uid'];

		this.load(action,height,parameters);
	},
	share : function() {
		// Constantes
		var action = 'share',
			height = 70,
			parameters = ['type','uid'];

		this.load(action,height,parameters);
	},
	favorite : function() {
		// Constantes
		var action = 'favorite',
			height = 150,
			parameters = ['type','uid'];

		this.load(action,height,parameters);
	},
	follow : function() {
		// Constantes
		var action = 'follow',
			height = 65,
			parameters = ['type','uid'];

		this.load(action,height,parameters);
	},
	access : function() {
		// Constantes
		var action = 'access',
			height = 0,
			parameters = ['type','uid'],
		    timeout = 5000;
		    
		    setTimeout(this.load(action,height,parameters),timeout);
	}
	};
	
    $.fn.extend({ 
        vindula: function(options) {

			// Configuração global e padrão
            var defaults = {
				width:'100%',
				//height:55,	
				username:null,
				user_token:null,
				dominio:'',
				path_app: '/vindula-api/',

            }
                 
            var options =  $.extend(defaults, options);
 
            return this.each(function() {
				options['obj'] = this;
				api.init(options);
             
            });
        }
    });
     
})(jQuery);