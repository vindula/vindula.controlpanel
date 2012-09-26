# -*- coding: utf-8 -*-
from vindula.controlpanel import MessageFactory as _
 
from AccessControl import ClassSecurityInfo
from zope.interface import Interface

from Products.ATContentTypes.content import schemata, base
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
SubtopicControlPanel_schema =  schemata.ATContentTypeSchema.copy() + Schema((
    
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
            label=u"Usuários ou grupos",
            description=u"Selecione os usuários ou grupos que terão permissão para acessar esse sub-tópico.",
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
    
))
finalizeATCTSchema(SubtopicControlPanel_schema, folderish=False)
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
    SubtopicControlPanel_schema[i].widget.visible = invisivel    

class SubtopicControlPanel(base.ATCTContent):
    """ SubtopicControlPane """
    
    security = ClassSecurityInfo()
    implements(ISubtopicControlPanel)
    portal_type = 'SubtopicControlPane'
    _at_rename_after_creation = True
    schema = SubtopicControlPanel_schema

registerType(SubtopicControlPanel, PROJECTNAME)