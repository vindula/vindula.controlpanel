$j = jQuery.noConflict();

$j(document).ready(function(){
    
    $j('#form-widgets-ativa_redirect-0').click(function(){
       var redirect = $j('#form-widgets-ativa_redirect-0');
       if(redirect.attr('checked')){
       
           var classico = $j('#form-widgets-ativa_loginClassico-0');
           var grafico = $j('#form-widgets-ativa_loginGrafico-0');
           
           if(classico.attr('checked')){
               alert('Ao habilitar a função de redirect, o login clássico será desabilitado e o login grafico será habilitado');
               classico.attr('checked',false);
               grafico.attr('checked',true);
               
           };
       };
    });

    $j('#form-widgets-ativa_loginClassico-0').click(function(){
       var classico = $j('#form-widgets-ativa_loginClassico-0');
       var redirect = $j('#form-widgets-ativa_redirect-0');
       var grafico = $j('#form-widgets-ativa_loginGrafico-0');
       if(classico.attr('checked')){
           
           if(redirect.attr('checked')){
               alert('Ao habilitar a função de login classico, a função de redirect será desabilitado');
               redirect.attr('checked',false);
               grafico.attr('checked',false);
               
           }else{
                if(grafico.attr('checked')){
                    grafico.attr('checked',false);
                };
           };
        }else{
            if(grafico.attr('checked')){
               grafico.attr('checked',false);
            };
            
        };
    });
    
    $j('#form-widgets-ativa_loginGrafico-0').click(function(){
       var grafico = $j('#form-widgets-ativa_loginGrafico-0');
       if(grafico.attr('checked')){
       
           var classico = $j('#form-widgets-ativa_loginClassico-0');
           
           if(classico.attr('checked')){
               classico.attr('checked',false);
               
           }
        }
    });


});