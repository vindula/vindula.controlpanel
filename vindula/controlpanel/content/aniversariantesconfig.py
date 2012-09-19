# -*- coding: utf-8 -*-
from zope import schema
from plone.directives import form
from vindula.controlpanel import MessageFactory as _

# Interface and schema

class IAniversariantesConfig(form.Schema):
    """ Aniversariantes Config """
    
    list_campos_user = schema.Text(title=unicode("Campos da listagem de aniversariantes", 'utf-8'),
                                   description=unicode("Adicione os campos que serão visualizados na listagem de aniversariantes.\
                                                        Os campos devem possuir o mesmo nome do campo do perfil do usuário e seguir o formato: Label | Campo", 'utf-8'),
                                   default = _(u"[Nome] | [name]\n[Departamento] | [organisational_unit]\n[Data de Aniversário] | [date_birth]\n [E-mail] | [email]"),
                                   required=False)
