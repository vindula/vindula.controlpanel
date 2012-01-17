# -*- coding: utf-8 -*-
from zope import schema
from plone.directives import form
from vindula.controlpanel import MessageFactory as _

# Interface and schema

class IVindulaHoleritesConfig(form.Schema):
    """ Vindula Recados Config """
    
    ativa_holerite = schema.Bool(
                title=_(u'label_ativa_holerites', default=u'Ativar a visualização de holerites no portal Myvindula'),
                description=_(u'help_activ_holerite', default=u'Se selecionado, Ativa a opção de holerite para todos os usuários do Myvindula no portal'),
                default=True
                )
