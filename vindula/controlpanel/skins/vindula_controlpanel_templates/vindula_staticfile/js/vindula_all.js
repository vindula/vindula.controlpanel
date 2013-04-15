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
        	this.root();
        	this.like();
        	this.comment();
        	this.rating();
        	this.share();
        	this.favorite();
        	this.follow();
            this.combo_standard();
        },
        load : function(action,height,parameters,get_parameters,url_action){
                if (typeof url_action == 'undefined')
                    url_action = action
                
        		var obj = this.config.obj,
        			conf = this.config,
        			make_url =  this.make_url,
                    make_iframe =  this.make_iframe;
        		$(obj).find('.vd_'+action).each(function() {
        			var $iframe = $('<iframe />'),
        			//Parametros de Configuração
        			parameter, local_parameters = [], get_local_parameters = {}, get_parameter;
        			
        			for (var i=0;i<parameters.length;i++){
        				parameter = parameters[i];		
        				local_parameters[i] = $(this).attr('data_'+parameter);
        			}
        			if (get_parameters){
        				for (var i=0;i<get_parameters.length;i++){
        					get_parameter = get_parameters[i]
        					get_local_parameters[get_parameter] = $(this).attr('data_'+get_parameter);
        				}	
        			}
        			
                    hash_id = hex_md5(action + $(this).attr('data_uid'));
                    get_local_parameters['hash_id'] = hash_id;
        			url = make_url(url_action,local_parameters,get_local_parameters);
        			
                    params_iframe = {'class': 'new_'+action,
                                     'src': url,
                                     'height': height,
                                     'width': conf.width,
                                     'id': hash_id}
                                    
        			$(this).append(make_iframe(params_iframe));
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
        make_iframe : function(params) {
            var params_def = {'frameborder': 0,
                              'scrolling': 'no'}
            params_def = $.extend(params_def, params);
            return $('<iframe>',params_def);
        },
        add_send_box : function(params) {
            var params_def = {'frameborder': 0,
                              'scrolling': 'no'}
            params_def = $.extend(params_def, params);
            var $iframe = make_iframe(params_def);
            
            if($('#'+params.hash_id).length >= 1)
                $('#'+params.hash_id).replaceWith($iframe);
            else
                $('#'+params.hash_id).after($iframe); 
        },
        root : function() {
        	// Constantes
        	var action = 'root',
        		height = 0,
        		parameters = ['type','uid'],
        		get_parameters = ['title','description','owner','date_created','date_modified','workflow','image'];
        		
        	this.load(action,height,parameters,get_parameters);
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
        combo_standard : function() {
            // Constantes
            var url_action = 'combo/standard'
                action = 'combo_standard',
                height = 65,
                get_parameters = null,
                parameters = ['type','uid'];
        
            this.load(action,height,parameters,get_parameters,url_action);
        }
	};
	
     $.fn.extend({ 
        vindula: function(method) {
            
            var options = Array.prototype.slice.call( arguments, 1 )[0]
            
            if ( api[method] ) {
                return api[method].apply( this, options);
            } else if ( typeof method == 'object' || ! method ) {
                // Configuracoes global e padrao
                var defaults = {
                    width:'100%',
                    username:null,
                    user_token:null,
                    dominio:'',
                    path_app: '/vindula-api/',
                }
                
                options = $.extend(defaults, options);
                
                return this.each(function() {
                    options['obj'] = this;
                    api.init(options);
                });
            } else {
                $.error( 'Method ' +  method + ' does not exist on jQuery.vindula' );
            }    
        }
    });

})(jQuery);