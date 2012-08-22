# -*- coding: utf-8 -*-
from vindula.controlpanel import MessageFactory as _
from AccessControl import ClassSecurityInfo
from Products.ATContentTypes.content.document import ATDocumentSchema, ATDocumentBase
from vindula.controlpanel.content.interfaces import IFieldSetMyvindula

from zope.interface import implements
from Products.Archetypes.atapi import *

from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from vindula.controlpanel.config import *

from vindula.controlpanel.browser.at.widget import VindulaReferenceSelectionWidget

# Interface and schema
FieldSetMyvindula_schema =  ATDocumentSchema.copy() + Schema((

    ReferenceField('logo',
        multiValued=0,
        allowed_types=('Image'),
        label=_(u"Logo Categoria"),
        relationship='logo',
        required=True,
        widget=VindulaReferenceSelectionWidget(
            #default_search_index='SearchableText',
            label=_(u"Logo Categoria"),
            description='A imagem selecionada será exibida ao lado dos campos do perfil do usuário.'),
    ),

))
finalizeATCTSchema(FieldSetMyvindula_schema, folderish=False)
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
    FieldSetMyvindula_schema[i].widget.visible = invisivel    

class FieldSetMyvindula(ATDocumentBase):
    """ FieldSetMyvindula """
    
    security = ClassSecurityInfo()
    implements(IFieldSetMyvindula)
    portal_type = 'FieldSetMyvindula'
    _at_rename_after_creation = True
    schema = FieldSetMyvindula_schema
    
registerType(FieldSetMyvindula, PROJECTNAME)
