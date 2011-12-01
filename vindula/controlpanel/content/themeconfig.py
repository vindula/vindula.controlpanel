# -*- coding: utf-8 -*-
from zope import schema
from zope.interface import Interface
from zope.interface import implements
from zope.app.component.hooks import getSite
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IContextSourceBinder
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.app.textfield import RichText
from z3c.relationfield.schema import RelationChoice
from Products.CMFCore.utils import getToolByName
from plone.app.vocabularies.types import BAD_TYPES
from vindula.controlpanel import MessageFactory as _

    
class ListPortalType(object):
    implements(IContextSourceBinder)
    
    def __init__(self):
        # nome do objeto de configuracao do vindula, deve estar na pasta "control-panel-objects"
        self.object = object 

    def __call__(self, context):
        terms = []
        L = []

        obj = getToolByName(context, 'portal_types')
        pprop = getToolByName(context, 'portal_properties')
        self.navProps = pprop.navtree_properties
        
        if obj:
            itens  = [t for t in obj.listContentTypes()
                        if t not in self.navProps.metaTypesNotToList and
                           t not in BAD_TYPES]
            
            if itens is not None:
                for item in itens:
                    #id = item.id
                    #type = item.Metatype()
                    #name = item.Title()
                   
                    terms.append(SimpleTerm(item, item, _(u'option_category', default=unicode(item))))
                      
        return SimpleVocabulary(terms)    
    
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
    
    text_footer = RichText(
        title=_(u"Conteúdo do rodapé"),
        description=_(u"Texto que deverá aparecer no rodapé do portal."),
        required=False,
        )
    
    itens_menu = schema.List(
         title=_(u"Itens do menu"),
         description=_(u"Selecione os tipos de itens que serão apresentados no menu e no sub-menu"),
         value_type=schema.Choice(source=ListPortalType()),
         required=False,
        )
    

    