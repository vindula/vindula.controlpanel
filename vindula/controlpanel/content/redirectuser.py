# -*- coding: utf-8 -*-
from vindula.controlpanel import MessageFactory as _
 
from AccessControl import ClassSecurityInfo
from zope.interface import Interface

from Products.ATContentTypes.content.document import ATDocumentSchema, ATDocumentBase
from vindula.controlpanel.content.interfaces import IRedirectUser

from zope.interface import implements
from archetypes.schemaextender.field import ExtensionField
from Products.Archetypes.atapi import *
from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget
from Products.UserAndGroupSelectionWidget.at import widget

from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from vindula.controlpanel.config import *

from vindula.controlpanel.browser.at.widget import VindulaReferenceSelectionWidget

# Interface and schema
RedirectUser_schema =  ATDocumentSchema.copy() + Schema((

#    BooleanField(
#        name='ativa_regra',
#        default=True,
#        widget=BooleanWidget(
#            label="Ativar Regra",
#            description='Se selecionado, Ativa está regra para os usuários.',
#        ),
#      
#    ),
    
    LinesField(
            name="userORgroups",
            multiValued=1,
            widget = widget.UserAndGroupSelectionWidget(
                label=u"Usuários ou Grupos",
                description=u"Selecione os usuários ou grupos que estarão nesta regra.",required=True,
                ),
            required=True,
            ),
    
    ReferenceField('redirectPath',
        multiValued=0,
        label=_(u"Local de envio"),
        relationship='redirectPath',
        widget=VindulaReferenceSelectionWidget(#default_search_index='SearchableText',
                                      typeview='list',
                                      label=_(u"Local de envio"),
                                      description='Selecione o local para o usuário será enviado.'),
        required=True,
        ),
 

))
finalizeATCTSchema(RedirectUser_schema, folderish=False)
invisivel = {'view':'invisible','edit':'invisible',}

L = ['text'] 
# Dates
L += ['effectiveDate','expirationDate','creation_date','modification_date']   
# Categorization
L += ['subject','relatedItems','location','language']
# Ownership
L += ['creators','contributors','rights']
# Settings
L += ['allowDiscussion','excludeFromNav', 'presentation','tableContents']

for i in L:
    RedirectUser_schema[i].widget.visible = invisivel    

class RedirectUser(ATDocumentBase):
    """ RedirectUser """
    
    security = ClassSecurityInfo()
    implements(IRedirectUser)
    portal_type = 'RedirectUser'
    _at_rename_after_creation = True
    schema = RedirectUser_schema
    
registerType(RedirectUser, PROJECTNAME)
