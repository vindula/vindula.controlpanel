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
import pdb
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
            description='A imagem selecionada será exibida no topo do portal.'
        ),
    ),
                                                                   
    ReferenceField('logoRodape',
        multiValued=0,
        allowed_types=('Image'),
        label=_(u"Logo Rodapé "),
        relationship='logoRodape',
        widget=ReferenceBrowserWidget(
            default_search_index='SearchableText',
            label=_(u"Logo Rodapé"),
            description='A imagem selecionada será exibida no rodapé do portal.'
        ),
    ),
    
    ReferenceField('imagesCycleLogo',
        multiValued=1,
        required=False,
        allowed_types=('Image'),
        relationship='imagesCycleLogo',
        widget=ReferenceBrowserWidget(
            default_search_index='SearchableText',
            label=_(u"Imagens rotativas cabeçalho"),
            description=_(u"Selecione as imagens que ficarão rotacionando no cabeçalho do portal."),
        ),
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
        widget=InAndOutWidget(
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
        name = 'posicaoImageBackground',
        widget=SelectionWidget(
            label='Posição da imagem de fundo',
            description="Selecione o coportamento da imagem de fundo.",
            format = 'select',
        ),
        vocabulary = [('no-repeat', 'Centralizar'), ('repeat', 'Repetir na pagina toda'), ('repeat-x', 'Repetir horizontalmente'), ('repeat-y', 'Repetir verticamente'),],
        default='no-repeat',
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
    
    ReferenceField('imageFooter',
        multiValued=0,
        allowed_types=('Image'),
        label=_(u"Imagem para o rodapé do portal."),
        relationship='imageFooter',
        widget=ReferenceBrowserWidget(
            default_search_index='SearchableText',
            label=_(u"Imagem para o rodapé do portal"),
            description='A imagem selecionada será exibida no rodapé do portal. Selecione uma imagem com dimenções 980x121'),
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
        ),
        schemata = 'Menu'
    ),   
                                                        
    ReferenceField('imageSubmenuBkg',
        multiValued=0,
        allowed_types=('Image'),
        label=_(u"Imagem para o background do menu dropdown"),
        relationship='imageBkgSubmenu',
        widget=ReferenceBrowserWidget(
            label=_(u"Imagem para background do menu Dropdown"),
            description='A imagem selecionada será exibida como plano de fundo do menu dropdown.\
                         A imagem será mostrada com a sua largura original, com repetição.'),
        schemata = 'Menu'
    ),
    
    ReferenceField('imageMenuBkg',
        multiValued=0,
        allowed_types=('Image'),
        label=_(u"Imagem para o background do primeiro nivel do menu"),
        relationship='imageBkgMenu',
        widget=ReferenceBrowserWidget(
            label=_(u"Imagem para background do primeiro nivel do menu"),
            description='A imagem selecionada será exibida como plano de fundo do menu.\
                         A imagem será mostrada com a sua altura original, com repetição.'),
        schemata = 'Menu'
    ),
    
    StringField(
        name='corMenuFonteDropdown',
        searchable=0,
        required=0,
        widget=SmartColorWidget(
            label='Cor da fonte do menu dropdown',
            description="Clique <a class='visualizacao' href='/++resource++vindula.controlpanel/menu/corMenuFonteDropdown.png'>aqui para exemplo</a>",
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
        ),
        schemata = 'Menu'
    ),
    
    # CONFIGURACAO DO TEMA DO PORTLET
    
    ReferenceField('imageTopPortlet',
        multiValued=0,
        allowed_types=('Image'),
        relationship='imageTopPortlet',
        widget=ReferenceBrowserWidget(
            label=_(u"Imagem para aparecer no topo do portlet"),
            description='A imagem selecionada será exibida como plano de fundo do menu.\
                         A imagem será mostrada com a sua altura original, com repetição.'),
        schemata = 'Portlet'

    ),
    
    IntegerField(
        name='heightTopPortlet',
        widget=IntegerWidget(
            label='Altura do topo do portlet',
            description='Altura, em pixels, do topo do portlet. Quando não definida manterá o padrão de 15px',
        ),
        schemata = 'Portlet'
    ),
    
    ReferenceField('imageMiddlePortlet',
        multiValued=0,
        allowed_types=('Image'),
        relationship='imageMiddlePortlet',
        widget=ReferenceBrowserWidget(
            label=_(u"Imagem para aparecer no meio do portlet"),
            description='A imagem selecionada será exibida como plano de fundo do menu.\
                         A imagem será mostrada com a sua altura original, com repetição.'),
        schemata = 'Portlet'
    ),

    ReferenceField('imageBottomPortlet',
        multiValued=0,
        allowed_types=('Image'),
        relationship='imageBottomPortlet',
        widget=ReferenceBrowserWidget(
            label=_(u"Imagem para aparecer em baixo do portlet"),
            description='A imagem selecionada será exibida como plano de fundo do menu.\
                         A imagem será mostrada com a sua altura original, com repetição.'),
        schemata = 'Portlet'
    ),
    
    IntegerField(
        name='heightBottomPortlet',
        widget=IntegerWidget(
            label='Altura do rodapé do portlet',
            description='Altura, em pixels, do topo do portlet. Quando não definida manterá o padrão de 23px',
        ),
        schemata = 'Portlet'
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
        url = self.context.absolute_url()+'/edit'
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
        D['corBG'] = self.checkTransparent(obj.getCorBackground()) or '#FFF'

        if obj.getImageBackground():
            D['urlBG'] = obj.getImageBackground().absolute_url()
        elif D.get('corBG') == '#FFF':
            D['urlBG'] = '/++resource++vindula.themedefault/images/bkgs/bk_body.jpg'
        else:
            D['urlBG'] = ''
        
        if D['urlBG']: D['posicaoBG'] = obj.getPosicaoImageBackground()

        if obj.getImageFooter():
            D['urlFooter'] = obj.getImageFooter().absolute_url()
        else:
            D['urlFooter'] = ''
        
        #-- Config Menu --#
        D['corMenuFundo'] = self.checkTransparent(obj.getCorMenuFundo()) or '#FFF'
        D['corMenuFonte'] = self.checkTransparent(obj.getCorMenuFonte()) or '#000'
        D['corMenuHoverDropdown'] = self.checkTransparent(obj.getCorMenuHoverDropdown()) or '#525254'
            
        D['corMenuFonteDropdown'] = self.checkTransparent(obj.getCorMenuFonteDropdown()) or '#e4e4e4'
        D['corMenuFonteHoverDropdown'] = self.checkTransparent(obj.getCorMenuFonteHoverDropdown()) or '#F58220'
        D['corMenuDropdownHover'] = self.checkTransparent(obj.getCorMenuDropdownHover()) or '#000'
        D['corMenuSelected'] = self.checkTransparent(obj.getCorMenuSelected()) or '#000'
        D['corMenuFonteSelected'] = self.checkTransparent(obj.getCorMenuFonteSelected()) or '#FFF'
        D['corMenuSelectedDropdown'] = self.checkTransparent(obj.getCorMenuSelectedDropdown()) or '#000'
        D['corMenuFonteSelectedDropdown'] = self.checkTransparent(obj.getCorMenuFonteSelectedDropdown()) or '#F58220'
        
        # IMAGENS DE FUNDO DO MENU E SUBMENU #
        if obj.getImageMenuBkg()   : D['urlMenu']    = obj.getImageMenuBkg().absolute_url()
        D['urlSubmenu'] = ''
        if obj.getImageSubmenuBkg():
            D['urlSubmenu'] = obj.getImageSubmenuBkg().absolute_url()
        elif D.get('corMenuHoverDropdown') == '#525254':
            D['urlSubmenu'] = '/++resource++vindula.themedefault/images/bkgs/bg_menu.jpg'
        
        # CONFIGURACAO DO PORTLET #
        if obj.getImageTopPortlet()    : D['urlTopPortlet']       = obj.getImageTopPortlet().absolute_url()
        if obj.getImageMiddlePortlet() : D['urlMiddlePortlet']    = obj.getImageMiddlePortlet().absolute_url()
        if obj.getImageBottomPortlet() : D['urlBottomPortlet']    = obj.getImageBottomPortlet().absolute_url()
        if obj.getHeightTopPortlet()   : D['heightTopPortlet']    = obj.getHeightTopPortlet()
        if obj.getHeightBottomPortlet(): D['heightBottomPortlet'] = obj.getHeightBottomPortlet()
        
        return D
     
    def getConfLayout(self):
        obj = getSite()['control-panel-objects']['ThemeConfig']
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
        params = {}
        params['id'] = id or plone
        
        #CONFIGURACAO DO PORTAL
        params['color']     = config.get('cor','#F58220') or '#F58220'
        params['urlBG']     = config.get('urlBG','/++resource++vindula.themedefault/images/bkgs/bk_body.jpg')
        params['posicaoBG'] = config.get('posicaoBG', 'no-repeat')
        params['colorBG']   = config.get('corBG','#FFF') or '#FFF'
        params['urlFooter'] = config.get('urlFooter') or ''
        
        #CONFIGURACAO DO MENU
        params['urlMenu']                      = config.get('urlMenu'                     , '')
        params['urlSubmenu']                   = config.get('urlSubmenu'                  , '/++resource++vindula.themedefault/images/bkgs/bg_menu.jpg')
        params['corMenuFundo']                 = config.get('corMenuFundo'                ,'#FFF')    or '#FFF'
        params['corMenuFonte']                 = config.get('corMenuFonte'                ,'#000')    or '#000'
        params['corMenuSelected']              = config.get('corMenuSelected'             ,'#000')    or '#000'
        params['corMenuHoverDropdown']         = config.get('corMenuHoverDropdown'        ,'#525254') or '#525254'
        params['corMenuFonteDropdown']         = config.get('corMenuFonteDropdown'        ,'#e4e4e4') or '#e4e4e4'
        params['corMenuDropdownHover']         = config.get('corMenuDropdownHover'        ,'#000')    or '#000'
        params['corMenuFonteSelected']         = config.get('corMenuFonteSelected'        ,'#FFF')    or '#FFF'
        params['corMenuSelectedDropdown']      = config.get('corMenuSelectedDropdown'     ,'#000')    or '#000'
        params['corMenuFonteHoverDropdown']    = config.get('corMenuFonteHoverDropdown'   ,'#F58220') or '#F58220'
        params['corMenuFonteSelectedDropdown'] = config.get('corMenuFonteSelectedDropdown','#F58220') or '#F58220'
        
        #CONFIGURACAO DO PORTLET
        params['urlTopPortlet']       = config.get('urlTopPortlet'   ,    '++resource++vindula.themedefault/images/bkgs/topoBoxTipo2-top.png')
        params['urlMiddlePortlet']    = config.get('urlMiddlePortlet',    '++resource++vindula.themedefault/images/bkgs/topoBoxTipo2-meio.png')
        params['urlBottomPortlet']    = config.get('urlBottomPortlet',    '++resource++vindula.themedefault/images/bkgs/topoBoxTipo2-botton.png')
        params['heightTopPortlet']    = config.get('heightTopPortlet',    15)
        params['heightBottomPortlet'] = config.get('heightBottomPortlet', 23)
        
        # CRIACAO DO CSS DINAMICO #    
        css =  \
        '/* vindula_theme.css */\n' \
               ' .%(id)s .titulo_info_boxTipo2 h4 a{color: %(color)s !important;}\n' \
               ' .%(id)s .circle {background-color:%(color)s !important;}\n' \
               ' .%(id)s dl.portlet .portletHeader .portletTopLeft {background-color: %(color)s !important; background-image: url("%(urlTopPortlet)s") !important; height:%(heightTopPortlet)spx;}\n' \
               ' .%(id)s dl.portlet .portletHeader > span, .%(id)s dl.portlet .portletHeader > a {background-color: %(color)s !important; background-image: url("%(urlMiddlePortlet)s") !important;}\n' \
               ' .%(id)s dl.portlet .portletHeader .portletTopRight {background-color: %(color)s !important; background-image: url("%(urlBottomPortlet)s") !important; height:%(heightBottomPortlet)spx;}\n' \
               ' .%(id)s .pag_all {background-color: %(color)s !important;}\n' \
               ' .%(id)s .userpage div.department {background-color: %(color)s !important;}\n' \
               ' .%(id)s .userpage div.area {border-bottom-color: %(color)s !important;}\n' \
         '/* cont_pagina.css */\n' \
               ' .%(id)s .cont_superior{ border-bottom-color: %(color)s !important;}\n' \
               ' .%(id)s .titulo h2 {color: %(color)s !important;}\n' \
               ' .%(id)s .descricao_destaque h4{ color: %(color)s !important;}\n' \
               ' .%(id)s .titulo_info_boxTipo2 h4{color: %(color)s !important;}\n' \
               ' .%(id)s .info_topoBoxTipo h4{color: %(color)s !important;}\n' \
               ' .%(id)s .descricao_titulo h4{color: %(color)s !important;}\n' \
               ' .%(id)s .opcoes_noticia h4{color: %(color)s !important;}\n' \
               ' .%(id)s .titulo_area h2{color: %(color)s !important;}\n' \
               ' .%(id)s .titulo_area{border-bottom-color: %(color)s !important;}\n' \
               ' .%(id)s .geral_lista_comentarios .comment {border-top-color: %(color)s !important;}\n' \
               ' .%(id)s .item_lista h4{color: %(color)s !important;}\n' \
               ' .%(id)s .bt_comentar input{background-color: %(color)s !important;}\n' \
               ' .%(id)s .bt_comments {background-color: %(color)s !important;}\n' \
         '/* geral.css */\n' \
               ' .%(id)s {background: url("%(urlBG)s") %(posicaoBG)s scroll 50%% 0 %(colorBG)s;}\n' \
               ' .%(id)s div#content a:hover, .%(id)s dl.portlet a:hover, .%(id)s .geral_busca #LSResult .livesearchContainer div.LSIEFix a:hover {color: %(color)s !important;}' \
               ' .%(id)s #geral_breadcrumb span{color:%(color)s;!important;}\n' \
               ' .%(id)s #barra_superior #cont_barra_superior li a:hover {color: %(color)s !important;}\n' \
               ' .%(id)s .cont_superior .documentFirstHeading{color: %(color)s !important;}\n' \
               ' .%(id)s #like .link{color:%(color)s !important;}\n' \
               ' .%(id)s div.listingBar a:hover{color:%(color)s !important;}\n' \
         '/* topo_nav.css */\n' \
               ' .%(id)s .geral_busca .searchButton {background-color: %(color)s !important;}\n' \
               ' .%(id)s #nav .nivel1 {border-bottom-color:%(corMenuSelected)s; background-color:%(corMenuFundo)s; background-image:url("%(urlMenu)s");}\n' \
               ' .%(id)s #nav .nivel2 li a {color: %(corMenuFonteHoverDropdown)s;}\n' \
               ' .%(id)s #nav ul.normal-menu li a {color:%(corMenuFonteSelected)s !important;}\n' \
               ' .%(id)s #portal-globalnav-drop li a {color:%(corMenuFonte)s !important;}\n' \
               ' .%(id)s #nav li a:hover {color:%(corMenuFonteDropdown)s !important;}\n' \
               ' .%(id)s #nav ul.menu-normal li:hover a {color:%(corMenuFonteDropdown)s !important;}\n' \
               ' .%(id)s #nav ul.normal-menu .nivel2 li a {color:%(corMenuFonte)s !important;}\n' \
               ' .%(id)s #nav li:hover {background-color:%(corMenuHoverDropdown)s; color:%(corMenuFonteDropdown)s !important;}\n' \
               ' .%(id)s #portal-globalnav-drop li:hover a { background: url("%(urlSubmenu)s") repeat-y scroll right 0 %(corMenuHoverDropdown)s !important; color: %(corMenuFonteDropdown)s !important;}\n' \
               ' .%(id)s #portal-globalnav-drop li a:hover.cor-hover{ color: %(corMenuFonteHoverDropdown)s !important;}\n' \
               ' .%(id)s #portal-globalnav-drop.nivel1 li.selected a:hover {color:%(corMenuFonteHoverDropdown)s !important;}\n' \
               ' .%(id)s #portal-globalnav-drop .selected a {background: none repeat scroll 0 0 %(corMenuSelected)s !important; color: %(corMenuFonteSelected)s !important;}\n' \
               ' .%(id)s #nav .nivel1 li.selected {background: none repeat scroll 0 0 %(corMenuSelected)s !important;}\n' \
               ' .%(id)s #nav ul.menu-normal li.selected a{color: %(corMenuFonteSelected)s !important; }\n' \
               ' .%(id)s #portal-globalnav-drop .nivel2, .%(id)s #portal-globalnav-drop .nivel3 {background: url("%(urlSubmenu)s") repeat scroll 0 0 %(corMenuHoverDropdown)s !important;}' \
               ' .%(id)s #nav .nivel2 {background: none repeat scroll 0 0 %(corMenuHoverDropdown)s;}\n' \
               ' .%(id)s #nav .nivel3 {background: none repeat scroll 0 0 %(corMenuHoverDropdown)s;}\n' \
               ' .%(id)s #nav .nivel2 li.selected a {background-color: %(corMenuSelectedDropdown)s !important; color: %(corMenuFonteSelectedDropdown)s !important;}\n' \
               ' .%(id)s #portal-globalnav-drop li:hover ul li:hover ul li a.hide {background: url("%(urlSubmenu)s") repeat-y scroll right 0 %(corMenuHoverDropdown)s !important; color: %(corMenuFonteDropdown)s !important;}\n' \
               ' .%(id)s #portal-globalnav-drop li:hover ul li:hover a.hide {background: %(corMenuDropdownHover)s !important; color:%(corMenuFonteHoverDropdown)s !important;}\n' \
               ' .%(id)s #portal-globalnav-drop li:hover ul li ul li:hover a.hide {background: %(corMenuDropdownHover)s !important; color:%(corMenuFonteHoverDropdown)s !important;}\n' \
               ' .%(id)s #portal-globalnav-drop li:hover ul li:hover ul li.selected a.hide {color:%(corMenuFonteSelectedDropdown)s !important; background: %(corMenuSelectedDropdown)s !important; }\n' \
         '/* chat.css */\n' \
               ' .%(id)s #jappix_mini div.jm_actions {background-color: %(color)s; border-bottom: %(color)s;}\n' \
               ' .%(id)s #jappix_mini div.jm_actions a.jm_one-action {background-color: %(color)s;}\n' \
               ' .%(id)s #jappix_mini a.jm_friend:hover, #jappix_mini a.jm_friend:focus {background-color: %(color)s; border-color: %(color)s;}\n' \
               ' .%(id)s #jappix_mini input.jm_send-messages {border-color: %(color)s;}\n' \
               ' .%(id)s #jappix_mini div.jm_chat-content {border-color: %(color)s;}\n' \
               ' .%(id)s #jappix_mini div.jm_actions a.jm_one-action:hover, #jappix_mini div.jm_actions a.jm_one-action:focus {background-color: %(color)s;}\n' \
         '/* portlet_controlpanel.css */\n' \
               ' .%(id)s #portlet-prefs .selectedHead {background-color: %(color)s;}\n' % params
        
        if params.get('urlFooter'):
             css += '/* rodape.css */\n' \
                    ' .%(id)s #rodape {background: url("%(urlFooter)s") no-repeat scroll 10px;}\n' % params
 
        
        self.response.setHeader('Content-Type', 'text/css; charset=UTF-8')
        return css