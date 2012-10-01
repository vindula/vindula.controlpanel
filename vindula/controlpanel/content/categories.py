# -*- coding: utf-8 -*-
from zope import schema
from plone.directives import form
from vindula.controlpanel import MessageFactory as _

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
    
    orgaoEdital = schema.Text(
        title=_(u"Orgaos dos editais"),
        description=_(u"""Adicione orgãos para ser relacionado a um edital.<br>
                          Adicione um orgão por linha.
                       """),
        required=False,
        )
    
    modalidadeEdital = schema.Text(
        title=_(u"Modalidade dos editais"),
        description=_(u"""Adicione modalidades para ser relacionado a um edital.<br>
                          Adicione uma modalidade por linha.
                       """),
        required=False,
        )
    