# -*- coding: utf-8 -*-
from vindula.controlpanel import MessageFactory as _
 
from AccessControl import ClassSecurityInfo
from zope.interface import Interface

from Products.ATContentTypes.content.folder import ATFolder
from vindula.controlpanel.content.interfaces import ITopicControlPanel

from zope.interface import implements
from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from vindula.controlpanel.config import *

from Products.UserAndGroupSelectionWidget.at import widget
from vindula.controlpanel.browser.at.widget import VindulaReferenceSelectionWidget

# Interface and schema
TopicControlPanel_schema =  ATFolder.schema.copy() + Schema((
    
    LinesField(
        name="usersOrGroupsTopic",
        multiValued=1,
        widget = widget.UserAndGroupSelectionWidget(
            label=u"Usuarios ou Grupos",
            description=u"Selecione os usuarios ou grupos que terao permissao para acessar todo conteudo deste topico.",
            ),
        required=True,
    ),
    
)) 
finalizeATCTSchema(TopicControlPanel_schema, folderish=True)

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
    TopicControlPanel_schema[i].widget.visible = invisivel

class TopicControlPanel(ATFolder):
    """ TopicControlPanel """
    
    security = ClassSecurityInfo()
    implements(ITopicControlPanel)
    portal_type = 'TopicControlPanel'
    _at_rename_after_creation = True
    schema = TopicControlPanel_schema
    
registerType(TopicControlPanel, PROJECTNAME)