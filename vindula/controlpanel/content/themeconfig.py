# -*- coding: utf-8 -*-
from zope import schema
from zope.interface import Interface
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.app.textfield import RichText
from z3c.relationfield.schema import RelationChoice
from vindula.controlpanel import MessageFactory as _

# Interface

class IThemeConfig(Interface):
    """ Theme Settings interface """

    logo_top = RelationChoice(
        title=_(u"Logo do Cabeçalho"),
        description=_(u"Logo que será exibido no cabeçalho do portal. Tamanho sugerido para a imagem: 00px x 00px."),
        source=ObjPathSourceBinder(
            portal_type = 'Image',
            ),
        required=False,
        ) 
    
    text_footer = RichText(
        title=_(u"Conteúdo do rodapé"),
        description=_(u"Texto que deverá aparecer no rodapé do portal."),
        default=_(u"© 2011 Vindula Software. All Rights Reserved"),
        required=False,
        )