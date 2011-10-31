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