# -*- coding: utf-8 -*-
from five import grok
from zope.interface import Interface
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.layout.viewlets.interfaces import IAboveContent
from zope.app.component.hooks import getSite
from vindula.myvindula.user import BaseFunc

from plone.registry.interfaces import IRegistry
from zope.component import queryUtility
from plone.app.discussion.interfaces import IDiscussionSettings
from Products.statusmessages.interfaces import IStatusMessage
from vindula.controlpanel import MessageFactory as _

from vindula.controlpanel.browser.models import RegistrationCompanyInformation


class ControlPanelView(grok.View):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('vindula-control-panel')
    
    
class MacroLogoTopView(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('vindula-macro-logotop')
    
    
class MacroFooterView(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('vindula-macro-footer')
    
class CompanyInformation(grok.View, BaseFunc):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('vindula-company-information')
    
    def load_from(self):
        return RegistrationCompanyInformation().registration_processes(self)
    
class CommentsConfigView(grok.View, BaseFunc):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('vindula-comments-configuration')
    
    campos = {'globally_enabled': {'required': False, 'type' : bool},}
    
    def load_from(self):
        form = self.request # var tipo 'dict' que guarda todas as informacoes do formulario (keys,items,values)
        form_keys = form.keys() # var tipo 'list' que guarda todas as chaves do formulario (keys)
        #success_url = self.context.absolute_url() + '/@@vindula-control-panel'
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IDiscussionSettings, check=False)
        
        # divisao dos dicionarios "errors" e "convertidos"
        form_data = {
            'data': {},
            'campos':self.campos,}
        
        # se clicou no botao "Salvar"
        if 'form.submited' in form_keys:
        
            if 'globally_enabled' in form_keys:
                settings.globally_enabled = True
            else:
                settings.globally_enabled = False
            
            #Redirect back to the front page with a status message
            IStatusMessage(self.request).addStatusMessage(_(u"Configuração alterada com sucesso."), "info")
            #self.request.response.redirect(success_url)      
        else:
            D = {}
            D['globally_enabled'] = settings.globally_enabled
            form_data['data'] = D
            
            return form_data

# Viewlet for menu and sub menu
class AlertDisplayViewlet(grok.Viewlet):
    grok.context(Interface) 
    grok.name('vindula.alert.display') 
    grok.require('zope2.View')
    grok.viewletmanager(IAboveContent) 

    def check(self):
        conf = getSite()['control-panel-objects']['vindula_alertdisplay']
        if conf:
            return conf.activ_display
        
    def type_message(self):
        conf = getSite()['control-panel-objects']['vindula_alertdisplay']
        if conf:
            return conf.type_messenger
    
    def title(self):
        conf = getSite()['control-panel-objects']['vindula_alertdisplay']
        if conf:
            return conf.title_messenger        
        
    def text(self):
        conf = getSite()['control-panel-objects']['vindula_alertdisplay']
        if conf:
            return conf.text_messenger.output
