# -*- coding: utf-8 -*-
from five import grok

from vindula.controlpanel import MessageFactory as _
from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName

from vindula.controlpanel.content.interfaces import IVindulaCategories
from Products.ATContentTypes.content import schemata, base

from zope.interface import implements
from Products.Archetypes.atapi import *
from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from vindula.controlpanel.config import *
from zope.app.component.hooks import getSite
from vindula.controlpanel.browser.at.widget import VindulaReferenceSelectionWidget
from Products.ATContentTypes.criteria import _criterionRegistry

# Local imports
from Products.DataGridField import DGFMessageFactory as _
from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column
from Products.DataGridField.SelectColumn import SelectColumn
from Products.DataGridField.RadioColumn import RadioColumn
from Products.DataGridField.CheckboxColumn import CheckboxColumn
from Products.DataGridField.FixedColumn import FixedColumn
from Products.DataGridField.DataGridField import FixedRow
from Products.DataGridField.HelpColumn import HelpColumn


VindulaCategories_schema =  schemata.ATContentTypeSchema.copy() + Schema((                                                          
  
    
    TextField(
        name='list_macros',
        widget=TextAreaWidget(
            label=_(u"Lista de macros disponíveis."),
            description=_(u"Adicione as macro que podem ser utilizadas no tipo de conteúdo 'Vindula Content Macro',<br />\
                            Adicione uma macro por linha, no padrão '[Nome] | [Pagina] | [Macro]'."),
            
            label_msgid='vindula_controlpanel_label_list_macros',
            description_msgid='vindula_controlpanel_help_list_macros',
            i18n_domain='vindula_controlpanel',
        ),
        
        #TODO -  Ver porque nao está incluindo um valor por padrao
        default = 'Lista de usuários | myvindulalistall | page-view\nLista de usuários | myvindulalistall | page-view<br />\
                  Perfil do Usuário | myvindula-user-perfil | page-view\nNovos usuários | myvindula-news-employee | page-view<br />\
                  Pensamentos | howareu-list-all | page-view',
                  
        required=False,
    ),
    
    LinesField(
        name='order_list',
        widget=MultiSelectionWidget(
            label=_(u"Itens que aparaceram nos campos de ordenação do portal"),
            description = _(u'Selecione abaixo os tipos de ordenação de conteúdo que aparecerão nos campos "Ordenar por".'),
            label_msgid='vindula_controlpanel_label_order_list',
            description_msgid='vindula_controlpanel_order_list',
            i18n_domain='vindula_controlpanel',
            format='checkbox',
        ),
        vocabulary='listToOrderBy',
        required=False,
    ),
    
    LinesField(
        name='profile_layout',
        widget=SelectionWidget(
            label=_(u"Selecione o layout da área de perfil"),
            description = _(u'Selecione qual layout será mostrado na área de perfil do usuário.'),
            label_msgid='vindula_controlpanel_label_profile_layout',
            description_msgid='vindula_controlpanel_profile_layout',
            i18n_domain='vindula_controlpanel',
            format='select',
        ),
        vocabulary=[('default', 'Layout padrão'),('simple', 'Layout simples')],
        required=False,
    ),
    
    ReferenceField('folder_image',
        multiValued=False,
        allowed_types=('Folder', 'VindulaFolder'),
        relationship='folder_image',
        widget=VindulaReferenceSelectionWidget(
            default_search_index='SearchableText',
            label=_(u"Seleção da pasta padrão de imagens"),
            description=_(u"Selecione a pasta que contêm as imagems do portal."),
            label_msgid='vindula_themedefault_label_folder_image',
            description_msgid='vindula_themedefault_help_folder_image',
            i18n_domain='vindula_themedefault',
            ),
        required=False
    ),
    
    TextField(
        name='orgaoEdital',
        widget=TextAreaWidget(
            label=_(u"Órgãos dos editais"),
            description=_(u"""Adicione orgãos para serem relacionados a um edital.<br>
                              Adicione um orgão por linha.
                           """),
            label_msgid='vindula_controlpanel_label_orgaoEdital',
            description_msgid='vindula_controlpanel_help_orgaoEdital',
            i18n_domain='vindula_controlpanel',
        ),
        required=False,
    ),
    
    TextField(
        name='modalidadeEdital',
        widget=TextAreaWidget(
            label=_(u"Modalidade dos editais"),
            description=_(u"""Adicione modalidades para serem relacionados a um edital.<br>
                              Adicione uma modalidade por linha.
                           """),
            label_msgid='vindula_controlpanel_label_modalidadeEdital',
            description_msgid='vindula_controlpanel_help_modalidadeEdital',
            i18n_domain='vindula_controlpanel',
        ),
        required=False,
    ),

    TextField(
        name='tipoUnidade',
        widget=TextAreaWidget(
            label=_(u"Tipos de Unidades Organizacionais"),
            description=_(u"""Adicione Tipos de Unidades Organizacionais para serem relacionados.<br>
                              Adicione um Tipo por linha.
                           """),
            label_msgid='vindula_controlpanel_label_tipoUnidade',
            description_msgid='vindula_controlpanel_help_tipoUnidade',
            i18n_domain='vindula_controlpanel',
        ),
        required=False,
    ),
    
    TextField(
        name='categories',
        widget=TextAreaWidget(
            label=_(u"Categorias dos menus"),
            description=_(u"""Adicione categorias para o menu. Uma por linha.
                           """),
            label_msgid='vindula_controlpanel_label_categories',
            description_msgid='vindula_controlpanel_help_categories',
            i18n_domain='vindula_controlpanel',
        ),
        required=False,
    ),
                                                                 
    DataGridField(
        name='categories_additem',
        columns=('content_type', 'catagories'),
#        fixed_rows = "getPredefinedSkillsData",
        allow_delete = True,
        allow_insert = True,
        allow_reorder = True,
        widget = DataGridWidget(
            label="Categorizar tipos de conteúdo",
            description="Selecione em qual categoria, definida acima, o tipo de conteúdo deve aparacer.",
            description_msgid='vindula_controlpanel_help_categories_additem',
            label_msgid='vindula_controlpanel_label_categories_additem',
            columns= {
                "content_type" : SelectColumn(_(u"Tipos de Conteúdo"), vocabulary="getContentTypes"),
                "catagories" : SelectColumn(_(u"Categorias"), vocabulary="getCategories")
            }
        ),
    ),                                                            
))

