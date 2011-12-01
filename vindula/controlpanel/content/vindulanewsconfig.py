# -*- coding: utf-8 -*-
from zope import schema
from plone.directives import form
from vindula.controlpanel import MessageFactory as _

# Interface and schema

class IVindulaNewsConfig(form.Schema):
    """ Vindula News Config """
    
    ativa_conpartilhamento = schema.Bool(
                title=_(u'label_ativa_conpartilhamento', default=u'Ativar o compartilhamento nas redes sociais'),
                description=_(u'help_activ_share', default=u'Se selecionado, Ativa a opção de compartilhamento nas redes sociais de todos os itens "Noticia" do portal'),
                default=False
                )
