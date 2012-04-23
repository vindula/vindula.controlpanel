# -*- coding: utf-8 -*-
from five import grok
from vindula.controlpanel import MessageFactory as _
from Products.CMFCore.utils import getToolByName
from zope.app.component.hooks import getSite
 
from AccessControl import ClassSecurityInfo
from zope.interface import Interface

from vindula.controlpanel.content.interfaces import IThemeConfig
from Products.ATContentTypes.content.document import ATDocumentSchema
from Products.ATContentTypes.content.document import ATDocumentBase
from Products.SmartColorWidget.Widget import SmartColorWidget

from zope.interface import implements
from Products.Archetypes.atapi import *
from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from vindula.controlpanel.config import *

# Interface and schema
ThemeConfig_schema =  ATDocumentSchema.copy() + Schema((

    BooleanField(
        name='ativa_menudropdown',
        default=False,
        widget=BooleanWidget(
            label="Ativar Menu Dropdown",
            description='Se selecionado, Ativa o Menu DropDown do Portal.',
        ),
      
    ),
    

    ReferenceField('logoCabecalho',
        multiValued=0,
        allowed_types=('Image'),
        label=_(u"Logo Cabecalho"),
        relationship='logoPortal',
        widget=ReferenceBrowserWidget(
            default_search_index='SearchableText',
            label=_(u"Logo Cabecalho"),
            description='A imagem selecionada será exibida no topo do portal.'),
    ),
                                                                   
    ReferenceField('logoRodape',
        multiValued=0,
        allowed_types=('Image'),
        label=_(u"Logo Rodapé "),
        relationship='logoRodape',
        widget=ReferenceBrowserWidget(
            default_search_index='SearchableText',
            label=_(u"Logo Rodapé"),
            description='A imagem selecionada será exibida no rodapé do portal.'),
    ),
    
    ReferenceField('favicon',
        multiValued=0,
        allowed_types=('Image'),
        label=_(u"Favicon"),
        relationship='favicon',
        widget=ReferenceBrowserWidget(
            default_search_index='SearchableText',
            label=_(u"Favicon"),
            description='Logo que será exibido no topo da aba do navegador.'),
    ),                                                                   

    StringField(
        name='itens_menu',
        widget=PicklistWidget(
            label=_(u"Itens do Menu"),
            description=_(u"Selecione os tipos de itens que serão apresentados no menu e no sub-menu."),
            format = 'select',
        ),
        vocabulary='voc_itens_menu',
        required=False,
    ),
    
    IntegerField(
        name='larguraPortal',
        required=0,
        widget=IntegerWidget(
            label='Largura do Portal',
            description="Largura do site em pixels, insira apenas números inteiros. Esta configuração não se aplica a todos os temas.",
        ),
    ),
                                                       
    #-----------BackGround do portal------------------#
    
    StringField(
        name='corPortal',
        searchable=0,
        required=0,
        widget=SmartColorWidget(
            label='Cor do Portal',
            description="Cor para toda área do portal.",
        ),
        schemata = 'Layout'
    ),
    StringField(
        name='corMenuPortal',
        searchable=0,
        required=0,
        widget=SmartColorWidget(
            label='Cor do background do Menu',
            description="Cor do background do Menu de todo portal.",
        ),
        schemata = 'Layout'
    ),
    
    ReferenceField('imageBackground',
        multiValued=0,
        allowed_types=('Image'),
        label=_(u"WallPapper do portal "),
        relationship='imageBackground',
        widget=ReferenceBrowserWidget(
            default_search_index='SearchableText',
            label=_(u"WallPaper do portal"),
            description='A imagem selecionada será exibida como plano de fundo do portal. A imagem será mostrada em seu tamanho original, sem repetição.'),
        schemata = 'Layout'
    ),                                                                   
    
    StringField(
        name='corBackground',
        searchable=0,
        required=0,
        widget=SmartColorWidget(
            label='Cor do background',
            description="Cor para o background do portal, caso a imagem não carregue ou não esteja selecionada.",
        ),
        schemata = 'Layout'
    ),
    
))

