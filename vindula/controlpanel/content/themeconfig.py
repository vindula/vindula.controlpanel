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

from vindula.controlpanel.browser.at.widget import VindulaReferenceSelectionWidget

# Interface and schema
ThemeConfig_schema =  ATDocumentSchema.copy() + Schema((

#    BooleanField(
#        name='ativa_menudropdown',
#        default=False,
#        widget=BooleanWidget(
#            label="Ativar Menu Dropdown",
#            description='Caso selecionado, ativa o Menu DropDown do Portal.',
#        ),
#        schemata = 'Menu'         
#    ),

    BooleanField(
        name='ativa_buscaAnonima',
        default=True,
        widget=BooleanWidget(
            label="Ativar busca para usuários anônimos",
            description='Caso selecionado, ativa a caixa de busca de conteúdo para usuários anônimos.',
        ),
    ),
    
    TextField(
        name='HTML_header',
        default_content_type = 'text/plain',
        default_output_type = 'text/html',
        
        widget=TextAreaWidget(
            label=_(u"HTML superior ao cabeçalho"),
            description=_(u"Insira um código HTML que vai aparacer acima do cabeçalho do Vindula."),
            
            label_msgid='vindula_controlpanel_label_HTML_header',
            description_msgid='vindula_controlpanel_help_HTML_header',
            i18n_domain='vindula_controlpanel',
        ),
        required=False,
        schemata = 'Extras'
    ),

    StringField(
        name='tipo_buscaPortal',
        widget=SelectionWidget(
            label=_(u"Selecione o tipo de busca para o portal"),
            description=_(u"Selecione o layout da busca."),
            label_msgid='vindula_tile_label_tipo_buscaPortal',
            description_msgid='vindula_tile_help_tipo_buscaPortal',
            i18n_domain='vindula_tile',
            format='select',
        ),
        vocabulary=[("search_01",_(u"Busca de 4 áreas")),
                    ("search_02", _(u"Busca de 2 áreas")),
                   ],
        default='search_01',
        required=True,
    ),
    
#    BooleanField(
#        name='ativa_menudropdown_nivel2',
#        default=False,
#        widget=BooleanWidget(
#            label="Ativar segundo nível do Menu Dropdown",
#            description='Caso selecionado, ativa o segundo nível do Menu DropDown do Portal.',
#        ),
#        schemata = 'Menu'        
#    ),

    ReferenceField('logoCabecalho',
        multiValued=0,
        allowed_types=('Image'),
        label=_(u"Logo do cabeçalho"),
        relationship='logoPortal',
        widget=VindulaReferenceSelectionWidget(
            #default_search_index='SearchableText',
            label=_(u"Logo do cabeçalho"),
            description='A imagem selecionada será exibida no topo do portal.'
        ),
    ),
    
    BooleanField(
        name='ativa_busca_footer',
        default=True,
        widget=BooleanWidget(
            label="Ativar caixa de busca no rodapé",
            description='Ativa a caixa de busca no rodapé do portal.',
        ),
    ),
                                                                   
#    ReferenceField('logoRodape',
#        multiValued=0,
#        allowed_types=('Image'),
#        label=_(u"Logo Rodapé "),
#        relationship='logoRodape',
#        widget=VindulaReferenceSelectionWidget(
#            #default_search_index='SearchableText',
#            label=_(u"Logo Rodapé"),
#            description='A imagem selecionada será exibida no rodapé do portal.'
#        ),
#    ),
#    
#    ReferenceField('imagesCycleLogo',
#        multiValued=1,
#        required=False,
#        allowed_types=('Image'),
#        relationship='imagesCycleLogo',
#        widget=VindulaReferenceSelectionWidget(
#            default_search_index='SearchableText',
#            label=_(u"Imagens rotativas cabeçalho"),
#            description=_(u"Selecione as imagens que ficarão rotacionando no cabeçalho do portal."),
#        ),
#    ),
#    
#    ReferenceField('socialNetworks',
#        multiValued=1,
#        required=0,
#        allowed_types=('SocialNetwork'),
#        relationship='socialNetworks',
#        widget=VindulaReferenceSelectionWidget(
#            default_search_index='SearchableText',
#            label=_(u"Redes sociais"),
#            description=_(u"Selecione as redes sociais que aparecerão no rodapé."),
#        ),
#    ),
    
    ReferenceField('favicon',
        multiValued=0,
        allowed_types=('Image'),
        label=_(u"Favicon"),
        relationship='favicon',
        widget=VindulaReferenceSelectionWidget(
            #default_search_index='SearchableText',
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
    
#    IntegerField(
#        name='larguraPortal',
#        required=0,
#        widget=IntegerWidget(
#            label='Largura do Portal',
#            description="Largura do site em pixels, insira apenas números inteiros. Esta configuração não se aplica a todos os temas.",
#        ),
#    ),
#                               
    # -- Layout do portal ---#
                                                        
#    StringField(
#        name = 'corGeralPortal',
#        searchable=0,
#        required=0,
#        widget=SmartColorWidget(
#            label='Cor dos Links do Portal',
#            description="Cor para grande parte do portal.",
#        ),
#        schemata = 'Layout'
#    ),                                                        
     
    ReferenceField('imageBackground',
        multiValued=0,
        allowed_types=('Image'),
        label=_(u"WallPapper do portal "),
        relationship='imageBackground',
        widget=VindulaReferenceSelectionWidget(
            #default_search_index='SearchableText',
            label=_(u"WallPaper do portal"),
            description='A imagem selecionada será exibida como plano de fundo do portal.'),
        schemata = 'Layout'
    ),
    
    StringField(
        name = 'posicaoImageBackground',
        widget=SelectionWidget(
            label='Posição da imagem de fundo',
            description="Selecione o comportamento da imagem de fundo.",
            format = 'select',
        ),
        vocabulary = [('no-repeat', 'Centralizar'), ('repeat', 'Repetir na página toda'), ('repeat-x', 'Repetir horizontalmente'), ('repeat-y', 'Repetir verticamente'),],
        default='no-repeat',
        schemata = 'Layout'
    ),
    
    BooleanField(
        name='desativaBackground',
        default=False,
        widget=BooleanWidget(
            label="Desativa o background do portal",
            description='Caso selecionado, irá desativar o background do portal prevalencendo assim somente a cor do fundo definida.',
        ),
        schemata = 'Layout'
    ),                                                                 
    
#    StringField(
#        name='corBackground',
#        searchable=0,
#        required=0,
#        widget=SmartColorWidget(
#            label='Cor do background',
#            description="Cor para o background do portal, caso a imagem não carregue ou não esteja selecionada.",
#        ),
#        schemata = 'Layout'
#    ),
    
#    ReferenceField('imageFooter',
#        multiValued=0,
#        allowed_types=('Image'),
#        label=_(u"Imagem para o rodapé do portal."),
#        relationship='imageFooter',
#        widget=VindulaReferenceSelectionWidget(
#            #default_search_index='SearchableText',
#            label=_(u"Imagem para o rodapé do portal"),
#            description='A imagem selecionada será exibida no rodapé do portal. Selecione uma imagem com dimensões 980x121'),
#        schemata = 'Layout'
#    ),
                                                            
                                                       
    #-----------Menu do portal------------------#
    
#    StringField(
#        name='corMenuFundo',
#        searchable=0,
#        required=0,
#        widget=SmartColorWidget(
#            label='Cor de fundo do menu',
#            description="Clique <a class='visualizacao' href='/++resource++vindula.controlpanel/menu/corMenuFundo.png'>aqui para exemplo</a>",
#        ),
#        schemata = 'Menu'
#    ),
#                                                            
#    StringField(
#        name='corMenuFonte',
#        searchable=0,
#        required=0,
#        widget=SmartColorWidget(
#            label='Cor da fonte do menu',
#            description="Clique <a class='visualizacao' href='/++resource++vindula.controlpanel/menu/corMenuFonte.png'>aqui para exemplo</a>",
#        ),
#        schemata = 'Menu'
#    ),
#            
#    StringField(
#        name='corMenuHoverDropdown',
#        searchable=0,
#        required=0,
#        widget=SmartColorWidget(
#            label='Cor do background do menu dropdown',
#            description="Clique <a class='visualizacao' href='/++resource++vindula.controlpanel/menu/corMenuHoverDropdown.png'>aqui para exemplo</a>",
#        ),
#        schemata = 'Menu'
#    ),   
#                                                        
#    ReferenceField('imageSubmenuBkg',
#        multiValued=0,
#        allowed_types=('Image'),
#        label=_(u"Imagem para o background do menu dropdown"),
#        relationship='imageBkgSubmenu',
#        widget=VindulaReferenceSelectionWidget(
#            label=_(u"Imagem para background do menu Dropdown"),
#            description='A imagem selecionada será exibida como plano de fundo do menu dropdown.\
#                         A imagem será mostrada com a sua largura original, com repetição.'),
#        schemata = 'Menu'
#    ),
#    
#    ReferenceField('imageMenuBkg',
#        multiValued=0,
#        allowed_types=('Image'),
#        label=_(u"Imagem para o background do primeiro nivel do menu"),
#        relationship='imageBkgMenu',
#        widget=VindulaReferenceSelectionWidget(
#            label=_(u"Imagem para background do primeiro nivel do menu"),
#            description='A imagem selecionada será exibida como plano de fundo do menu.\
#                         A imagem será mostrada com a sua altura original, com repetição.'),
#        schemata = 'Menu'
#    ),
#    
#    StringField(
#        name='corMenuFonteDropdown',
#        searchable=0,
#        required=0,
#        widget=SmartColorWidget(
#            label='Cor da fonte do menu dropdown',
#            description="Clique <a class='visualizacao' href='/++resource++vindula.controlpanel/menu/corMenuFonteDropdown.png'>aqui para exemplo</a>",
#        ),
#        schemata = 'Menu'
#    ), 
#    
#    StringField(
#        name='corMenuFonteHoverDropdown',
#        searchable=0,
#        required=0,
#        widget=SmartColorWidget(
#            label='Cor da fonte do menu, quando ativo no menu dropdown',
#            description="Clique <a class='visualizacao' href='/++resource++vindula.controlpanel/menu/corMenuFonteHoverDropdown.png'>aqui para exemplo</a>",
#        ),
#        schemata = 'Menu'
#    ),
#    
#    StringField(
#        name='corMenuDropdownHover',
#        searchable=0,
#        required=0,
#        widget=SmartColorWidget(
#            label='Cor do background do link ativo dentro do menu dropdown',
#            description="Clique <a class='visualizacao' href='/++resource++vindula.controlpanel/menu/corMenuDropdownHover.png'>aqui para exemplo</a>",
#        ),
#        schemata = 'Menu'
#    ),     
#    
#    StringField(
#        name='corMenuSelected',
#        searchable=0,
#        required=0,
#        widget=SmartColorWidget(
#            label='Cor do background do link selecionado no primeiro nível do menu',
#            description="Clique <a class='visualizacao' href='/++resource++vindula.controlpanel/menu/corMenuSelected.png'>aqui para exemplo</a>",
#        ),
#        schemata = 'Menu'
#    ),   
#    
#    StringField(
#        name='corMenuFonteSelected',
#        searchable=0,
#        required=0,
#        widget=SmartColorWidget(
#            label='Cor da fonte do link selecionado no primeiro nível do portal',
#            description="Clique <a class='visualizacao' href='/++resource++vindula.controlpanel/menu/corMenuFonteSelected.png'>aqui para exemplo</a>",
#        ),
#        schemata = 'Menu'
#    ),   
#
#    StringField(
#        name='corMenuSelectedDropdown',
#        searchable=0,
#        required=0,
#        widget=SmartColorWidget(
#            label='Cor do background do link selecionado no menu dropdown',
#            description="Clique <a class='visualizacao' href='/++resource++vindula.controlpanel/menu/corMenuSelectedDropdown.png'>aqui para exemplo</a>",
#        ),
#        schemata = 'Menu'
#    ),                                                  
#
#    StringField(
#        name='corMenuFonteSelectedDropdown',
#        searchable=0,
#        required=0,
#        widget=SmartColorWidget(
#            label='Cor da fonte do link selecionado no menu ',
#            description="Clique <a class='visualizacao' href='/++resource++vindula.controlpanel/menu/corMenuFonteSelectedDropdown.png'>aqui para exemplo</a>",
#        ),
#        schemata = 'Menu'
#    ),
    
    # CONFIGURACAO DO TEMA DO PORTLET
    
#    ReferenceField('imageTopPortlet',
#        multiValued=0,
#        allowed_types=('Image'),
#        relationship='imageTopPortlet',
#        widget=VindulaReferenceSelectionWidget(
#            label=_(u"Imagem para aparecer no topo do portlet"),
#            description='A imagem selecionada será exibida como plano de fundo do portlet.\
#                         A imagem será mostrada com a sua altura original, com repetição.'),
#        schemata = 'Portlet'
#
#    ),
#    
#    IntegerField(
#        name='heightTopPortlet',
#        widget=IntegerWidget(
#            label='Altura do topo do portlet',
#            description='Altura, em pixels, do topo do portlet. Quando não definida manterá o padrão de 15px',
#        ),
#        schemata = 'Portlet'
#    ),
#    
#    ReferenceField('imageMiddlePortlet',
#        multiValued=0,
#        allowed_types=('Image'),
#        relationship='imageMiddlePortlet',
#        widget=VindulaReferenceSelectionWidget(
#            label=_(u"Imagem para aparecer no meio do portlet"),
#            description='A imagem selecionada será exibida como plano de fundo do portlet.\
#                         A imagem será mostrada com a sua altura original, com repetição.'),
#        schemata = 'Portlet'
#    ),
#
#    ReferenceField('imageBottomPortlet',
#        multiValued=0,
#        allowed_types=('Image'),
#        relationship='imageBottomPortlet',
#        widget=VindulaReferenceSelectionWidget(
#            label=_(u"Imagem para aparecer em baixo do portlet"),
#            description='A imagem selecionada será exibida como plano de fundo do portlet.\
#                         A imagem será mostrada com a sua altura original, com repetição.'),
#        schemata = 'Portlet'
#    ),
#    
#    IntegerField(
#        name='heightBottomPortlet',
#        widget=IntegerWidget(
#            label='Altura do rodapé do portlet',
#            description='Altura, em pixels, do topo do portlet. Quando não definida manterá o padrão de 23px',
#        ),
#        schemata = 'Portlet'
#    ),
))
finalizeATCTSchema(ThemeConfig_schema, folderish=False)
invisivel = {'view':'invisible','edit':'invisible',}
ThemeConfig_schema['text'].widget.label = 'Texto do Rodapé'
ThemeConfig_schema['text'].widget.description = 'Texto a ser exibido no rodapé do portal.'
ThemeConfig_schema.moveField('text', after='logoCabecalho')
ThemeConfig_schema.moveField('ativa_busca_footer', after='text')
ThemeConfig_schema['title'].widget.visible = invisivel

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
        config_padrao = getSite()['control-panel-objects']['ThemeConfig']
        
        D = {}

        if config_padrao.getLogoCabecalho():
            D['logo_portal'] = config_padrao.getLogoCabecalho().absolute_url()
        else:
            D['logo_portal'] = config_padrao.portal_url() + '/++resource++vindula.controlpanel/imagens/logo_topo.png'
        
        
        #-- Background Portal --#
        D['urlBG'] = ''
        if not config_padrao.getDesativaBackground():
            if config_padrao.getImageBackground():
                D['urlBG'] = obj.getImageBackground().absolute_url()
            else:
                D['urlBG'] = '/++resource++vindula.themedefault/images/bkgs/bk_body.jpg'

        D['posicaoBG'] = obj.getPosicaoImageBackground() or config_padrao.getPosicaoImageBackground() or 'no-repeat'
        
        #Ocultando a busca do footer
        D['displaySearchFooter'] = 'none'
        if config_padrao.getAtiva_busca_footer():
            D['displaySearchFooter'] = 'block'
            
            
        return D
     
    def getConfLayout(self):
        obj = getSite()['control-panel-objects']['ThemeConfig']
        return self.getConfig(obj)       
          
    def getConfiguration(self):
#        ctx = self.context.restrictedTraverse('OrgStruct_view')()
#        ctx = self.context
#        if ctx.portal_type != 'Plone Site':
#            if ctx.activ_personalit:
#                return self.getConfig(ctx), ctx.id 
        
        return self.getConfLayout(), ''

    
    def render(self):
        config, id = self.getConfiguration()
        
        plone = getSite().id
        params = {}
        params['id'] = id or plone
        
        #CONFIGURACAO DO PORTAL
        params['urlBG']     = config.get('urlBG')
        params['posicaoBG'] = config.get('posicaoBG')
        params['displaySearchFooter'] = config.get('displaySearchFooter')
        
        css = """
            .%(id)s { background-image: url("%(urlBG)s"); } \n
            .%(id)s { background-repeat: %(posicaoBG)s; }\n
            .%(id)s { background-position: 50%% 0; }\n
            
            .%(id)s #footer #portal-searchbox { display: %(displaySearchFooter)s; }\n
        """ % params
 
        
        self.response.setHeader('Content-Type', 'text/css; charset=UTF-8')
        return css

