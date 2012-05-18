# -*- coding: utf-8 -*-
from five import grok
from zope.interface import Interface
from plone.app.layout.navigation.interfaces import INavigationRoot
from Products.CMFCore.interfaces import ISiteRoot
from plone.app.layout.viewlets.interfaces import IAboveContent
from zope.app.component.hooks import getSite
from vindula.myvindula.user import BaseFunc, BaseStore

from Products.CMFCore.Expression import Expression
from Products.CMFCore.utils import getToolByName
from vindula.myvindula.validation import to_utf8, valida_form
from zope.app.component.hooks import getSite

from plone.registry.interfaces import IRegistry
from zope.component import queryUtility
from plone.app.discussion.interfaces import IDiscussionSettings
from Products.statusmessages.interfaces import IStatusMessage
from vindula.controlpanel import MessageFactory as _

from vindula.controlpanel.browser.models import RegistrationCompanyInformation, ModelsProducts, ModelsCompanyInformation

from Products.GenericSetup.interfaces import ISetupTool    
import pickle


class ControlPanelView(grok.View):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('vindula-control-panel')
    
    
class MacroLogoTopView(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('vindula-macro-logotop')
    
    
    def getOrgStrucContent(self):
        ctx = self.context.restrictedTraverse('OrgStruct_view')()
        portal = self.context.portal_url.getPortalObject();
        config_obj = portal['control-panel-objects']['vindula_themeconfig'];
        
        D = {}
        if ctx.portal_type != 'Plone Site':
            if ctx.activ_personalit:
                D['id'] = ctx.id 
                if ctx.getLogoPortal():
                    D['url'] = ctx.getLogoPortal().absolute_url()
                else:
                    if config_obj.getLogoCabecalho() is not None:
                        D['url']  =  config_obj.getLogo_top().absolute_url()
                    else:
                        D['url']  = "/++resource++vindula.controlpanel/logo_topo.png"
        return D
    
    
class MacroFooterView(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('vindula-macro-footer')
    
    
    def getOrgStrucContent(self):
        portal = self.context.portal_url.getPortalObject();
        config_obj = portal['control-panel-objects']['vindula_themeconfig'];

        ctx = self.context.restrictedTraverse('OrgStruct_view')()
        D = {}
        if ctx.portal_type != 'Plone Site':
            if ctx.activ_personalit:
                D['id'] = ctx.id 
                    
                if ctx.getLogoRodape():
                    D['url'] = ctx.getLogoRodape().absolute_url()
                else:
                    if config_obj.getLogoCabecalho() is not None:
                        D['url']  =  config_obj.getLogoCabecalho().absolute_url()
                    else:
                        D['url']  = "/++resource++vindula.controlpanel/logo_rodape.png"              
        
        return D
            
            
class ManageProductsView(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('vindula-manage-products')
            
    def updateProducts(self):
        portal_quickinstaller = self.context.portal_url.getPortalObject().portal_quickinstaller
        products = portal_quickinstaller.listInstallableProducts(skipInstalled=False)
        table_of_products = ModelsProducts()
        products_table = table_of_products.get_AllProducts()
        
        #Remove produtos a mais que possa existir no banco de dados.
        if products_table.count() > len(products):
            products_name = []
            for product in products:
                products_name.append(product['id'])
                
            for product_table in products_table:
                if product_table.name not in products_name:
                    table_of_products.store.remove(product_table)
                    table_of_products.store.flush()
        
        #Verifca se existem produtos novos adicionados ou se o status de algum foi alterado.
        for product in products:
            result = table_of_products.get_ProductsName(product['id'])
            if result.count() != 0 :
                installed = True if product['status'] == 'installed' else False
                if result.one().installed != installed:
                    setattr(result.one(), 'installed', installed)
            else:
                D = {}
                D['name']      = unicode(product['id'])
                D['title']     = unicode(product['title'])
                D['active']    = True
                D['installed'] = product['status'] == 'installed'
                
                table_of_products.set_Products(**D)
                

    def getProducts(self):
        self.updateProducts()
        form = self.request.form
        table_products = ModelsProducts()
        products = table_products.get_AllProducts()
        
        if 'save' in form.keys():
            if products:
                for product in products:
                    D = {}
                    D['id']        = product.id
                    D['name']      = product.name
                    D['title']     = product.title
                    D['installed'] = product.installed
                    if 'products' in form.keys() and str(product.id) in form.get('products'):
                        if not bool(product.active):
                            D['active']    = True
                    else:
                        if bool(product.active):
                            D['active']    = False

                    for column in D:
                        value = D.get(column, None)
                        setattr(product, column, value)
            
            
        products = table_products.get_AllProducts()
        L = []
        if products:
            for product in products:
                D = {}
                D['id']        = product.id 
                D['name']      = product.name
                D['title']     = product.title
                D['active']    = bool(product.active)
                D['installed'] = product.installed
                
                L.append(D)
            return L
        
        return None
    
class PrefsInstallProductsFormView(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('prefs_install_products_form')
    
    def getProductsEdited(self):
        all_products = ManageProductsView(self.context, self.request).getProducts()
        portal_quickinstaller = self.context.portal_url.getPortalObject().portal_quickinstaller
        
        products_intallable = portal_quickinstaller.listInstallableProducts()
        products_intalled = portal_quickinstaller.listInstalledProducts()
        
        
        products = {'installable': [], 'installed': []}
        
        
        for product in all_products:
            if product['active'] == True:
                if product['installed'] == False:
                    for product_intallable in products_intallable:
                        if product_intallable['id'] == product['name']:
                            products['installable'].append(product_intallable)
                else:
                    for product_intalled in products_intalled:
                        if product_intalled['id'] == product['name']:
                            products['installed'].append(product_intalled)
        
        return products          
    
    def render(self):
        pass

class CompanyInformation(grok.View, BaseFunc):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('vindula-company-information')
    
    def load_from(self):
        return ModelsCompanyInformation().get_CompanyInformation()
    

class ManageCompanyInformation(grok.View, BaseFunc):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('vindula-manage-company')
    
    def load_from(self):
        return RegistrationCompanyInformation().registration_processes(self)

#Views de renderização dos Logo da empresa --------------   
class CompanyInfImage(grok.View, BaseFunc):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('company-logo')
    
    def render(self):
        pass
    
    def update(self):
        form = self.request.form
        
        if 'id' in form.keys():
            id = form.get('id','0')
            campo_image = ModelsCompanyInformation().get_CompanyInformation_byID(int(id))

        elif 'cnpj' in form.keys():
            try: cnpj = unicode(form.get('cnpj',''))
            except: cnpj = form.get('cnpj','')  
            campo_image = ModelsCompanyInformation().get_CompanyInformation_by_CNPJ(cnpj)
        
        else:
            campo_image = None
        
        if campo_image:
            image = campo_image.logo_corporate
            x =  pickle.loads(image)
            filename = x['filename']
            self.request.response.setHeader("Content-Type", "image/jpeg", 0)
            #self.request.response.setHeader('Content-Disposition','attachment; filename=%s'%(filename))
            self.request.response.write(x['data'])
        
        else:
            self.request.response.write('')    
    
    
    
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

    def getConfigurador(self):
        if 'control-panel-objects' in  getSite().keys():
            control = getSite()['control-panel-objects']
            if 'vindula_alertdisplay' in control.keys():
                cong_alert = control['vindula_alertdisplay']
                return cong_alert
            else:
                return None
        else:
            return None

    def checkWorkflow(self):
        workflow = getSite().portal_workflow
        if 'vindula_intranet_workflow' in workflow.getDefaultChain():
            member = getSite().portal_membership.getAuthenticatedMember()
            #Caso de intranet restrita ao publico
            if member.getUserName() != 'Anonymous User':
                #user Logado
                return True
            else:
                #user Anonimo
                return False
        else:
            #Caso de intranet aberta ao publico
            return True

    def check(self):
        conf = self.getConfigurador()
        if conf:
            try: return conf.activ_display
            except: return None
            
    def type_message(self):
        conf = self.getConfigurador()
        if conf:
            return conf.type_messenger
    
    def title(self):
        conf = self.getConfigurador()
        if conf:
            return conf.title_messenger        
        
    def text(self):
        conf = self.getConfigurador()
        if conf:
            if conf.text_messenger:
                return conf.text_messenger.output
            
class StatusDataBaseView(grok.View):
    grok.context(ISiteRoot)
    grok.require('zope2.View')
    grok.name('vindula-status-DB')
    
    def load(self):
        sql = "show tables;"
        result=[]
        data = BaseStore().store.execute(sql)
        if data.rowcount != 0:
            for obj in data.get_all():
                result.append(obj[0])
        return result


class ManageLinksUserViewlet(grok.Viewlet):
    grok.name('vindula.controlpanel.linkuser') 
    grok.require('zope2.View')
    grok.viewletmanager(IAboveContent)     
    grok.context(Interface)
       
    def update(self):
        portal = getSite()
        workflow = portal['portal_workflow']
        
        membership = self.context.portal_membership
        groups = self.context.portal_groups
        
        user_login = membership.getAuthenticatedMember()
        user_groups = [i.id for i in groups.getGroupsByUserId(user_login.id) if i]
        
        L = []
        if 'control-panel-objects' in portal.keys():
            control = portal['control-panel-objects']
            if 'link-user-folder' in control.keys():
                folder_links = control['link-user-folder']
                links = folder_links.objectValues()
                for link in links:
                    checa = False
                    if workflow.getInfoFor(link, 'review_state') == 'published':
                       checa = True 
                    else:
                        if 'Manager' in user_login.getRoles():
                            checa = True
                        else:
                            for roles in link.get_local_roles():
                                if user_login.id in roles:
                                    checa = True
                                else:
                                    for group in user_groups:
                                        if group in roles:
                                            checa = True
                                            break
                        
                    if checa:
                        D ={}
                        D['url'] = link.getRemoteUrl()
                        D['title'] = link.Title()
                        L.append(D)
        
        return L

class ManageConfigBuscaView(grok.View):
    grok.name('vindula-confg-busca') 
    grok.require('zope2.View')
    grok.context(Interface)
    
    def render(self):
        pass

    def getConfigurador(self):
        if 'control-panel-objects' in  getSite().keys():
            control = getSite()['control-panel-objects']
            if 'vindula_themeconfig' in control.keys():
                conf_theme = control['vindula_themeconfig']
                return conf_theme.getAtiva_buscaAnonima()
            else:
                return None
        else:
            return None        


    def checkSearch(self):
        conf = self.getConfigurador()
        if conf:
            return True
        else:
            member = getSite().portal_membership.getAuthenticatedMember()
            #Caso de intranet restrita ao publico
            if member.getUserName() != 'Anonymous User':
                #user Logado
                return True
            else:
                #user Anonimo
                return False
            
    def checkSearchRediret(self):
        conf = self.checkSearch()
        request = self.context.REQUEST
        if not conf:
            url = getSite().portal_url() + '/acl_users/credentials_cookie_auth/require_login?came_from='+request.getURL()
            request.response.redirect(url)
