# -*- coding: utf-8 -*-
from zope import schema
from plone.directives import form
from vindula.controlpanel import MessageFactory as _

# Interface and schema

class IVindulaRecadosConfig(form.Schema):
    """ Vindula Recados Config """
    
    ativa_recados = schema.Bool(
                title=_(u'label_ativa_recados', default=u'Ativar os recados aos usuários do Myvindula no portal'),
                description=_(u'help_activ_share', default=u'Se selecionado, Ativa a opção de recados para todos os usuários do Myvindula no portal'),
                default=True
                )
