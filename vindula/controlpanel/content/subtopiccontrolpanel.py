# -*- coding: utf-8 -*-
from vindula.controlpanel import MessageFactory as _
 
from AccessControl import ClassSecurityInfo
from zope.interface import Interface

from Products.ATContentTypes.content.document import ATDocumentSchema, ATDocumentBase
from vindula.controlpanel.content.interfaces import ISubtopicControlPanel

from zope.interface import implements
from archetypes.schemaextender.field import ExtensionField
from Products.Archetypes.atapi import *
from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget
from Products.UserAndGroupSelectionWidget.at import widget

from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from vindula.controlpanel.config import *

from vindula.controlpanel.browser.at.widget import VindulaReferenceSelectionWidget

# Interface and schema
SubtopicControlPanel_schema =  ATDocumentSchema.copy() + Schema((
    
    StringField(
        name='viewName',
        searchable=0,
        required=0,
        widget=StringWidget(
            label='Nome da View',
            description="Insira o nome da view a ser carregada, pode ser inserida com ou sem @@.",
        ),
    ),
    
    LinesField(
        name="usersOrGroupsSub",
        multiValued=1,
        widget = widget.UserAndGroupSelectionWidget(
            label=u"Usuarios ou grupos",
            description=u"Selecione os usuários ou grupos que terão permissão para acessar esse subtópico.",
            ),
        required=False,
    ),
            
    BooleanField(
        name='useSuperiorGroups',
        default=True,
        widget=BooleanWidget(
            label="Herdar usuários e grupos",
            description='Herdar configurações de usuários e grupos do tópico "pai".',
        ),
    ),
    
    BooleanField(
        name='useAjaxMode',
        default=False,
        widget=BooleanWidget(
            label="Renderizar a view por ajax.",
            description='Ative essa opção para renderizar a view ao lado por ajax.<br>Essa opção não funciona bem em todos os tipos de conteúdo.',
        ),
    ),
    
#    ReferenceField('icon',
#        multiValued=0,
#        allowed_types=('Image'),
#        relationship='iconTopic',
#        widget=VindulaReferenceSelectionWidget(
#            label=_(u"Icone do topico"),
#            description='Icone que aparecera ao lado do topico na lista.'),
#    ),
    
))
finalizeATCTSchema(SubtopicControlPanel_schema, folderish=False)
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
    SubtopicControlPanel_schema[i].widget.visible = invisivel    

class SubtopicControlPanel(ATDocumentBase):
    """ SubtopicControlPane """
    
    security = ClassSecurityInfo()
    implements(ISubtopicControlPanel)
    portal_type = 'SubtopicControlPane'
    _at_rename_after_creation = True
    schema = SubtopicControlPanel_schema
    
registerType(SubtopicControlPanel, PROJECTNAME)