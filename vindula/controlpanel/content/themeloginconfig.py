# -*- coding: utf-8 -*-
from five import grok

from Products.ATContentTypes.content.document import ATDocumentSchema, ATDocumentBase
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from vindula.controlpanel.browser.at.widget import VindulaReferenceSelectionWidget
from vindula.controlpanel.content.interfaces import IThemeLoginConfig
from vindula.controlpanel import MessageFactory as _
from vindula.controlpanel.config import *

from Products.validation.validators.ExpressionValidator import ExpressionValidator
from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget
from zope.interface import implements, Interface, invariant, Invalid
from Products.SmartColorWidget.Widget import SmartColorWidget
from zope.app.component.hooks import getSite
from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *

# Interface and schema
""" Vindula Config Login"""
ThemeLoginConfig_schema =  ATDocumentSchema.copy() + Schema((
    StringField(
        name = 'tipoLogin',
        widget=SelectionWidget(
            label='Tipo da tela de login',
            description="Selecione o tipo da tela de login do portal.",
            format = 'radio',
        ),
        vocabulary = [('classico', 'Login clássico'), ('grafico','Login gráfico'),],
        default='clássico',
    ),
    
    BooleanField(
        name='ativaRedirect',
        default=True,
        widget=BooleanWidget(
            label="Ativar a função de redirecionar",
            description='Se selecionado ativa a função de redirecionamento dos usuário',
        ),
    ),
    
    #Schemata Layout
    
    ReferenceField('imagemBackground',
        multiValued=0,
        allowed_types=('Image'),
        label=_(u"Imagem de background"),
        relationship='imageBackground',
        widget=VindulaReferenceSelectionWidget(
            label=_(u"Imagem de background"),
            description='A imagem selecionada será exibida no fundo da tela de login gráfico.'
        ),
        schemata = 'Layout'
    ),
    
    ReferenceField('imagemBackground',
        multiValued=0,
        allowed_types=('Image'),
        label=_(u"Imagem de background"),
        relationship='imageBackground',
        widget=VindulaReferenceSelectionWidget(
            label=_(u"Imagem de background"),
            description='A imagem selecionada será exibida no fundo da tela de login gráfico.'
        ),
        schemata = 'Layout'
    ),
    
    StringField(
        name = 'posicaoImagem',
        widget=SelectionWidget(
            label='Posição da imagem',
            description="Selecione a posição que a imagem de fundo deverá aparecer.",
            format = 'select',
        ),
        vocabulary = [('estender','Estender'),('centro', 'Centralizar'), ('lado_lado', 'Lado a Lado')],
        schemata = 'Layout'
    ),  
    
    StringField(
        name = 'corSolidaBackground',
        searchable=0,
        required=0,
        widget=SmartColorWidget(
            label='Cor solida do background',
            description="Cor sólida que aparacerá no fundo da tela de login gráfico.",
        ),
        schemata = 'Layout'
    ),  
                                                        
))

finalizeATCTSchema(ThemeLoginConfig_schema, folderish=False)

invisivel = {'view':'invisible','edit':'invisible',}
ThemeLoginConfig_schema['title'].widget.visible = invisivel
ThemeLoginConfig_schema['description'].widget.visible = invisivel
ThemeLoginConfig_schema['text'].widget.visible = invisivel

# Dates
L = ['effectiveDate','expirationDate','creation_date','modification_date']   
# Categorization
L += ['subject','relatedItems','location','language']
# Ownership
L += ['creators','contributors','rights']
# Settings
L += ['allowDiscussion','excludeFromNav', 'presentation','tableContents']

for i in L:
    ThemeLoginConfig_schema[i].widget.visible = invisivel    

class ThemeLoginConfig(ATDocumentBase):
    """ ThemeLoginConfig """
    
    security = ClassSecurityInfo()
    implements(IThemeLoginConfig)
    portal_type = 'ThemeLoginConfig'
    _at_rename_after_creation = True
    schema = ThemeLoginConfig_schema

registerType(ThemeLoginConfig, PROJECTNAME)

class ThemeLoginConfigView(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('view')

    def render(self):
        pass

    def update(self):
        url = self.context.absolute_url()+'/edit'
        self.context.REQUEST.response.redirect(url)

class MyvindulaConfigLogin(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('myvindula-conf-login')

    def render(self):
        pass
    
    def configurador(self):
        if 'control-panel-objects' in  getSite().keys():
            control = getSite()['control-panel-objects']
            if 'ThemeLoginConfig' in control.keys():
                return control['ThemeLoginConfig']
            else:
                return False
        else:
            return False
    
    def check_redirect(self):
        if self.configurador():
            control = self.configurador()
            return control.getAtivaRedirect()
        else:
            return True
        