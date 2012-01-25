# -*- coding: utf-8 -*-
from zope import schema
from zope.interface import Interface
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.app.textfield import RichText
from z3c.relationfield.schema import RelationChoice
from vindula.controlpanel import MessageFactory as _
from vindula.controlpanel.vocabularies import ListPortalType

    
# Interface and schema

class IThemeConfig(Interface):
    """ Theme Settings interface """

    logo_top = RelationChoice(
        title=_(u"Logo do Cabeçalho"),
        description=_(u"Logo que será exibido no cabeçalho do portal."),
        source=ObjPathSourceBinder(
            portal_type = 'Image',
            ),
        required=False,
        ) 
    
    
    logo_footer = RelationChoice(
        title=_(u"Logo do Rodapé"),
        description=_(u"Logo que será exibido no rodapé do portal."),
        source=ObjPathSourceBinder(
            portal_type = 'Image',
            ),
        required=False,
        ) 
    
    favicon = RelationChoice(
        title=_(u"Favicon do Portal"),
        description=_(u"Logo que será exibido no topo da aba do navegador."),
        source=ObjPathSourceBinder(
            portal_type = 'Image',
            ),
        required=False,
        ) 
    
    text_footer = RichText(
        title=_(u"Conteúdo do rodapé"),
        description=_(u"Texto que deverá aparecer no rodapé do portal."),
        required=False,
        )
    
    itens_menu = schema.List(
         title=_(u"Itens do menu"),
         description=_(u"Selecione os tipos de itens que serão apresentados no menu e no sub-menu."),
         value_type=schema.Choice(source=ListPortalType()),
         required=False,
        )
    
    width_page = schema.Int(
        title=_(u"Largura do site"),
        description=_(u"Largura do site em pixels, insira apenas números iteiros. Esta configuração não se aplica a todos os temas."),
        required=False,
        )