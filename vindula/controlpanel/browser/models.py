# -*- coding: utf-8 -*-

from vindula.myvindula.validation import valida_form
from Products.statusmessages.interfaces import IStatusMessage
from vindula.myvindula import MessageFactory as _
from storm.locals import *
from storm.locals import Store
from vindula.myvindula.user import BaseStore, BaseFunc



class ModelsCompanyInformation(Storm, BaseStore):
    __storm_table__ = 'vin_controlpanel_company_information'
    
    id = Int(primary=True)
    short_name = Unicode()
    corporate_name = Unicode()
    cnpj = Unicode()
    phone_number = Unicode()
    date_creation = DateTime()
    address = Unicode()
    city = Unicode()
    stade = Unicode()
    postal_code = Unicode()
    email = Unicode()
    website = Unicode()
    
    
    def get_CompanyInformation(self):
        data = self.store.find(ModelsCompanyInformation).one()
        if data:
            return data
        else:
            return None

    def set_CompanyInformation(self,**kwargs):
        # adicionando...
        company = ModelsCompanyInformation(**kwargs)
        self.store.add(company)
        self.store.flush()         
        
        
class RegistrationCompanyInformation(BaseFunc):
    def to_utf8(value):
        return unicode(value, 'utf-8')

    campos = {'short_name'    : {'required': False, 'type' : to_utf8, 'label':'Nome',         'decription':u'Digite o nome da empresa',         'ordem':0},
              'corporate_name': {'required': False, 'type' : to_utf8, 'label':'Razão Social', 'decription':u'Digite a razão Social da empresa', 'ordem':1},
              'cnpj'          : {'required': False, 'type' : to_utf8, 'label':'CNPJ',         'decription':u'Digite o CNPJ do empresa',         'ordem':2},
              'phone_number'  : {'required': False, 'type' : to_utf8, 'label':'Telefone',     'decription':u'Digite o telefone da empresa',     'ordem':3},
              'address'       : {'required': False, 'type' : to_utf8, 'label':'Endereço',     'decription':u'Digite o endereço do empresa',     'ordem':4},
              'city'          : {'required': False, 'type' : to_utf8, 'label':'Cidade',       'decription':u'Digite o cidade da empresa',       'ordem':5},
              'stade'         : {'required': False, 'type' : to_utf8, 'label':'Estado',       'decription':u'Digite a estado da empresa',       'ordem':6},
              'postal_code'   : {'required': False, 'type' : to_utf8, 'label':'CEP',          'decription':u'Digite o cep da empresa',          'ordem':7},
              'email'         : {'required': False, 'type' : 'email',   'label':'E-mail',       'decription':u'Digite o email da empresa',        'ordem':8},
              'website'       : {'required': False, 'type' : to_utf8, 'label':'Site',         'decription':u'Digite o site da empresa',         'ordem':9}}
                        
    def registration_processes(self,context):
        success_url = context.context.absolute_url() + '/@@vindula-control-panel'
        access_denied = context.context.absolute_url() + '/login'
        form = context.request # var tipo 'dict' que guarda todas as informacoes do formulario (keys,items,values)
        form_keys = form.keys() # var tipo 'list' que guarda todas as chaves do formulario (keys)
        campos = self.campos
        
        # divisao dos dicionarios "errors" e "convertidos"
        form_data = {
            'errors': {},
            'data': {},
            'campos':campos,}
        
        # se clicou no botao "Voltar"
        if 'form.voltar' in form_keys:
            context.request.response.redirect(success_url)
          
        # se clicou no botao "Salvar"
        elif 'form.submited' in form_keys:
            # Inicia o processamento do formulario
            # chama a funcao que valida os dados extraidos do formulario (valida_form) 
            errors, data = valida_form(campos, context.request.form)  

            if not errors:
                # editando...
                result = ModelsCompanyInformation().get_CompanyInformation()
                if result:
                    for campo in campos.keys():
                        value = data.get(campo, None)
                        setattr(result, campo, value)

                else:
                    #adicionando...
                    ModelsCompanyInformation().set_CompanyInformation(**data)
                #Redirect back to the front page with a status message
                IStatusMessage(context.request).addStatusMessage(_(u"Thank you for your order. We will contact you shortly"), "info")
                context.request.response.redirect(success_url)
                                   
            else:
                form_data['errors'] = errors
                form_data['data'] = data
                return form_data
          
        # se for um formulario de edicao 
        else:
            data = ModelsCompanyInformation().get_CompanyInformation()
            D = {}
            for campo in campos.keys():
                D[campo] = getattr(data, campo, '')
            if data:
               form_data['data'] = D
               return form_data
            else:
               return form_data
              
#        # se o usuario não estiver logado
#        else:
#            IStatusMessage(context.request).addStatusMessage(_(u'Error to saving the register.'),"erro")
#            context.request.response.redirect(access_denied)
    