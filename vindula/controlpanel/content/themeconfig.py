# -*- coding: utf-8 -*-

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
            description='Será exibido no topo do portal.'),
    ),
                                                                   
    ReferenceField('logoRodape',
        multiValued=0,
        allowed_types=('Image'),
        label=_(u"Logo Rodape "),
        relationship='logoRodape',
        widget=ReferenceBrowserWidget(
            default_search_index='SearchableText',
            label=_(u"Logo Rodape"),
            description='Será exibido no rodape a imagem selecionada.'),
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
    
    ReferenceField('imageBackground',
        multiValued=0,
        allowed_types=('Image'),
        label=_(u"WallPapper do portal "),
        relationship='imageBackground',
        widget=ReferenceBrowserWidget(
            default_search_index='SearchableText',
            label=_(u"WallPaper do portal"),
            description='Será exibido no backgroup do portal a imagem selecionada. A imagem será mostrada em seu tamanho original, sem repetição.'),
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
ThemeConfig_schema['description'].widget.visible = invisivel
ThemeConfig_schema['title'].widget.visible = invisivel


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

