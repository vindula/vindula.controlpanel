# -*- coding: utf-8 -*-
from zope import schema
from plone.directives import form
from five import grok
from vindula.controlpanel import MessageFactory as _

from zope.interface import Interface
from zope.app.component.hooks import getSite

# Interface and schema

class IVindulaConfigAll(form.Schema):
    """ Vindula User Config """
    
    ativa_editfunc = schema.Bool(
                title=_(u'label_ativa_editfunc', default=u'Ativar a opção do usuário poder editar seu perfil no portal Myvindula'),
                description=_(u'help_activ_holerite', default=u'Se selecionado, ativa a opção do usuário poder editar seu perfil no portal Myvindula'),
                default=True
                )
    
    ativa_holerite = schema.Bool(
                title=_(u'label_ativa_holerites', default=u'Ativar a visualização de holerites no portal Myvindula'),
                description=_(u'help_activ_holerite', default=u'Se selecionado, Ativa a opção de holerite para todos os usuários do Myvindula no portal'),
                default=True
                )
    
    ativa_documents = schema.Bool(
                title=_(u'label_ativa_documents', default=u'Ativar a visualização de documentos no portal Myvindula'),
                description=_(u'help_activ_holerite', default=u'Se selecionado, Ativa a opção de documentos para todos os usuários do Myvindula no portal'),
                default=True
                )
    
    ativa_compartilhamento = schema.Bool(
                title=_(u'label_ativa_conpartilhamento', default=u'Ativar o compartilhamento nas redes sociais'),
                description=_(u'help_activ_share', default=u'Se selecionado, Ativa a opção de compartilhamento nas redes sociais de todos os itens "Noticia" do portal'),
                default=True
                )
    
    ativa_pensamentos = schema.Bool(
                title=_(u'label_ativa_pensamentos', default=u'Ativar a visualização dos pensametos no portal Myvindula'),
                description=_(u'help_activ_holerite', default=u'Se selecionado, Ativa a opção de pensamentos para todos os usuários do Myvindula no portal'),
                default=True
                )
    
    ativa_recados = schema.Bool(
                title=_(u'label_ativa_recados', default=u'Ativar os recados aos usuários do Myvindula no portal'),
                description=_(u'help_activ_share', default=u'Se selecionado, Ativa a opção de recados para todos os usuários do Myvindula no portal'),
                default=True
                )
    
    ativa_alert_first_access = schema.Bool(
            title=_(u'label_ativa_alert_first_access', default=u'Ativar a menssagem para o primeira cadastro no Myvindula'),
            description=_(u'help_ativa_alert_first_access', default=u'Se selecionado, Ativa a menssagem para o usuario fazer seu primeira cadastro do Myvindula no portal'),
            default=True
            )
    
    ativa_muit_user = schema.Bool(
                title=_(u'label_ativa_muit_user', default=u'Ativar o mecanismo para muitos usuários no myvindula'),
                description=_(u'help_ativa_muit_user', default=u'Se selecionado, Ativa a opção de muitos usuários no myvindula'),
                default=False
                )
    
    
    
class VindulaConfiguration(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('myvindula-conf-userpanel')
    
    ''' Metodos de Configuração do vindula '''

    def render(self):
        pass

    def configurador(self):
        if 'control-panel-objects' in  getSite().keys():
            control = getSite()['control-panel-objects']
            if 'vindula_vindulaconfigall' in control.keys():
                return control['vindula_vindulaconfigall']

            else:
                
                return False
        else:
            return False
    

    def config_muit_user(self):
        if self.configurador():
            control = self.configurador()
            return control.ativa_muit_user
        else:
            return False

    def check_share(self):
        if self.configurador():
            control = self.configurador()
            return control.ativa_compartilhamento
        else:
            return False

    
    def check_recados(self):
        if self.configurador():
            control = self.configurador()
            return control.ativa_recados
        else:
            return False

        
    def check_pensamentos(self):
        if self.configurador():
            control = self.configurador()
            return control.ativa_pensamentos
        else:
            return False
        
        
    def check_editfunc(self):
        if self.configurador():
            control = self.configurador()
            return control.ativa_editfunc

        else:
            return False
    
    def check_holerite(self):
        if self.configurador():
            control = self.configurador()
            return control.ativa_holerite
        else:
            return False
        
        
    def check_documents(self):
        if self.configurador():
            control = self.configurador()
            return control.ativa_documents
        else:
            return False   
    
    def check_alert_first_access(self):
        if self.configurador():
            control = self.configurador()
            return control.ativa_alert_first_access
        else:
            return False   
        
    
    
