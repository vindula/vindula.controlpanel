# -*- coding: utf-8 -*-
from zope import schema
from plone.directives import form
from vindula.controlpanel import MessageFactory as _

# Interface and schema

class IVindulaEditFuncConfig(form.Schema):
    """ Vindula Edit Func Config """
    
    ativa_editfunc = schema.Bool(
                     title=_(u'label_ativa_editfunc', default=u'Ativar a opção do usuário poder editar seu perfil no portal Myvindula'),
                     description=_(u'help_activ_holerite', default=u'Se selecionado, ativa a opção do usuário poder editar seu perfil no portal Myvindula'),
                     default=True
                     )
