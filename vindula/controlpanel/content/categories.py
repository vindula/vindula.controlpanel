# -*- coding: utf-8 -*-
from zope import schema
from plone.directives import form
from vindula.controlpanel import MessageFactory as _
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from vindula.controlpanel.vocabularies import ListToOrderBy

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
        description = _(u'Selecione abaixo os tipos de ordenação de conteúdo que apareceram nos campos "Ordenar por".'),
        required = False,
        value_type = schema.Choice( source = ListToOrderBy() ),
        )