# -*- coding: utf-8 -*-
import pickle, string
import json
import urllib2
import re
import unicodedata
from random import randint

from copy import copy
from datetime import datetime
from random import choice

import pkg_resources
from AccessControl import getSecurityManager
from Acquisition import aq_inner
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.permissions import ManagePortal
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from collective.plonefinder.browser.finder import Finder
from five import grok
from plone.app.discussion.interfaces import IDiscussionSettings
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.layout.viewlets.interfaces import IBelowContentBody, IAboveContent
from plone.app.users.browser.register import BaseRegistrationForm, CantSendMailWidget
from plone.registry.interfaces import IRegistry
from vindula.content.content.interfaces import IVindulaNews
from vindula.content.models.content import ModelsContent
from vindula.myvindula.models.dados_funcdetail import ModelsDadosFuncdetails
from vindula.myvindula.models.required_reading_data import RequiredReadingData
from vindula.myvindula.user import BaseFunc, BaseStore
from zope.app.component.hooks import getSite
from zope.browsermenu.interfaces import IBrowserMenu
from zope.component import queryUtility, getUtility, getMultiAdapter
from zope.formlib import form
from zope.interface import Interface
from plone.i18n.normalizer.interfaces import IIDNormalizer

from vindula.controlpanel import MessageFactory as _
from vindula.controlpanel.browser.models import RegistrationCompanyInformation, ModelsProducts, ModelsCompanyInformation


#Imports para criar a tela de Criar Usuário do Plone

# from vindula.myvindula.registration import SchemaFunc
class ControlPanelView(grok.View):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('vindula-control-panel')

    def update(self):
        url = self.context.absolute_url() + '/@@overview-controlpanel'
        self.request.response.redirect(url)

    def getVindulaVersion(self):
        try:
            return 'Vindula %s' % pkg_resources.get_distribution('Vindula.MyVindula').version
        except Exception as error:
            print error
            return 'Não encontrada'

class ManageContentTypesView(grok.View):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('manage-content-types')

