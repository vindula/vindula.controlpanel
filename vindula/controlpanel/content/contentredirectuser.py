# -*- coding: utf-8 -*-
from vindula.controlpanel import MessageFactory as _
 
from AccessControl import ClassSecurityInfo
from zope.interface import Interface

from Products.ATContentTypes.content.folder import ATFolder
from vindula.controlpanel.content.interfaces import IContentRedirectUser

from zope.interface import implements
from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from vindula.controlpanel.config import *

# Interface and schema
ContentRedirectUser_schema =  ATFolder.schema.copy() 
finalizeATCTSchema(ContentRedirectUser_schema, folderish=True)

invisivel = {'view':'invisible','edit':'invisible',}
# Dates
L = ['effectiveDate','expirationDate','creation_date','modification_date']   
# Categorization
L += ['subject','relatedItems','location','language']
# Ownership
L += ['creators','contributors','rights']
# Settings
L += ['allowDiscussion','excludeFromNav']

for i in L:
    ContentRedirectUser_schema[i].widget.visible = invisivel
    
ContentRedirectUser_schema['title'].default = u'Objeto de armazenagem das regras de redirecionamento.'
ContentRedirectUser_schema['description'].default = u'Pasta que guarda os objetos de configuração dos redirecionamento.' 
    

class ContentRedirectUser(ATFolder):
    """ ContentRedirectUser """
    
    security = ClassSecurityInfo()
    implements(IContentRedirectUser)
    portal_type = 'ContentRedirectUser'
    _at_rename_after_creation = True
    schema = ContentRedirectUser_schema
    
registerType(ContentRedirectUser, PROJECTNAME)
