# -*- coding: utf-8 -*-

from vindula.myvindula.validation import valida_form
from Products.statusmessages.interfaces import IStatusMessage
from vindula.myvindula import MessageFactory as _
from storm.locals import *
from storm.locals import Store
from storm.expr import Desc
from vindula.myvindula.user import BaseStore, BaseFunc
import pickle


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
    logo_corporate = Pickle()
    
    
    def get_CompanyInformation(self):
        data = self.store.find(ModelsCompanyInformation) #.one()
        if data.count() > 0:
            return data
        else:
            return None
    
    def get_CompanyInformation_by_Name(self, name):
        data = self.store.find(ModelsCompanyInformation, Or(ModelsCompanyInformation.short_name.like('%' + '%'.join(name.split(' ')) + '%' ),
                                                            ModelsCompanyInformation.corporate_name.like('%' + '%'.join(name.split(' ')) + '%' ))
                               )
        if data.count() > 0:
            return data[0]
        else:
            return None
    
    
    
    def get_CompanyInformation_byID(self, id):
        data = self.store.find(ModelsCompanyInformation, ModelsCompanyInformation.id == id).one()
        if data:
            return data
        else:
            return None        

    def get_CompanyInformation_by_CNPJ(self, cnpj):
        data = self.store.find(ModelsCompanyInformation, ModelsCompanyInformation.cnpj == cnpj).one()
        if data:
            return data
        else:
            return None        

    def del_CompanyInformation(self, id):
        result = self.get_CompanyInformation_byID(id)
        if result:
            self.store.remove(result)
            self.store.flush()

    def set_CompanyInformation(self,**kwargs):
        # adicionando...
        company = ModelsCompanyInformation(**kwargs)
        self.store.add(company)
        self.store.flush()         
        
        
class RegistrationCompanyInformation(BaseFunc):
    def to_utf8(value):
        return unicode(value, 'utf-8')

    campos = {'short_name'    : {'required': True, 'type' : to_utf8, 'label':'Nome',         'decription':u'Digite o nome da empresa',          'ordem':0},
              'corporate_name': {'required': True, 'type' : to_utf8, 'label':'Razão Social', 'decription':u'Digite a razão Social da empresa',  'ordem':1},
              'cnpj'          : {'required': True, 'type' : to_utf8, 'label':'CNPJ',         'decription':u'Digite o CNPJ do empresa',          'ordem':2, 'mascara':'Cnpj'},
              'phone_number'  : {'required': False, 'type' : to_utf8, 'label':'Telefone',     'decription':u'Digite o telefone da empresa',     'ordem':3, 'mascara':'Telefone'},
              'address'       : {'required': False, 'type' : to_utf8, 'label':'Endereço',     'decription':u'Digite o endereço do empresa',     'ordem':4},
              'city'          : {'required': False, 'type' : to_utf8, 'label':'Cidade',       'decription':u'Digite o cidade da empresa',       'ordem':5},
              'stade'         : {'required': False, 'type' : to_utf8, 'label':'Estado',       'decription':u'Digite a estado da empresa',       'ordem':6},
              'postal_code'   : {'required': False, 'type' : to_utf8, 'label':'CEP',          'decription':u'Digite o cep da empresa',          'ordem':7, 'mascara':'Cep'},
              'email'         : {'required': False, 'type' : 'email',   'label':'E-mail',       'decription':u'Digite o email da empresa',      'ordem':8},
              'website'       : {'required': False, 'type' : to_utf8, 'label':'Site',           'decription':u'Digite o site da empresa',       'ordem':9, 'mascara':'Site'},
              'logo_corporate' : {'required': False, 'type' : 'file',  'label':'Logo da Empresa','decription':u'Coloque o logo da empresa',     'ordem':10},
              }
                        
    def registration_processes(self,context):
        success_url = context.context.absolute_url() + '/vindula-company-information'
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

            if form['logo_corporate'].filename != '':
                
                photo = form.get('logo_corporate',None)
                filename = photo.filename # pega o nome do arquivo
                if not filename.endswith('png') and not filename.endswith('jpg') and not filename.endswith('gif') and\
                    not filename.endswith('PNG') and not filename.endswith('JPG') and not filename.endswith('GIF'): 
                    
                    errors['logo_corporate'] = u"Selecione um arquivo de Imagem"
            
            if not errors:

                if form['logo_corporate'].filename != '':
                        photo = form.get('logo_corporate',None)    
                        upload = photo.read()       
                        M ={}
                        M['data'] = upload
                        M['filename'] = filename                        
                        data['logo_corporate'] = unicode(pickle.dumps(M),'utf-8')
                    
                if 'id' in form_keys:
                    # editando...
                    id = int(form.get('id'))
                    # editando...
                    result = ModelsCompanyInformation().get_CompanyInformation_byID(id)
                    if result:
                        if not form['logo_corporate'].filename:
                            data['logo_corporate'] = result.logo_corporate
                        
                        for campo in campos.keys():
                            value = data.get(campo, None)
                            setattr(result, campo, value)
                        
                        BaseStore().store.commit()

                else:
                    #adicionando...
                    ModelsCompanyInformation().set_CompanyInformation(**data)
                
                #Redirect back to the front page with a status message
                IStatusMessage(context.request).addStatusMessage(_(u"Empresa"), "info")
                context.request.response.redirect(success_url)
                                   
            else:
                form_data['errors'] = errors
                form_data['data'] = data
                return form_data
          
        # se clicou no botao "Excluir"
        elif 'form.excluir' in form_keys:
            id = int(form.get('id'))
            ModelsCompanyInformation().del_CompanyInformation(id)
          
            #Redirect back to the front page with a status message
            IStatusMessage(context.request).addStatusMessage(_(u"Empresa movida"), "info")
            context.request.response.redirect(success_url)
          
        # se for um formulario de edicao
        elif 'id' in form_keys:         
            id = form.get('id','0')
            id = int(id)

            data = ModelsCompanyInformation().get_CompanyInformation_byID(id)
            D = {}
            for campo in campos.keys():
                D[campo] = getattr(data, campo, '')
            if data:
               form_data['data'] = D
               return form_data
            else:
               return form_data                

                
        # se for um formulario de adicao
        else:
            return form_data      
            



class ModelsProducts(Storm, BaseStore):
    __storm_table__ = 'vin_controlpanel_products'
    
    id        = Int(primary=True)
    name      = Unicode()
    title     = Unicode()
    active    = Bool()
    installed = Bool()
    
    def get_ProductsId(self, id):
        # seeking...
        data = self.store.find(ModelsProducts, ModelsProducts.name == id)
        if data:
            return data
        else:
            return None
        
    def get_ProductsName(self, name):
        # seeking...
        data = self.store.find(ModelsProducts, ModelsProducts.name == unicode(name))
        if data:
            return data
        else:
            return None
    
    def get_AllProducts(self):
        # seeking...
        data = self.store.find(ModelsProducts)
        if data:
            return data
        else:
            return None

    def set_Products(self,**kwargs):
        # adding...
        product = ModelsProducts(**kwargs)
        self.store.add(product)
        self.store.flush()
        