# -*- coding: utf-8 -*-
from zope.interface import implements
from zope.app.component.hooks import getSite
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from Products.CMFCore.utils import getToolByName
from vindula.controlpanel import MessageFactory as _
from plone.app.vocabularies.types import BAD_TYPES


class ControlPanelObjects(object):
    """ Create SimpleVocabulary for any Choice Fields """

    implements(IContextSourceBinder)
    
    def __init__(self, object, type):
        # nome do objeto de configuracao do vindula, deve estar na pasta "control-panel-objects"
        self.object = object 
        # nome do campo do objeto onde ira buscar os valores, precisa ser do tipo "schema.Text"
        self.type = type 

    def __call__(self, context):
        terms = []
        #terms.append(SimpleTerm('', '--NOVALUE--', _(u'option_category', default=u'Selecione')))

        try:
            obj = getSite()['control-panel-objects'][self.object]
        except:
            obj = None
        
        if obj:
            try:
                field = obj.__getattribute__(self.type)
            except:
                field = None
            if field is not None:
                items = field.splitlines()
                n = 0
                for item in items:
                    id = str(n) + item.lower().replace(' ', '-')
                    n += 1
                    terms.append(SimpleTerm(id, id, _(u'option_category', default=unicode(item))))
                      
        return SimpleVocabulary(terms)
    
class ControlPanelMacro(object):
    """ Create SimpleVocabulary for any Choice Fields """

    implements(IContextSourceBinder)
    
    def __init__(self, object, type):
        # nome do objeto de configuracao do vindula, deve estar na pasta "control-panel-objects"
        self.object = object 
        # nome do campo do objeto onde ira buscar os valores, precisa ser do tipo "schema.Text"
        self.type = type 

    def __call__(self, context):
        terms = []
        #terms.append(SimpleTerm('', '--NOVALUE--', _(u'option_category', default=u'Selecione')))

        try:obj = getSite()['control-panel-objects'][self.object]
        except:obj = None
        
        if obj:
            try:
                field = obj.__getattribute__(self.type)
            except:
                field = None
            if field is not None:
                items = field.splitlines()
                n = 0
                for item in items:
                    L = item.split('|')
                    name = L[0]
                    id = L[1].replace(' ','') +'&'+L[2].replace(' ','')
                    #id = str(n) + item.lower().replace(' ', '-')
                    
                    n += 1
                    terms.append(SimpleTerm(id, id, _(u'option_category', default=unicode(name))))
                      
        return SimpleVocabulary(terms)
      
class ListPortalType(object):
    """ Create SimpleVocabulary for portal types """
    
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
                    terms.append(SimpleTerm(item, item, _(u'option_category', default=unicode(item))))
                      
        return SimpleVocabulary(terms)
    
    
class ListExitForm(object):
    """ Create SimpleVocabulary for Exit of form """
    implements(IContextSourceBinder)
    def __init__(self):
        # nome do objeto de configuracao do vindula, deve estar na pasta "control-panel-objects"
        self.object = object 
    def __call__(self, context):
        terms = []
        
        terms.append(SimpleTerm('email', 'email', _(u'option_category', default=u'Enviar um e-mail com os dados do form')))
        terms.append(SimpleTerm('savedb', 'savedb', _(u'option_category', default=u'Salvar o formulário no banco de dados para uma futura consulta')))
                      
        return SimpleVocabulary(terms)      
    
      
class ListDisplayAlerts(object):
    """ Create SimpleVocabulary for Display of Alerts """
    
    implements(IContextSourceBinder)
    
    def __init__(self):
        # nome do objeto de configuracao do vindula, deve estar na pasta "control-panel-objects"
        self.object = object 
    
    def __call__(self, context):
        terms = []
        terms.append(SimpleTerm('error', 'error', _(u'option_category', default=u'Advertência: Mensagem utilizada para indicar eventos de alta criticidade')))
        terms.append(SimpleTerm('info', 'info', _(u'option_category', default=u'Informativo: Mensagem utilizada para indicar eventos com baixa criticidade')))
        
        return SimpleVocabulary(terms)