# -*- coding: utf-8 -*-
from zope.interface import implements
from zope.app.component.hooks import getSite
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from Products.CMFCore.utils import getToolByName
from vindula.controlpanel import MessageFactory as _
from plone.app.vocabularies.types import BAD_TYPES

from vindula.myvindula.user import ModelsFuncDetails

from AccessControl import ClassSecurityInfo
from Products.CMFCore.permissions import View
from Products.ATContentTypes.criteria import _criterionRegistry

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
                field = obj.__getattr__(self.type)
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
      
#class ListPortalType(object):
#    """ Create SimpleVocabulary for portal types """
#    
#    implements(IContextSourceBinder)
#    
#    def __init__(self):
#        # nome do objeto de configuracao do vindula, deve estar na pasta "control-panel-objects"
#        self.object = object 
#
#    def __call__(self, context):
#        terms = []
#        L = []
#        
#        obj = getToolByName(context, 'portal_types')
#        pprop = getToolByName(context, 'portal_properties')
#        self.navProps = pprop.navtree_properties
#        
#        if obj:
#            itens  = [t for t in obj.listContentTypes()
#                        if t not in self.navProps.metaTypesNotToList and
#                           t not in BAD_TYPES]
#            
#            if itens is not None:
#                for item in itens:
#                    terms.append(SimpleTerm(item, item, _(u'option_category', default=unicode(item))))
#                      
#        return SimpleVocabulary(terms)
    
class ListUserPortal(object):
    """ Create SimpleVocabulary for user portal """
    
    implements(IContextSourceBinder)
    
    def __init__(self):
        # nome do objeto de configuracao do vindula, deve estar na pasta "control-panel-objects"
        self.object = object 

    def __call__(self, context):
        acl_users = getToolByName(context, 'acl_users')
        
        users = ModelsFuncDetails().get_allFuncDetails() #acl_users.getUsers()
        terms = []
        
        if users is not None:
            for user in users:
                member_id = user.username
                member_name = user.name or member_id
                terms.append(SimpleTerm(member_id, member_id, _(u'option_category', default=unicode(member_name))))
                
        return SimpleVocabulary(terms)
    
class ListExitForm(object):
    """ Create SimpleVocabulary for Exit of form """
    implements(IContextSourceBinder)
    def __init__(self):
        self.object = object 
    def __call__(self, context):
        terms = []
        obj = {'email':u'Enviar um e-mail com os dados do formulário',
               'savedb':u'Salvar o formulário no banco de dados para uma futura consulta',
               'content_type':u'Criar um tipo de conteúdo para cada resultado do formulário'}
        
        for i in obj.keys():
            terms.append(SimpleTerm(i, i, _(u'option_category', default=obj[i])))
                              
        return SimpleVocabulary(terms)      

class ListDestinoForm(object):
    """ Create SimpleVocabulary for destination of form """
    implements(IContextSourceBinder)
    def __init__(self):
        self.object = object 
    def __call__(self, context):
        terms = []
        obj = {'doc_plone':u'Enviar o usuário a um documento do plone',
               'url':u'Redireciona o usuário  a uma url especifica',
               'parameto':u'Envia parâmetro a outro formulário ou página'}
        
        for i in obj.keys():
            terms.append(SimpleTerm(i, i, _(u'option_category', default=obj[i])))
                      
        return SimpleVocabulary(terms)        
      
class ListDisplayAlerts(object):
    """ Create SimpleVocabulary for Display of Alerts """
    implements(IContextSourceBinder)
    def __init__(self):
        self.object = object 
    def __call__(self, context):
        terms = []
        obj = {'error':u'Advertência: Mensagem utilizada para indicar eventos de alta criticidade',
               'warning':u'Atenção: Mensagem utilizada para indicar eventos com media criticidade',
               'info':u'Informativo: Mensagem utilizada para indicar eventos com baixa criticidade'}
        
        for i in obj.keys():
            terms.append(SimpleTerm(i, i, _(u'option_category', default=obj[i])))
        
        return SimpleVocabulary(terms)
    
    
class ListToOrderBy(object):
    """ Create SimpleVocabulary for Display of Alerts """
    implements(IContextSourceBinder)
    security = ClassSecurityInfo()
    security.declareProtected(View, 'criteriaByIndexId')
    security.declareProtected(View, 'validateAddCriterion')
    
    def __init__(self):
        self.object = object 
    def __call__(self, context):
        tool = getToolByName(self, 'portal_atct')
        listFields = tool.getEnabledFields() 
        fields = [ field
                    for field in listFields
                    if self.validateAddCriterion(field[0], 'ATSortCriterion') ]
        
        return wrap_in_terms(fields) 
    
    def criteriaByIndexId(self, indexId):
        catalog_tool = getToolByName(getSite(), 'portal_catalog')
        indexObj = catalog_tool.Indexes[indexId]
        results = _criterionRegistry.criteriaByIndex(indexObj.meta_type)
        return results
    
    def validateAddCriterion(self, indexId, criteriaType):
        """Is criteriaType acceptable criteria for indexId
        """
        return criteriaType in self.criteriaByIndexId(indexId)
    
def wrap_in_terms(items):
    """This just wraps all the study sectors in a thing called vocabulary
    which is needed to let the z3c.form machinery display them in select
    boxes or what ever is appropriate.
    """
    terms = []
    if items:
        for item in items:
            term = SimpleTerm(
                    title = item[1],
                    value = item,
            )
            terms.append(term)
  
    return SimpleVocabulary(terms)