# -*- coding: utf-8 -*-
from vindula.controlpanel import MessageFactory as _
 
from AccessControl import ClassSecurityInfo
from zope.interface import Interface

from Products.ATContentTypes.content.folder import ATFolder
from vindula.controlpanel.content.interfaces import IContainerTopicsControlPanel

from zope.interface import implements
from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from vindula.controlpanel.config import *

# Interface and schema
ContainerTopicsControlPanel_schema =  ATFolder.schema.copy() 
finalizeATCTSchema(ContainerTopicsControlPanel_schema, folderish=True)

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
    ContainerTopicsControlPanel_schema[i].widget.visible = invisivel

class ContainerTopicsControlPanel(ATFolder):
    """ ContainerTopicsControlPanel """
    
    security = ClassSecurityInfo()
    implements(IContainerTopicsControlPanel)
    portal_type = 'ContainerTopicsControlPanel'
    _at_rename_after_creation = True
    schema = ContainerTopicsControlPanel_schema
    
registerType(ContainerTopicsControlPanel, PROJECTNAME)