class ManageContentTagsView(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('manage-content-tags')

class ManageTagsView(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('manage-tags')

class VindulaFinderUploadView(Finder):
    """ Custom Finder class for widget """

    def __init__(self, context, request):
        super(VindulaFinderUploadView, self).__init__(context, request)
        self.findername = 'refbrowser_finder'
        self.multiselect = True

        self.allowupload = True
        self.allowaddfolder = True
        self.allowimagesizeselection = False
        self.review_state = ''

        #self.query = {'review_state':'published'}

        context = aq_inner(context)

    def __call__(self):
        # redefine some js methods (to select items ...)
        request = aq_inner(self.request)
        self.jsaddons = self.get_jsaddons()
        self.cssaddons = '''
                            .popup .browserStatic {background: none;}
                         '''

        self.review_state = request.get('review_state', self.review_state)


        return super(VindulaFinderUploadView, self).__call__()

    def _quotestring(self, s):
        return '"%s"' % s

    def _quote_bad_chars(self, s):
        bad_chars = ["(", ")"]
        for char in bad_chars:
            s = s.replace(char, self._quotestring(char))
        return s

    def finderQuery(self, topicQuery=None):
        """
        return query for results depending on some params
        """
        request = self.request
        if self.query:
            return self.query
        elif self.typeview == 'selection':
            return {'uid': self.blacklist}
        elif self.displaywithoutquery or self.searchsubmit:
            query = {}
            path = {}
            if not self.searchsubmit:
                path['depth'] = 1
            path['query'] = self.browsedpath
            query['path'] = path
            sort_index = self.sort_on
            if self.sort_withcatalog:
                query['sort_on'] = sort_index
                query['sort_order'] = self.sort_order
            if self.types:
                query['portal_type'] = self.types

            if self.searchsubmit:
                # TODO : use a dynamic form
                # with different possible searchform fields
                q = request.get('SearchableText', '')
                q = q.encode('raw_unicode_escape').decode('utf-8')
                if q:
                    for char in '?-+*':
                        q = q.replace(char, ' ')
                    r = q.split()
                    r = " AND ".join(r)
                    searchterms = self._quote_bad_chars(r) + '*'

                    query['SearchableText'] = searchterms

            if self.review_state:
                    query['review_state'] = self.review_state

            for key in query.keys():
                if not query.get(key): query.pop(key)

            return query

    def get_jsaddons(self):
        """ redefine selectItem method in js string """

        jsstring = """
            function getUrlVars() {
                    var vars = {};
                    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi,function(m,key,value) {
                        vars[key] = value;
                    });
                return vars;
            }

        selectCKEditorItem = function (selector, title) {
                        var nameField = getUrlVars()['fieldName'];
                        var multi = parseInt(getUrlVars()['mult']);

                        window.opener.RefBrowserWidget_setReference('ref_browser_'+nameField,selector,title,multi);
                        window.opener.RefBrowserWidget_ajaxObjSelect(nameField,selector);
                        if (!multi){
                            window.close();
                        }else{
                           alert('Conteúdo '+title+' adicionado.');
                        };
                     };

        Browser.selectItem = selectCKEditorItem;
             """
        return jsstring




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
        data = self.generate_random_string(13)
        sql = 'SELECT * FROM vinapp_myvindula_userschemadata WHERE username = "%s";' %(data)
        result=[]
        data = BaseStore().store.execute(sql)
        if data.rowcount != 0:
            for obj in data.get_all():
                result.append(obj[0])

        return result


    def generate_random_string(self, length, stringset=string.letters + string.digits):
        '''
        Returns a string with `length` characters chosen from `stringset`
        >>> len(generate_random_string(20) == 20
        '''
        return ''.join([choice(stringset) for i in range(length)])



class ManageConfigBuscaView(grok.View):
    grok.name('vindula-confg-busca')
    grok.require('zope2.View')
    grok.context(Interface)

    def render(self):
        pass

    def getConfigurador(self):
        if 'control-panel-objects' in  getSite().keys():
            control = getSite()['control-panel-objects']
            if 'ThemeConfig' in control.keys():
                conf_theme = control['ThemeConfig']
                return conf_theme
            else:
                return None
        else:
            return None


    def checkSearch(self):
        conf = self.getConfigurador()

        if conf:
            if conf.getAtiva_buscaAnonima():
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
        else:
            return True

    def _getTypeSearch(self):
        conf = self.getConfigurador()
        if conf:
            type_search = conf.getTipo_buscaPortal()
            return type_search

        return None

    def checkType01(self):
        type_search = self._getTypeSearch()
        if type_search:
            if type_search == 'search_01':
                return True
            else:
                return False
        else:
            return True

    def checkType02(self):
        type_search = self._getTypeSearch()
        if type_search:
            if type_search == 'search_02':
                return True
            else:
                return False
        else:
            return False


    def checkSearchRediret(self):
        conf = self.checkSearch()
        request = self.context.REQUEST
        if not conf:
            url = getSite().portal_url() + '/acl_users/credentials_cookie_auth/require_login?came_from='+request.getURL()
            request.response.redirect(url)


class ManagePortletView(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('vindula-manage-portlet')

    def render(self):
        pass

    def getUrlManagePortlet(self,portlet):
        portal = self.context.portal_url.getPortalObject()

        baseUrl = portal.absolute_url()+ '/' + '/'.join(portlet['key'].split('/')[2:])
        manager = portlet['manager']
        name = portlet['name']
        refererUrl = self.context.absolute_url()

        url = '%s/++contextportlets++%s/%s/edit?referer=%s' % (baseUrl, manager,name,refererUrl)

        return url


class CustomLoginView(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('vindula-custom-login')

    def getControlPanelObjects(self):
        if 'control-panel-objects' in  getSite().keys():
            return getSite().get('control-panel-objects')
        return None

    def getThemeConfObj(self):
        control = self.getControlPanelObjects()
        if 'ThemeConfig' in control.keys():
            return control.get('ThemeConfig')
        return None

    def getLoginConfObj(self):
        control = self.getControlPanelObjects()
        if control:
            if 'ThemeLoginConfig' in control.keys():
                return control.get('ThemeLoginConfig')
        return None

    #Metodo retorna verdadeiro caso o tipo de login nao for grafico nem personalizado
    def getLoginGrafico(self):
        conf_login = self.getLoginConfObj()
        if conf_login:
            if conf_login.getTipoLogin() != 'classico':
                return True
        return None

    def getUrlImageBackground(self):
        conf_login = self.getLoginConfObj()
        if conf_login:
            img = conf_login.getImagemBackground()
            if img:
                return img.absolute_url()
        return None

    def getOpacityBox(self):
        conf_login = self.getLoginConfObj()
        if conf_login:
            try:
                type = float(conf_login.getOpacityBox())
                if type >= 0 and type <= 1:
                    return 'opacity: %s;' % (type)
            except:
                pass

        return None


    def getTypeBackground(self):
        conf_login = self.getLoginConfObj()
        if conf_login:
            type = conf_login.getPosicaoImagem()
            if type == 'centro':
                return 'background: url("%s") no-repeat scroll center center %s' % (self.getUrlImageBackground() or '', conf_login.getCorSolidaBackground() or 'transparent')
            elif type == 'lado_lado':
                return 'background: url("%s") repeat scroll 0 0 %s' % (self.getUrlImageBackground() or '', conf_login.getCorSolidaBackground() or 'transparent')
            elif type == 'estender':
                color = conf_login.getCorSolidaBackground()
                if color and color != 'transparent':
                    return 'background: repeat scroll 0 0 %s' % (conf_login.getCorSolidaBackground())
        return None

    def getEstiloLoginCustomizado(self):
        conf_login = self.getLoginConfObj()
        css = ''
        if conf_login:
            for linha in conf_login.getCustomCSS():
                css += linha
        return css

class CustomCssLogin(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('custom-login-dynamic.css')

    def render(self):
        css = """
            input[type="text"]:focus,
            textarea:focus,
            input[type="password"]:focus {
                border-color: %(portal_color)s !important;
            }

            .formControls input[type="submit"] { background-color: %(portal_color)s; border-color: %(portal_color)s }

        """ % {'portal_color': self.getPortalColor()}

        self.response.setHeader('Content-Type', 'text/css; charset=UTF-8')
        return css


    def getThemeConfObj(self):
        control = self.getControlPanelObjects()
        if 'ThemeConfig' in control.keys():
            return control.get('ThemeConfig')
        return None

    def getPortalColor(self):
        portal_color = self.getThemeConfObj().getCorGeralPortal()
        return portal_color == 'transparent' and 'none' or portal_color

    def getControlPanelObjects(self):
        if 'control-panel-objects' in  getSite().keys():
            return getSite().get('control-panel-objects')
        return None


class VindulaPortletPrefs(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('vindula_portlet_prefs')

    def getControlPanelObjects(self):
        if 'control-panel-objects' in  getSite().keys():
            return getSite().get('control-panel-objects')
        return None

    def getDicTopics(self):
        control = self.getControlPanelObjects()
        if control and control.get('ContainerTopicsControlPanel') and control.get('ContainerTopicsControlPanel').contentValues():
            topics = control.get('ContainerTopicsControlPanel').contentValues({'portal_type': 'TopicControlPanel'})
            if topics:
                list_topics = []
                for topic in topics:
                    dic_topic = {}
                    dic_topic['topic'] = topic
                    dic_topic['subtopics'] = []
                    subtopics = topic.contentValues({'portal_type': 'SubtopicControlPanel'})
                    if subtopics:
                        for subtopic in subtopics:
                            dic_topic['subtopics'].append(subtopic)
                    list_topics.append(dic_topic)
                return list_topics
        return None

    def getSelected(self, topico):
        url = self.request.URL
        url_topico = '%s/%s' % (self.context.portal_url(), topico.getViewName())
        if url_topico == url:
            return True
        return False

    def getAccessTopic(self, topic, super=False):
        groups_tool = getToolByName(getSite(), 'portal_groups')
        member = getSite().portal_membership.getAuthenticatedMember()
        groups_user = [i.id for i in groups_tool.getGroupsByUserId(member.getUserName())]

        try:
            topic.portal_url()
        except:
            dict_topics = self.getDicTopics()
            url_topic = topic.getURL().replace(getSite().portal_url()+'/', '')
            if dict_topics:
                topic = None
                for lis_topic in dict_topics:
                    for subtopic in lis_topic['subtopics']:
                        view_name = subtopic.getViewName()
                        if view_name == url_topic:
                            topic = subtopic
                            super = self.getAccessTopic(lis_topic['topic'])
                            break
                    if topic:
                        break

        if super:
            return True
        elif topic:
            try:
                if topic.getUseSuperiorGroups():
                    topic_access = topic.getUsersOrGroupsTopic()
                else:
                    topic_access = topic.getUsersOrGroupsSub()
            except:
                topic_access = topic.getUsersOrGroupsTopic()

            if member.id in topic_access:
                return True
            else:
                for group in groups_user:
                    if group in topic_access:
                        return True
            return False
        else:
            return False

    def hasSubTopicActive(self, topic):
        for subtopic in topic.contentValues({'portal_type': 'SubtopicControlPanel'}):
            if self.getAccessTopic(subtopic):
                return True
        return False

# Codigo comentado pois a funcionalidade nao vai ser utilizada no momento

#class LinkEditContent(grok.Viewlet):
#    grok.context(Interface)
#    grok.name('vindula.controlpanel.linkeditcontent')
#    grok.require('cmf.ManagePortal')
#    grok.viewletmanager(IBelowContent)
#
#    def getContentEdit(self):
#        request = self.request
#        pc = getSite().portal_catalog
#        url = request.URL.replace(getSite().portal_url()+'/', '')
#        results = pc({'portal_type': 'SubtopicControlPanel'})
#
#        if self.context.portal_type not in ('SubtopicControlPanel', 'TopicControlPanel',) and url:
#            for result in results:
#                result = result.getObject()
#                view_name = result.getViewName()
#                if view_name and view_name in url:
#                    return result.absolute_url() + '/edit'
#
#        return None

class ShowAllRolesUsersView(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('usergroup-userprefs-all')

class EditVindulaColorsView(grok.View):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('edit-vindula-colors')

class WebServiceControlPanelView(grok.View):
    grok.context(ISiteRoot)
    grok.require('cmf.ManagePortal')
    grok.name('ws-control-panel')

#Visao de unidades INATIVAS, ou seja unidades que existem no Plone porém foi excluida no Django
class InactiveStructuresView(grok.View):
    grok.context(ISiteRoot)
    grok.require('cmf.ManagePortal')
    grok.name('inactive-structures')

    def getInactiveStructures(self):
        data =  ModelsContent.getAllByContentType(type='OrganizationalStructure', deleted=True)
        p_catalog = getToolByName(self.context, 'portal_catalog')
        items = []
        UID_list = []

        for item in data:
            if item.uid not in UID_list:
                UID_list.append(item.uid)

        if UID_list:
            items = p_catalog(porta_type='OrganizationalStructure',
                              UID=UID_list,
                              sort_on='sortable_title',
                              sort_order='ascending')

            #Garantindo que irá retornar somente tipos OrganizationalStructure, pois o catalog pode trazer conteudos dentro de unidades organizacionais
            items = [i.getObject() for i in items if i.getObject().portal_type == 'OrganizationalStructure']

        return items


#Criacao do formulário de adicionar usuários do plone customizada
class IAddUserSchema(Interface):
    pass

class AddUserForm(BaseRegistrationForm):

    label = _(u'heading_add_user_form', default=u'Add New User')
    description = u""
    template = ViewPageTemplateFile('views_templates/newuser_form.pt')

    @property
    def form_fields(self):
        defaultFields = super(AddUserForm, self).form_fields

        # The mail_me field needs special handling depending on the
        # validate_email property and on the correctness of the mail
        # settings.
        portal = getUtility(ISiteRoot)
        ctrlOverview = getMultiAdapter((portal, self.request),
                                       name='overview-controlpanel')
        mail_settings_correct = not ctrlOverview.mailhost_warning()
        if not mail_settings_correct:
            defaultFields['mail_me'].custom_widget = CantSendMailWidget
        else:
            # Make the password fields optional: either specify a
            # password or mail the user (or both).  The validation
            # will check that at least one of the options is chosen.
            defaultFields['password'].field.required = False
            defaultFields['password_ctl'].field.required = False
            if portal.getProperty('validate_email', True):
                defaultFields['mail_me'].field.default = True
            else:
                defaultFields['mail_me'].field.default = False

        # Append the manager-focused fields
        allFields = defaultFields + form.Fields(IAddUserSchema)
        return allFields

    @form.action(_(u'label_register', default=u'Register'),
                 validator='validate_registration', name=u'register')
    def action_join(self, action, data):
        super(AddUserForm, self).handle_join_success(data)
        portal_groups = getToolByName(self.context, 'portal_groups')
        user_id = data['username']
        is_zope_manager = getSecurityManager().checkPermission(ManagePortal, self.context)

        try:
            # Add user to the selected group(s)
            if 'groups' in data.keys():
                for groupname in data['groups']:
                    group = portal_groups.getGroupById(groupname)
                    if 'Manager' in group.getRoles() and not is_zope_manager:
                        raise Forbidden

                    portal_groups.addPrincipalToGroup(user_id, groupname, self.request)
        except (AttributeError, ValueError), err:
            IStatusMessage(self.request).addStatusMessage(err, type="error")
            return

        # SchemaFunc().registration_processes(data, user_id, True)
        dados = {u'username':self.unicode(user_id),
                 u'email':self.unicode(data.get('email','')),
                 u'name':self.unicode(data.get('fullname',user_id))}

        user_schema = ModelsDadosFuncdetails()
        user_schema.createUserProfile(dados)


        IStatusMessage(self.request).addStatusMessage(
            _(u"User added."), type='info')
        self.request.response.redirect(
            self.context.absolute_url() +
            '/@@usergroup-userprefs?searchstring=' + user_id)


    def unicode(self,valor):
        if valor:
            if type(valor) == unicode:
                return valor
            else:
                return unicode(valor,'utf-8')
        else:
            return u''

class ContentMenu(BrowserView):
    def getMenuItems(self):
        menu = getUtility(IBrowserMenu, name='plone_contentmenu')
        items = menu.getMenuItems(self.context, self.request)
        items.reverse()
        dic_categorias = {}

        obj_vindula_categories = getSite().get('control-panel-objects', None)
        if obj_vindula_categories:
            obj_vindula_categories = obj_vindula_categories.get('vindula_categories', None)
            if obj_vindula_categories and obj_vindula_categories.portal_type == 'VindulaCategories':
                conf_additems = obj_vindula_categories.getCategories_additem()
                for item in conf_additems:
                    categoria = item.get('catagories')
                    if dic_categorias.get(categoria):
                        dic_categorias[categoria].append(item.get('content_type'))
                    else:
                        dic_categorias[categoria] = [item.get('content_type')]

        if dic_categorias:
            for item in items:
                if item['extra']['id'] == 'plone-contentmenu-factories':
                    list_aux = copy(item['submenu'])
                    for key in reversed(obj_vindula_categories.getCategories().keys()):
                        if dic_categorias.get(key, None):
                            for submenu in list_aux:
                                if submenu.get('id', None) and submenu['id'].lower() in dic_categorias[key]:
                                    category = [menu for menu in item['submenu'] if menu.get('id', None) == key]
                                    if not category:
                                        new_category = {'action': None,
                                                        'description': '',
                                                        'extra': {'class': 'dropdownAddContent positionRelative',
                                                                           'id': 'dropdownAddContent',
                                                                           'separator': None},
                                                        'icon': '',
                                                        'id':  key,
                                                        'selected':  False,
                                                        'submenu': [],
                                                        'title': key}

                                        item['submenu'].insert(0, new_category)
                                        index = item['submenu'].index(new_category)
                                    else:
                                        index = item['submenu'].index(category[0])

                                    item['submenu'][index]['submenu'].append(submenu)
                                    item['submenu'].remove(submenu)

        return items


class ThemeView(grok.View):
    grok.context(ISiteRoot)
    grok.require('zope2.View')
    grok.name('theme-view')



class ReadMoreViewlet(grok.Viewlet):
    grok.context(IVindulaNews)
    grok.name('vindula.controlpanel.readmore')
    grok.require('zope2.View')
    grok.viewletmanager(IBelowContentBody)

    def getReadMore(self):
        news = list(self.catalogNews(context=self.context, withKeywords=True))
        results = []
        [results.append(new) for new in news if new.getObject() != self.context]

        return results

    def catalogNews(self, context=None, withKeywords=False):
        p_catalog = getSite().portal_catalog
        if not context:
            context = self.context

        query = {}
        query['portal_type'] = ['VindulaNews', 'News Item']
        query['sort_order'] = 'descending'
        if withKeywords:
            query['Subject'] = context.getRawSubject()
        query['sort_on'] = 'effective'
        query['review_state'] = ['published', 'external']

        return p_catalog(**query)

class SeeAlsoViewlet(grok.Viewlet):
    grok.context(IVindulaNews)
    grok.name('vindula.controlpanel.seealso')
    grok.require('zope2.View')
    grok.viewletmanager(IBelowContentBody)

    def getSeeAlso(self):
        news = list(self.catalogNews(context=self.context))
        results = []
        if self.context.ThemeNews():
            for item in news:
                obj = item.getObject()
                if obj.portal_type == 'VindulaNews':
                    if obj == self.context or not obj.ThemeNews():
                       continue
                    else:
                        for tema in obj.ThemeNews():
                            if tema in self.context.ThemeNews():
                                results.append(item)
        return results

    def catalogNews(self, context=None, withKeywords=False):
        p_catalog = getSite().portal_catalog
        if not context:
            context = self.context

        query = {}
        query['portal_type'] = ['VindulaNews', 'News Item']
        query['sort_order'] = 'descending'
        if withKeywords:
            query['Subject'] = context.getRawSubject()
        query['sort_on'] = 'effective'
        query['review_state'] = ['published', 'external']

        return p_catalog(**query)

class StaticBarViewletManager(grok.ViewletManager):
    """ This viewlet manager is responsible for all gomobiletheme.basic viewlet registrations.

    Viewlets are directly referred in main_template.pt by viewlet name,
    thus overriding Plone behavior to go through ViewletManager render step.
    """
    grok.context(Interface)
    grok.name('vindula.network.staticbarviewletmanager')

class ContainerBeforeContentViewletManager(grok.ViewletManager):
    """
        Viewlets are directly referred in main_template.pt by viewlet name,
        thus overriding Plone behavior to go through ViewletManager render step.
    """
    grok.context(Interface)
    grok.name('vindula.controlpanel.containerbeforecontent.viewletmanager')

class RequiredReadingViewlet(grok.Viewlet):
    grok.context(Interface)
    grok.name('vindula.controlpanel.requiredreading')
    grok.require('zope2.View')
    grok.viewletmanager(ContainerBeforeContentViewletManager)


    def getMyRequiredDocuments(self):
        p_catalog = getToolByName(self.context, 'portal_catalog')
        g_tool = getToolByName(self.context, 'portal_groups')
        m_tool = getToolByName(self.context, 'portal_membership')

        brains = p_catalog(requiredReading=True,
                           review_state=['published', 'internally_published', 'external'])
        my_username = m_tool.getAuthenticatedMember().getUserName()
        my_required_docs = []

        for brain in brains:
            obj = brain.getObject()
            try:
                if (not obj.getStartDateReqRead() and not obj.getExpirationDateReqRead()) \
                   or obj.getStartDateReqRead().asdatetime().replace(tzinfo=None) < datetime.now() < obj.getExpirationDateReqRead().asdatetime().replace(tzinfo=None):

                    if obj.getUsersGroupsReqRead():
                        for id_user in obj.getUsersGroupsReqRead():
                            if g_tool.getGroupById(id_user):
                                if my_username in g_tool.getGroupById(id_user).getGroupMemberIds() \
                                   and obj not in my_required_docs:
                                    my_required_docs.append(obj)
                            else:
                                if id_user == my_username \
                                   and obj not in my_required_docs:
                                    my_required_docs.append(obj)

                    #Eh leitura obrigatoria para todo mundo
                    else:
                        my_required_docs.append(obj)
            except:
                return []

        if my_required_docs:
            aux_list_docs = copy(my_required_docs)
            m_tool = getToolByName(self.context, 'portal_membership')
            my_username = m_tool.getAuthenticatedMember().getUserName()

            for doc in aux_list_docs:
                model_content = ModelsContent().getContent_by_uid(doc.UID())

                if model_content and \
                   RequiredReadingData.getData(username=my_username, content=model_content):
                    my_required_docs.remove(doc)

        return my_required_docs

class CheckRequiredReadingView(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('check-required-reading')

    def isRequiredReading(self):
        g_tool = getToolByName(self.context, 'portal_groups')

        if getattr(self.context, "requiredReading", False):
            context = self.context

            if (not context.getStartDateReqRead() and not context.getExpirationDateReqRead()) \
               or context.getStartDateReqRead().asdatetime().replace(tzinfo=None) < datetime.now() < context.getExpirationDateReqRead().asdatetime().replace(tzinfo=None):
                if context.getUsersGroupsReqRead():
                    m_tool = getToolByName(self.context, 'portal_membership')
                    my_username = m_tool.getAuthenticatedMember().getUserName()
                    for id_user in context.getUsersGroupsReqRead():
                        if g_tool.getGroupById(id_user):
                            if my_username in g_tool.getGroupById(id_user).getGroupMemberIds():
                               return True
                        else:
                            if id_user == my_username:
                               return True
                else:
                    return True

        return False

    def getDataRead(self):
        m_tool = getToolByName(self.context, 'portal_membership')
        my_username = m_tool.getAuthenticatedMember().getUserName()
        model_content = ModelsContent().getContent_by_uid(self.context.UID())
        mark_read = self.request.get('read', False)

        if model_content:
            data = None
            if mark_read:
                return RequiredReadingData().setReadingData(username=my_username, content=model_content, is_read=True)

            if not data:
                data = RequiredReadingData.getData(username=my_username, content=model_content)
                if data:
                    data = data[0]
                return data

class CheckRequiredReadingViewlet(grok.Viewlet):
    grok.context(Interface)
    grok.name('vindula.controlpanel.checkrequiredreading')
    grok.require('zope2.View')
    grok.viewletmanager(IBelowContentBody)




class CreateNewsFromURLView(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('create-news-url')

    def generate_id(self, contexto, titulo, random=False):
        normalizer = getUtility(IIDNormalizer)
        new_id = normalizer.normalize(titulo)
        if random:
            new_id += str(randint(1, 1000))

        if getattr(contexto, new_id, False):
            return self.generate_id(contexto, titulo, True)
        else:
            return new_id

    def load_data(self):
        url = []
        Pagina = []
        normalizer = getUtility(IIDNormalizer)
        if self.request.form:
            if self.request.form['url_json']:
                urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', self.request.form['url_json'])
                if urls:
                    url = self.request.form['url_json']

        if url:
            try:
                urlJSON = urllib2.urlopen(url)
                Read_urlJSON = urlJSON.read()
                json_dumps = json.dumps(Read_urlJSON)
                json_load = json.loads(json_dumps)
                Dict_JSON = json.loads(json_load)

                try:
                    self.context.invokeFactory( type_name="VindulaFolder",
                                                id="PaginasImportadas",
                                                title="Páginas Importadas",
                                                description="Lista de todas as páginas importadas")
                except:
                    pass
                HTML_reads = []
                Pagina = []
                for obj in Dict_JSON:
                    url_access = obj['urlContent']
                    # id_pasta = obj['keyCode']
                    # self.context.PaginasImportadas.invokeFactory(type_name="VindulaFolder", id=id_pasta,
                    #                                                                         title=obj['edicao'],
                    #                                                                         description="Pasta de conteúdos")
                    content_html = urllib2.urlopen(url_access).read()
                    HTML_dumps = json.dumps(content_html)
                    HTML_loads = json.loads(HTML_dumps)
                    HTML_reads.append(json.loads(HTML_loads))

                    for content in HTML_reads:
                        for HTML_content in content:
                            HTML_content['titulo'].encode('utf-8')
                            HTML_content['conteudo'].encode('utf-8')
                            Pagina.append(HTML_content)
                for pagina in Pagina:
                    id_titulo = normalizer.normalize(pagina['titulo'])
                    id_pagina = pagina['keyCode'] + id_titulo
                    if getattr(self.context.PaginasImportadas, id_pagina, False):
                        pass
                    else:
                        self.context.PaginasImportadas.invokeFactory(type_name="VindulaNews",id=id_pagina,
                                                                                            title=pagina['titulo'],
                                                                                            description=pagina['resumo'],
                                                                                            text=pagina['conteudo'])
                data = "Páginas importadas com sucesso"
            except:
                data = "URL inválida ou as Páginas contidas no arquivo Json já existem"
                pass
        else:
            data = "Digite uma url válida"
        return data