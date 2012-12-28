# -*- coding: utf-8 -*-
from zope import schema
from plone.directives import form
from five import grok
from vindula.controlpanel import MessageFactory as _

from random import randint

from zope.interface import Interface
from zope.app.component.hooks import getSite, setSite

# Interface and schema

class IVindulaConfigAll(form.Schema):
    """ Vindula User Config """
    
    ativa_editfunc = schema.Bool(
                title=_(u'label_ativa_editfunc', default=u'Ativar a opção do usuário poder editar seu perfil'),
                description=_(u'help_activ_holerite', default=u'Caso selecionado ativa a opção do usuário poder editar seu perfil no Vindula'),
                default=True
                )
    
    ativa_holerite = schema.Bool(
                title=_(u'label_ativa_holerites', default=u'Ativar a visualização de holerites'),
                description=_(u'help_activ_holerite', default=u'Caso selecionado ativa a opção de holerite para todos os usuários do Vindula'),
                default=True
                )
    
    ativa_documents = schema.Bool(
                title=_(u'label_ativa_documents', default=u'Ativar a visualização de documentos'),
                description=_(u'help_activ_holerite', default=u'Caso selecionado ativa a opção de documentos para todos os usuários do Vindula'),
                default=True
                )
    
    ativa_compartilhamento = schema.Bool(
                title=_(u'label_ativa_conpartilhamento', default=u'Ativar o compartilhamento nas redes sociais'),
                description=_(u'help_activ_share', default=u'Caso selecionado ativa a opção de compartilhamento nas redes sociais\
                                                             de todos os itens "Página" do Vindula'),
                default=True
                )
    
    ativa_pensamentos = schema.Bool(
                title=_(u'label_ativa_pensamentos', default=u'Ativar a visualização dos pensametos'),
                description=_(u'help_activ_holerite', default=u'Caso selecionado ativa a opção de pensamentos para todos os usuários do Vindula'),
                default=True
                )
    
    ativa_recados = schema.Bool(
                title=_(u'label_ativa_recados', default=u'Ativar os recados aos usuários'),
                description=_(u'help_activ_share', default=u'Caso selecionado ativa a opção de recados para todos os usuários do Vindula'),
                default=True
                )
    
    ativa_alert_first_access = schema.Bool(
            title=_(u'label_ativa_alert_first_access', default=u'Ativar a mensagem para o primeiro cadastro'),
            description=_(u'help_ativa_alert_first_access', default=u'Caso selecionado ativa a mensagem para o usuário fazer\
                                                                      seu primeiro cadastro do Vindula'),
            default=True
            )
    
    ativa_muit_user = schema.Bool(
                title=_(u'label_ativa_muit_user', default=u'Ativar o mecanismo para muitos usuários'),
                description=_(u'help_ativa_muit_user', default=u'Caso selecionado ativa a opção de muitos usuários no Vindula'),
                default=False
                )
    
    ativa_filtro_busca_user = schema.Bool(
                title=_(u'label_ativa_filtro_busca_user', default=u'Altera o mecanismo do portlet busca de pessoas'),
                description=_(u'help_ativa_filtro_busca_user', default=u'Caso selecionado ativa o filtro para somente buscar os usuários\
                                                                         que possuam telefone cadastrado no perfil do Vindula'),
                default=False
                )

    ativa_recados_user_publicos = schema.Bool(
                title=_(u'label_ativa_recados_user_publicos', default=u'Ativa a opção de recados públicos aos usuários'),
                description=_(u'help_ativa_recados_user_publicos', default=u'Caso selecionado ativa a opção de recados visíveis a todos os usuários do Vindula'),
                default=False
                )
    
    ativa_richtext = schema.Bool(
                title=_(u'label_ativa_richtext', default=u'Ativar a opção do usuário poder editar os comentários com o Editor Ckeditor'),
                description=_(u'help_activ_holerite', default=u'Caso selecionado ativa a opção do usuário poder editar os comentários com o Editor Ckeditor'),
                default=False
                )
    
    ativa_MyvindulaPrivate = schema.Bool(
                title=_(u'label_ativa_MyvindulaPrivate', default=u'Restringe a visualização da tela Meu Perfil para usuários anônimos'),
                description=_(u'help_ativa_MyvindulaPrivate', default=u'Restringe a visualização da tela Meu Perfil para usuários anônimos,\
                                                                        ideal para "intranet privada" e "intranet + extranet"'),
                default=False
                )
    
    ativa_infoAutor = schema.Bool(
                title=_(u'label_ativa_infoAutor', default=u'Ativar visualização das informações auxiliares do conteúdo'),
                description=_(u'help_activa_infoAutor', default=u'Caso selecionado ativa a visualização das informações do autor e data de criação do conteúdo abaixo do título'),
                default=True
                )
    
    ativa_gravatar = schema.Bool(
                title=_(u'label_ativa_gravatar', default=u'Ativar a integração do Vindula com o gravatar.com'),
                description=_(u'help_activa_gravatar', default=u'Caso selecionado a foto do perfil do usuário será a foto definida Gravatar, a foto do Gravatar será exibida apenas \
                                                                 se o usuário não tiver uma foto já difinida no Vindula e tiver uma conta no Gravatar associada a seu email.\n\
                                                                 Esta funcionalidade requer conectividade do Vindula com o site gravatar.com.'),
                default=True
                )
    
    
class VindulaConfiguration(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('myvindula-conf-userpanel')
    
    ''' Metodos de Configuração do vindula '''

    def render(self):
        pass

    def update(self):
        site = getSite()
        #import pdb;pdb.set_trace()
        try:
            if site.portal_type != 'Plone Site':
                print " **** Alteração do GetSite ******** " + str(site) 
                setSite(site=self.context.portal_url.getPortalObject())
        except:
            setSite(site=self.context.portal_url.getPortalObject())


    def randomIdComents(self):
        return randint(1,1000) 

    def configurador(self):
        self.update()
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
    
    def check_filtro_busca_user(self):
        if self.configurador():
            control = self.configurador()
            return control.ativa_filtro_busca_user
        else:
            return False   
        
    def check_filtro_recados_user_publicos(self):
        if self.configurador():
            control = self.configurador()
            return control.ativa_recados_user_publicos
        else:
            return False
                    
    def check_ativa_richtext(self):
        if self.configurador():
            control = self.configurador()
            return control.ativa_richtext
        else:
            return False        
        
    def check_MyvindulaPrivate(self):
        if self.configurador():
            control = self.configurador()
            return control.ativa_MyvindulaPrivate
        else:
            return False                
        
    def check_ativa_infoAutor(self):
        if self.configurador():
            control = self.configurador()
            return control.ativa_infoAutor
        else:
            return True        
        
    def check_ativa_gravatar(self):
        if self.configurador():
            control = self.configurador()
            return control.ativa_gravatar
        else:
            return True        
        
        
    def check_myvindulaprivate_isanonymous(self):
        member = getSite().portal_membership
        if self.check_MyvindulaPrivate() and\
           member.isAnonymousUser():
            #executar redirect ao login
            return True
        return False
        
        
