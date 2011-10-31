# -*- coding: utf-8 -*-
from plone.directives import form
from zope import schema
from vindula.controlpanel import MessageFactory as _

# Interface and schema

class ICategories(form.Schema):
    """ Categories """
    
    title = schema.Text(
        title=_(u"Categorias de Estruturas Organizacionais"),
        description=_(u"Adicione uma categoria por linha."),
        )