finalizeATCTSchema(ThemeConfig_schema, folderish=False)
invisivel = {'view':'invisible','edit':'invisible',}
ThemeConfig_schema['text'].widget.label = 'Texto do Rodapé'
ThemeConfig_schema['text'].widget.description = 'Texto a ser exibido no rodapé do portal.'
ThemeConfig_schema.moveField('text', after='logoRodape')
ThemeConfig_schema['title'].widget.visible = invisivel
ThemeConfig_schema['description'].widget.visible = invisivel


class ThemeConfig(ATDocumentBase):
    """ ThemeConfig """
    
    security = ClassSecurityInfo()
    implements(IThemeConfig)
    portal_type = 'ThemeConfig'
    _at_rename_after_creation = True
    schema = ThemeConfig_schema
    
    def voc_itens_menu(self):
        types = self.portal_types.listContentTypes()
        return types
    
        
    
class ThemeConfigView(grok.View):
    grok.context(IThemeConfig)
    grok.require('zope2.View')
    grok.name('view')
    
    def render(self):
        pass
    
    def update(self):
        url = getSite().portal_url() + '/vindula-control-panel'
        self.context.REQUEST.response.redirect(url)
        
class ThemeConfigCssView(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('personal-layout.css')
     
    def getConfLayout(self):
        obj = getSite()['control-panel-objects']['vindula_themeconfig']
        D = {}
        D['cor'] = obj.corPortal
        try:
            D['url'] = obj.getImageBackground().absolute_url()
        except:
            D['url'] = '/++resource++vindula.themedefault/images/bkgs/bk_body.jpg'
        D['corMenu'] = obj.corMenuPortal
        D['colorBG'] = obj.corBackground
        
        return D      
          
    def getConfiguration(self):
        ctx = self.context.restrictedTraverse('OrgStruct_view')()
        D = {}
        if ctx.portal_type != 'Plone Site':
            if ctx.activ_personalit:
                D['id'] = ctx.id 
                D['cor'] = ctx.corPortal
                D['corMenu'] = ctx.corMenuOrganizacional
                if ctx.getImageBackground():
                    D['url'] = ctx.getImageBackground().absolute_url()
                else:
                    D['url']  = '/++resource++vindula.controlpanel/logo_topo.png'
                D['colorBG'] = ctx.corBackground
        else:
            D = self.getConfLayout()
            
        return D
    
    def render(self):
        config = self.getConfiguration()
        plone = getSite().id
        id = config.get('id',plone)
        color = config.get('cor','#F58220') or '#F58220'
        url = config.get('url','')
        corMenu = config.get('corMenu','')
        colorBG = config.get('colorBG','')
        
        css =  '/* vindula_theme.css */\n'
        css += '    .%s .titulo_info_boxTipo2 h4 a{color: %s !important;}\n' %(id,color) 
        css += '    .%s .gallery-cycle-controls #cycle-prev, .%s .gallery-cycle-controls #cycle-next {background-color:%s !important;}\n' %(id,id,color)
        css += '    .%s .portletWrapper .portletHeader {background-color: %s !important;}' %(id,color)
        css += '    .%s .portletWrapper .portletHeader-dainamic .topPortlet {background-color: %s !important;}' %(id,color)
        css += '    .%s .portletWrapper .portletHeader-dainamic .meioPortlet {background-color: %s !important;}' %(id,color)
        css += '    .%s .portletWrapper .portletHeader-dainamic .bottonPortlet {background-color: %s !important;}' %(id,color)
        css += '/* cont_pagina.css */\n'
        css += '    .%s .cont_superior{ border-bottom-color: %s !important;}\n'%(id,color) 
        css += '    .%s .titulo h2 {color: %s !important;}\n' %(id,color) 
        css += '    .%s .descricao_destaque h4{ color: %s !important;}\n' %(id,color) 
        css += '    .%s .titulo_info_boxTipo2 h4{color: %s !important;}\n' %(id,color) 
        css += '    .%s .info_topoBoxTipo h4{color: %s !important;}\n' %(id,color) 
        css += '    .%s .descricao_titulo h4{color: %s !important;}\n' %(id,color) 
        css += '    .%s .opcoes_noticia h4{color: %s !important;}\n' %(id,color) 
        css += '    .%s .titulo_area h2{color: %s !important;}\n' %(id,color) 
        css += '    .%s .titulo_area{border-bottom-color: %s !important;}\n' %(id,color) 
        css += '    .%s .geral_lista_comentarios .comment {border-top-color: %s !important;}\n' %(id,color) 
        css += '    .%s .item_lista h4{color: %s !important;}\n' %(id,color) 
        css += '    .%s .bt_comentar input{background-color: %s !important;}\n' %(id,color) 
        css += '/* geral.css */\n'
        css += '    .%s {background: url("%s") no-repeat scroll 50%% 0 %s;}\n' %(id,url,colorBG)
        css += '    .%s div#content a:hover, .%s .geral_busca #LSResult .livesearchContainer div.LSIEFix a:hover {color: %s !important;}\n' %(id,id,color)
        css += '    .%s div#content a:hover, .%s dl.portlet a:hover, .%s .geral_busca #LSResult .livesearchContainer div.LSIEFix a:hover {color: %s !important;}' %(id,id,id,color)
        css += '    .%s #geral_breadcrumb span{color:%s;!important;}\n' %(id,color)
        css += '    .%s #barra_superior #cont_barra_superior li a:hover {color: %s !important;}\n' %(id,color) 
        css += '    .%s .cont_superior .documentFirstHeading{color: %s !important;}\n' %(id,color)
        css += '    .%s #like .link{color:%s !important;}\n' %(id,color) 
        css += '/* topo_nav.css */\n'
        css += '    .%s #nav li a:hover {color:%s !important;}\n' %(id,color)
        css += '    .%s .geral_busca .searchButton {background-color: %s !important;}\n' %(id,color)
        css += '    .%s #portal-globalnav-drop .selected a,#portal-globalnav-drop li:hover a {background-color: #000000;color:%s !important;}\n' %(id,color)
        css += '    .%s #portal-globalnav-drop.nivel1 li.selected a:hover {color:%s !important;}\n' %(id,color)
        css += '    .%s #portal-globalnav-drop .selected a, #portal-globalnav-drop li:hover a {background:%s ;color: %s; !important}\n' %(id,corMenu,color)
        css += '    .%s #nav .nivel1 li.selected {background: none repeat scroll 0 0 %s !important;}\n' %(id,corMenu)
        css += '    .%s #nav .nivel2 li.selected {background-color: %s !important;}\n' %(id,corMenu)
        css += '    .%s #nav .nivel2 li, #nav .nivel2 li.selected {border: 4px solid %s !important;}\n' %(id,corMenu)
        css += '    .%s #nav .nivel2 {background: none repeat scroll 0 0 %s;}\n' %(id,corMenu)
        css += '    .%s #nav .nivel2 li, #nav .nivel2 li.selected  {border: 4px solid %s;}\n' %(id,corMenu)
        css += '    .%s #nav .nivel2 li, #nav .nivel2 li  {border: 4px solid %s;}\n' %(id,corMenu)
        css += '    .%s #portal-globalnav-drop li:hover ul li:hover a.hide {background-color: %s; color:#000000 !important;}\n' %(id,color)
        css += '    .%s #portal-globalnav-drop li:hover ul li.selected a.hide {color:%s !important;}\n' %(id,color)
        
        self.response.setHeader('Content-Type', 'text/css; charset=UTF-8')
        return css

registerType(ThemeConfig, PROJECTNAME)
