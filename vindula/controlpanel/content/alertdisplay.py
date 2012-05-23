# -*- coding: utf-8 -*-
from zope import schema
from zope.interface import Interface
from vindula.controlpanel import MessageFactory as _
from vindula.controlpanel.vocabularies import ListDisplayAlerts
from plone.app.textfield import RichText

# Interface and schema
class IAlertDisplay(Interface):
    """ Vindula  Alert Display """
    
    activ_display = schema.Bool(title=_(u'label_activ_comment', default=u'Ativar Mensagem de Alerta'),
                                description=_(u'help_activ_comment', default=u'Se selecionado, Ativa a visualização da mensagem em todo o portal'),
                                default=False)
    
    type_messenger = schema.Choice(title=_(u"Tipo da mensagem"),
                                   description=_(u"Selecione uma opção de visualização de mensagem."),
                                   source=ListDisplayAlerts(),
                                   required=True)
    
    title_messenger = schema.TextLine(title=_(u"Titulo da mensagem"),
                                     description=_(u"Digite o titulo que será mostrado na caixa destaque do alerta do portal"),
                                     required=True)
    
    text_messenger = RichText(title=_(u"Texto da mensagem"),
                                     description=_(u"Digite o texto que será mostrado no alerta do portal"),
                                     required=False)

    
                          
        