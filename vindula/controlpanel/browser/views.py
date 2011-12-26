# -*- coding: utf-8 -*-
from five import grok
from zope.interface import Interface
from plone.app.layout.navigation.interfaces import INavigationRoot
from vindula.myvindula.user import BaseFunc
from vindula.controlpanel.browser.models import RegistrationCompanyInformation, ModelsProducts

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
        return RegistrationCompanyInformation().registration_processes(self)