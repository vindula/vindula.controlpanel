# -*- coding: utf-8 -*-
from vindula.controlpanel import MessageFactory as _
 
from AccessControl import ClassSecurityInfo
from zope.interface import Interface

from Products.ATContentTypes.content.folder import ATFolder
from vindula.controlpanel.content.interfaces import IObjectsControlPanel

from zope.interface import implements
from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from vindula.controlpanel.config import *

# Interface and schema
ObjectsControlPanel_schema =  ATFolder.schema.copy() 
finalizeATCTSchema(ObjectsControlPanel_schema, folderish=True)

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
    ObjectsControlPanel_schema[i].widget.visible = invisivel

class ObjectsControlPanel(ATFolder):
    """ ContainerTopicsControlPanel """
    
    security = ClassSecurityInfo()
    implements(IObjectsControlPanel)
    portal_type = 'ContainerTopicsControlPanel'
    _at_rename_after_creation = True
    schema = ObjectsControlPanel_schema
    
registerType(ObjectsControlPanel, PROJECTNAME)