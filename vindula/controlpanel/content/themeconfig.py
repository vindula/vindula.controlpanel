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
    
    BooleanField(
        name='ativa_buscaAnonima',
        default=True,
        widget=BooleanWidget(
            label="Ativar busca para usuários anônimos",
            description='Se selecionado, Ativa a caixa de busca de conteudo para usuários anônimos.',
        ),
        
    ),

    BooleanField(
        name='ativa_menudropdown_nivel2',
        default=False,
        widget=BooleanWidget(
            label="Ativar segundo nível do Menu Dropdown",
            description='Se selecionado, ativa o segundo nível do Menu DropDown do Portal.',
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
                               
    # -- Layout do portal ---#
                                                        
    StringField(
        name = 'corGeralPortal',
        searchable=0,
        required=0,
        widget=SmartColorWidget(
            label='Cor dos Links do Portal',
            description="Cor para grande parte do portal.",
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
                                                            
                                                       
    #-----------Menu do portal------------------#
    
    StringField(
        name='corMenuFundo',
        searchable=0,
        required=0,
        widget=SmartColorWidget(
            label='Cor de fundo do menu',
            description="Clique <a class='visualizacao' href='/++resource++vindula.controlpanel/menu/corMenuFundo.png'>aqui para exemplo</a>",
            #description="Cor para o fundo do primeiro nível do menu do portal.",
        ),
        schemata = 'Menu'
    ),
                                                            
    StringField(
        name='corMenuFonte',
        searchable=0,
        required=0,
        widget=SmartColorWidget(
            label='Cor da fonte do menu',
            description="Clique <a class='visualizacao' href='/++resource++vindula.controlpanel/menu/corMenuFonte.png'>aqui para exemplo</a>",
            #description="Cor para a fonte do primeiro nível do menu do portal.",
        ),
        schemata = 'Menu'
    ),
            
    StringField(
        name='corMenuHoverDropdown',
        searchable=0,
        required=0,
        widget=SmartColorWidget(
            label='Cor do background do menu dropdown',
            description="Clique <a class='visualizacao' href='/++resource++vindula.controlpanel/menu/corMenuHoverDropdown.png'>aqui para exemplo</a>",
            #description="Cor do background do link quando estiver com o mouse selecionado no primeiro nível, e a cor do fundo do Menu Dropdown.",
        ),
        schemata = 'Menu'
    ),   
                                                        
    ReferenceField('imageMenuBkg',
        multiValued=0,
        allowed_types=('Image'),
        label=_(u"Imagem para o background do menu dropdown"),
        relationship='imageBkgMenu',
        widget=ReferenceBrowserWidget(
            default_search_index='SearchableText',
            label=_(u"Imagem para background do menu Dropdown"),
            description='A imagem selecionada será exibida como plano de fundo do menu.\
                         A imagem será mostrada em seu tamanho original, com repetição.'),
        schemata = 'Menu'
    ),
    
    StringField(
        name='corMenuFonteDropdown',
        searchable=0,
        required=0,
        widget=SmartColorWidget(
            label='Cor da fonte do menu dropdown',
            description="Clique <a class='visualizacao' href='/++resource++vindula.controlpanel/menu/corMenuFonteDropdown.png'>aqui para exemplo</a>",
            #description="Cor da fonte do link quando estiver selecionado pelo mouse no Menu Dropdown.",
        ),
        schemata = 'Menu'
    ), 
    
    StringField(
        name='corMenuFonteHoverDropdown',
        searchable=0,
        required=0,
        widget=SmartColorWidget(
            label='Cor da fonte do menu, quando ativo no menu dropdown',
            description="Clique <a class='visualizacao' href='/++resource++vindula.controlpanel/menu/corMenuFonteHoverDropdown.png'>aqui para exemplo</a>",
#            description="Cor para a fonte do primeiro nível do menu do portal quando ele\
#                         estiver quando selecionado pelo mouse e ao cor dos links dentro do Menu Dropdown.",
        ),
        schemata = 'Menu'
    ),
    
    StringField(
        name='corMenuDropdownHover',
        searchable=0,
        required=0,
        widget=SmartColorWidget(
            label='Cor do background do link ativo dentro do menu dropdown',
            description="Clique <a class='visualizacao' href='/++resource++vindula.controlpanel/menu/corMenuDropdownHover.png'>aqui para exemplo</a>",
            #description="Cor do link quando estiver selecionado pelo mouse dentro do Menu Dropdown.",
        ),
        schemata = 'Menu'
    ),     
    
    StringField(
        name='corMenuSelected',
        searchable=0,
        required=0,
        widget=SmartColorWidget(
            label='Cor do background do link selecionado no primeiro nível do menu',
            description="Clique <a class='visualizacao' href='/++resource++vindula.controlpanel/menu/corMenuSelected.png'>aqui para exemplo</a>",
            #description="Cor do fundo do link quando estiver selecionado no primeiro nível do Menu.",
        ),
        schemata = 'Menu'
    ),   
    
    StringField(
        name='corMenuFonteSelected',
        searchable=0,
        required=0,
        widget=SmartColorWidget(
            label='Cor da fonte do link selecionado no primeiro nível do portal',
            description="Clique <a class='visualizacao' href='/++resource++vindula.controlpanel/menu/corMenuFonteSelected.png'>aqui para exemplo</a>",
            #description="Cor da fonte link quando estiver selecionado no primeiro nível.",
        ),
        schemata = 'Menu'
    ),   

    StringField(
        name='corMenuSelectedDropdown',
        searchable=0,
        required=0,
        widget=SmartColorWidget(
            label='Cor do background do link selecionado no menu dropdown',
            description="Clique <a class='visualizacao' href='/++resource++vindula.controlpanel/menu/corMenuSelectedDropdown.png'>aqui para exemplo</a>",
            #description="Cor do background do link quando estiver selecionado no Menu Dropdown.",
        ),
        schemata = 'Menu'
    ),                                                  

    StringField(
        name='corMenuFonteSelectedDropdown',
        searchable=0,
        required=0,
        widget=SmartColorWidget(
            label='Cor da fonte do link selecionado no menu ',
            description="Clique <a class='visualizacao' href='/++resource++vindula.controlpanel/menu/corMenuFonteSelectedDropdown.png'>aqui para exemplo</a>",
            #description="Cor da fonte do link quando estiver selecionado no Menu.",
        ),
        schemata = 'Menu'
    ),


))
finalizeATCTSchema(ThemeConfig_schema, folderish=False)
invisivel = {'view':'invisible','edit':'invisible',}
ThemeConfig_schema['text'].widget.label = 'Texto do Rodapé'
ThemeConfig_schema['text'].widget.description = 'Texto a ser exibido no rodapé do portal.'
ThemeConfig_schema.moveField('text', after='logoRodape')
ThemeConfig_schema['title'].widget.visible = invisivel
ThemeConfig_schema['description'].widget.visible = invisivel

# Dates
L = ['effectiveDate','expirationDate','creation_date','modification_date']   
# Categorization
L += ['subject','relatedItems','location','language']
# Ownership
L += ['creators','contributors','rights']
# Settings
L += ['allowDiscussion','excludeFromNav', 'presentation','tableContents']

for i in L:
    ThemeConfig_schema[i].widget.visible = invisivel    

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
    
registerType(ThemeConfig, PROJECTNAME)


#----------------------------        
#Views de configuração    
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
     
    def checkTransparent(self, value):
        if value == 'transparent':
            return ''
        else:
            return value
        
    def getConfig(self, obj): 
        D = {}
        D['cor'] = self.checkTransparent(obj.getCorGeralPortal()) or '#F58220'

        #-- Background Portal --#
        D['corBackground'] = self.checkTransparent(obj.getCorBackground()) or '#FFF'
        if obj.getImageBackground():
            D['url'] = obj.getImageBackground().absolute_url()
        
        elif D.get('corBackground') == '#FFF':
            D['url'] = '/++resource++vindula.themedefault/images/bkgs/bk_body.jpg'
        
        else:
            D['url'] = ''
        
        #-- Config Menu --#
        D['corMenuFundo'] = self.checkTransparent(obj.getCorMenuFundo()) or '#FFF'
        D['corMenuFonte'] = self.checkTransparent(obj.getCorMenuFonte()) or '#000'

        D['corMenuHoverDropdown'] = self.checkTransparent(obj.getCorMenuHoverDropdown()) or '#525254'
        if obj.getImageMenuBkg():
            D['urlMenu'] = obj.getImageMenuBkg().absolute_url()
        
        elif D.get('corMenuHoverDropdown') == '#525254':
            D['urlMenu'] = '/++resource++vindula.themedefault/images/bkgs/bg_menu.jpg'
        
        else:
            D['urlMenu'] = ''
        
        D['corMenuFonteDropdown'] = self.checkTransparent(obj.getCorMenuFonteDropdown()) or '#e4e4e4'
        D['corMenuFonteHoverDropdown'] = self.checkTransparent(obj.getCorMenuFonteHoverDropdown()) or '#F58220'
        D['corMenuDropdownHover'] = self.checkTransparent(obj.getCorMenuDropdownHover()) or '#000'
        D['corMenuSelected'] = self.checkTransparent(obj.getCorMenuSelected()) or '#000'
        D['corMenuFonteSelected'] = self.checkTransparent(obj.getCorMenuFonteSelected()) or '#FFF'
        D['corMenuSelectedDropdown'] = self.checkTransparent(obj.getCorMenuSelectedDropdown()) or '#000'
        D['corMenuFonteSelectedDropdown'] = self.checkTransparent(obj.getCorMenuFonteSelectedDropdown()) or '#F58220'
        

        return D
     
    def getConfLayout(self):
        obj = getSite()['control-panel-objects']['vindula_themeconfig']
        return self.getConfig(obj)       
          
    def getConfiguration(self):
        ctx = self.context.restrictedTraverse('OrgStruct_view')()
        if ctx.portal_type != 'Plone Site':
            if ctx.activ_personalit:
                return self.getConfig(ctx), ctx.id 
        
        return self.getConfLayout(), ''

    
    def render(self):
        config, id = self.getConfiguration()
        plone = getSite().id
        id = id or plone
        
        color = config.get('cor','#F58220') or '#F58220'
        colorBG = config.get('colorBG','#FFF') or '#FFF'
        url = config.get('url','/++resource++vindula.themedefault/images/bkgs/bk_body.jpg')
        
        corMenuFundo = config.get('corMenuFundo','#FFF') or '#FFF'
        corMenuFonte = config.get('corMenuFonte','#000') or '#000'
        corMenuHoverDropdown = config.get('corMenuHoverDropdown','#525254') or '#525254'
        urlMenu = config.get('urlMenu', '/++resource++vindula.themedefault/images/bkgs/bg_menu.jpg')
        corMenuFonteDropdown = config.get('corMenuFonteDropdown','#e4e4e4') or '#e4e4e4'
        corMenuFonteHoverDropdown = config.get('corMenuFonteHoverDropdown','#F58220') or '#F58220'
        corMenuDropdownHover = config.get('corMenuDropdownHover','#000') or '#000'
        corMenuSelected = config.get('corMenuSelected','#000') or '#000'
        corMenuFonteSelected = config.get('corMenuFonteSelected','#FFF') or '#FFF'
        corMenuSelectedDropdown = config.get('corMenuSelectedDropdown','#000') or '#000'
        corMenuFonteSelectedDropdown = config.get('corMenuFonteSelectedDropdown','#F58220') or '#F58220'
        
      
        css =  '/* vindula_theme.css */\n'
        css += '    .%s .titulo_info_boxTipo2 h4 a{color: %s !important;}\n' %(id,color) 
        css += '    .%s .gallery-cycle-controls #cycle-prev, .%s .gallery-cycle-controls #cycle-next {background-color:%s !important;}\n' %(id,id,color)
        css += '    .%s .portletWrapper .portletHeader {background-color: %s !important;}' %(id,color)
        css += '    .%s .portletWrapper .portletHeader-dainamic .topPortlet {background-color: %s !important;}' %(id,color)
        css += '    .%s .portletWrapper .portletHeader-dainamic .meioPortlet {background-color: %s !important;}' %(id,color)
        css += '    .%s .portletWrapper .portletHeader-dainamic .bottonPortlet {background-color: %s !important;}' %(id,color)
        css += '    .%s .pag_all {background-color: %s !important;}' %(id,color)
        css += '    .%s .userpage div.department {background-color: %s !important;}' %(id,color)
        css += '    .%s .userpage div.area {border-bottom-color: %s !important;}' %(id,color) 
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
        css += '/* topo_nav.css */\n' #23
        css += '    .%s .geral_busca .searchButton {background-color: %s !important;}\n' %(id,color)
        css += '    .%s #nav .nivel1 {border-bottom-color: %s;background-color:%s;}\n' %(id,corMenuSelected,corMenuFundo)
        css += '    .%s #nav li a {color:%s !important;}\n' %(id,corMenuFonte)
        css += '    .%s #nav li a:hover {color:%s !important;}\n' %(id,corMenuFonteDropdown)
        css += '    .%s #nav .nivel2 li a {color:%s !important;}\n' %(id,corMenuFonteDropdown)       
        css += '    .%s #nav .nivel2 li.selected a {color:%s !important;}\n' %(id,corMenuFonteSelectedDropdown)
        css += '    .%s #nav li:hover {background-color:%s; color:%s !important;}\n' %(id,corMenuHoverDropdown,corMenuFonteDropdown)
        css += '    .%s #portal-globalnav-drop li:hover a { background: url("%s") repeat scroll 0 0 %s !important; color: %s !important;}\n' %(id,urlMenu, corMenuHoverDropdown,corMenuFonteDropdown)
        css += '    .%s #portal-globalnav-drop.nivel1 li.selected a:hover {color:%s !important;}\n' %(id,corMenuFonteSelected)
        css += '    .%s #portal-globalnav-drop .selected a {background: none repeat scroll 0 0 %s !important; color: %s !important;}\n' %(id,corMenuSelected, corMenuFonteSelected)
        css += '    .%s #nav .nivel1 li.selected {background: none repeat scroll 0 0 %s !important;}\n' %(id,corMenuSelected)
        css += '    .%s #nav .nivel1 li.selected a{color: %s !important; }\n' %(id,corMenuFonteSelected)
        css += '    .%s #portal-globalnav-drop .nivel2, .%s #portal-globalnav-drop .nivel3 {background: url("%s") repeat scroll 0 0 %s !important;}' %(id,id,urlMenu,corMenuHoverDropdown)
        css += '    .%s #nav .nivel2 {background: none repeat scroll 0 0 %s;}\n' %(id,corMenuHoverDropdown)
        css += '    .%s #nav .nivel3 {background: none repeat scroll 0 0 %s;}\n' %(id,corMenuHoverDropdown)
        css += '    .%s #nav .nivel2 li.selected a {background-color: %s !important; color: %s !important;}\n' %(id,corMenuSelectedDropdown,corMenuFonteSelectedDropdown)
        css += '    .%s #portal-globalnav-drop li:hover ul li:hover ul li a.hide {background: url("%s") repeat scroll 0 0 %s !important; color: %s !important;}\n' %(id,urlMenu, corMenuHoverDropdown,corMenuFonteDropdown)
        css += '    .%s #portal-globalnav-drop li:hover ul li:hover a.hide {background: %s !important; color:%s !important;}\n' %(id,corMenuDropdownHover,corMenuFonteHoverDropdown)
        css += '    .%s #portal-globalnav-drop li:hover ul li ul li:hover a.hide {background: %s !important; color:%s !important;}\n' %(id,corMenuDropdownHover,corMenuFonteHoverDropdown)
        css += '    .%s #portal-globalnav-drop li:hover ul li:hover ul li.selected a.hide {color:%s !important; background: %s !important; }\n' %(id,corMenuFonteSelectedDropdown,corMenuSelectedDropdown)
        css += '/* chat.css */\n'
#        css += '    .%s .chatboxhead {background-color: %s; border-right-color: %s; border-left-color: %s;}\n' %(id,color,color,color)
#        css += '    .%s .chatboxblink {background-color: %s; border-right-color: %s; border-left-color: %s;}\n' %(id,color,color,color)
#        css += '    .%s .chatboxtextareaselected {border-color: %s;}\n' %(id,color)
        css += '    .%s #jappix_mini div.jm_actions {background-color: %s; border-bottom: %s;}\n' %(id,color,color)
        css += '    .%s #jappix_mini div.jm_actions a.jm_one-action {background-color: %s;}\n' %(id,color)
        css += '    .%s #jappix_mini a.jm_friend:hover, #jappix_mini a.jm_friend:focus {background-color: %s; border-color: %s;}\n' %(id,color,color)
        css += '    .%s #jappix_mini input.jm_send-messages {border-color: %s;}\n' %(id,color)
        css += '    .%s #jappix_mini div.jm_chat-content {border-color: %s;}\n' %(id,color)
        css += '    .%s #jappix_mini div.jm_actions a.jm_one-action:hover, #jappix_mini div.jm_actions a.jm_one-action:focus {background-color: %s;}\n' %(id,color)
 
        
        self.response.setHeader('Content-Type', 'text/css; charset=UTF-8')
        return css