finalizeATCTSchema(VindulaCategories_schema, folderish=False)

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
    VindulaCategories_schema[i].widget.visible = invisivel  

class VindulaCategories(base.ATCTContent):
    """ VindulaCategories """
    security = ClassSecurityInfo()
    implements(IVindulaCategories)
    portal_type = 'Categories'
    _at_rename_after_creation = True
    schema = VindulaCategories_schema
    
    def getCategories(self):
        L=[]
        categories = self.categories().replace('\r','').split('\n')
        for cat in categories:
            L.append(((cat), _(cat)))
        return DisplayList(tuple(L))
    
    def getContentTypes(self):
        return DisplayList(tuple([ (id.lower(), id) for id in self.portal_types.listContentTypes() ]))

    
    def listToOrderBy(self):
        tool = getToolByName(self, 'portal_atct')
        listFields = tool.getEnabledFields()
        fields = [ (str(field), field[1]) for field in listFields if self.validateAddCriterion(field[0], 'ATSortCriterion') and field[0] not in ['effective', 'sortable_title']]

        return fields
    
    def criteriaByIndexId(self, indexId):
        catalog_tool = getToolByName(getSite(), 'portal_catalog')
        indexObj = catalog_tool.Indexes[indexId]
        results = _criterionRegistry.criteriaByIndex(indexObj.meta_type)
        return results
    
    def validateAddCriterion(self, indexId, criteriaType):
        """Is criteriaType acceptable criteria for indexId
        """
        return criteriaType in self.criteriaByIndexId(indexId)

registerType(VindulaCategories, PROJECTNAME)