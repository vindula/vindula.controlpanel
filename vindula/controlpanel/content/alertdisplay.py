# -*- coding: utf-8 -*-
from zope import schema
from zope.interface import Interface
from vindula.controlpanel import MessageFactory as _
from vindula.controlpanel.vocabularies import ListDisplayAlerts
from plone.app.textfield import RichText

# Interface and schema
class IAlertDisplay(Interface):
    """ Vindula  Alert Display """
    
    activ_display = schema.Bool(title=_(u'label_activ_comment', default=u'Ativar Menssagem de Alerta'),
                                description=_(u'help_activ_comment', default=u'Se selecionado, ativa a visualização da mensagem em todo o portal'),
                                default=False)
    
    type_messenger = schema.Choice(title=_(u"Tipo da menssagem"),
                                   description=_(u"Selecione uma opção de visualização de menssagem."),
                                   source=ListDisplayAlerts(),
                                   required=True)
    
    title_messenger = schema.TextLine(title=_(u"Título da menssagem"),
                                     description=_(u"Digite o título que será mostrado na caixa destaque do alerta do portal"),
                                     required=True)
    
    text_messenger = RichText(title=_(u"Texto da menssagem"),
                                     description=_(u"Digite o texto que sera mostrado no alerta do portal"),
                                     required=False)

    
                          
        