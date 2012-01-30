# -*- coding: utf-8 -*-
from zope import schema
from plone.directives import form
from vindula.controlpanel import MessageFactory as _

# Interface and schema

class IVindulaPensamentosConfig(form.Schema):
    """ Vindula Recados Config """
    
    ativa_pensamentos = schema.Bool(
                title=_(u'label_ativa_pensamentos', default=u'Ativar a visualização dos pensametos no portal Myvindula'),
                description=_(u'help_activ_holerite', default=u'Se selecionado, Ativa a opção de pensamentos para todos os usuários do Myvindula no portal'),
                default=True
                )