# -*- coding: utf-8 -*-
from zope import schema
from plone.directives import form
from vindula.controlpanel import MessageFactory as _

# Interface and schema

class IVindulaUserConfig(form.Schema):
    """ Vindula User Config """
    
    ativa_muit_user = schema.Bool(
                title=_(u'label_ativa_muit_user', default=u'Ativar o mecanismo para muitos usuários no myvindula'),
                description=_(u'help_ativa_muit_user', default=u'Se selecionado, Ativa a opção de muitos usuários no myvindula'),
                default=False
                )
