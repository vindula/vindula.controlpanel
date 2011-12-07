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
        title=_(u"Lista de macros disponiveis"),
        description=_(u"Adicione as macro que podem ser utilizadas na tipo de conteudo 'Vindula Content Macro',<br />\
                        Adicione uma macro por linha, no padrão '[Nome] | [Pagina] | [Macro]'."),
        required=False,
        )
    