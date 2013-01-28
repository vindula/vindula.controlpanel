# -*- coding: utf-8 -*-
from zope import schema
from plone.directives import form
from vindula.controlpanel import MessageFactory as _
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from vindula.controlpanel.vocabularies import ListToOrderBy
from plone.formwidget.contenttree import ObjPathSourceBinder
from z3c.relationfield.schema import RelationChoice

#from collective.plonefinder.widgets.referencewidget import FinderSelectWidget

# Interface and schema

class ICategories(form.Schema):
    """ Categories """
    
    orgstructure = schema.Text(
        title=_(u"Categorias de Estruturas Organizacionais"),
        description=_(u"Adicione uma categoria por linha."),
        required=False,
        )
    
    list_macros = schema.Text(
        title=_(u"Lista de macros disponíveis"),
        description=_(u"Adicione as macro que podem ser utilizadas no tipo de conteúdo 'Vindula Content Macro',<br />\
                        Adicione uma macro por linha, no padrão '[Nome] | [Pagina] | [Macro]'."),
        default = _(u"Lista de usuários | myvindulalistall | page-view\nLista de usuários | myvindulalistall | page-view\n\
                      Perfil do Usuário | myvindula-user-perfil | page-view\nNovos usuários | myvindula-news-employee | page-view\n\
                      Pensamentos | howareu-list-all | page-view"),
        required=False,
        )
    
    form.widget(order_list=CheckBoxFieldWidget)
    order_list = schema.List(
        title = _(u'Itens que aparaceram nos campos de ordenação do portal.'),
        description = _(u'Selecione abaixo os tipos de ordenação de conteúdo que aparecerão nos campos "Ordenar por".'),
        required = False,
        value_type = schema.Choice( source = ListToOrderBy() ),
        )
    
    #form.widget(folder_image=FinderSelectWidget)
    folder_image = RelationChoice(title=_(u"Seleção da pasta padrão de imagens"),
                                  description=_(u"Selecione a pasta que contêm as imagems do portal."),
                                  source=ObjPathSourceBinder(portal_type = ('Folder', 'VindulaFolder'),
                                                             review_state = ('published','internal','external')
                                                             ),
                                  required=False)
    
    orgaoEdital = schema.Text(
        title=_(u"Órgãos dos editais"),
        description=_(u"""Adicione orgãos para serem relacionados a um edital.<br>
                          Adicione um orgão por linha.
                       """),
        required=False,
        )
    
    modalidadeEdital = schema.Text(
        title=_(u"Modalidade dos editais"),
        description=_(u"""Adicione modalidades para serem relacionados a um edital.<br>
                          Adicione uma modalidade por linha.
                       """),
        required=False,
        )