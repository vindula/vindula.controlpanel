# -*- coding: utf-8 -*-
from zope import schema
from plone.directives import form
from five import grok
from vindula.controlpanel import MessageFactory as _

from zope.interface import Interface
from zope.app.component.hooks import getSite

from zope.interface import invariant, Invalid
# Interface and schema

class StartBeforeEnd(Invalid):
    __doc__ = _(u"The start or end date is invalid")

class IVindulaConfigLogin(form.Schema):
    """ Vindula Config Login"""
    
    ativa_redirect = schema.Bool(
                title=_(u'label_ativa_redirect', default=u'Ativar a função de redirecionar'),
                description=_(u'help_activ_holerite', default=u'Se selecionado ativa a função de redirecionamento dos usuário'),
                default=True
                )
    
    ativa_loginClassico = schema.Bool(
                title=_(u'label_ativa_loginClassico', default=u'Ativar o login classico do portal vindula'),
                description=_(u'help_ativa_loginClassico', default=u'Se selecionado ativa a tela classica de login para os usuários'),
                default=False
                )
    
    ativa_loginGrafico = schema.Bool(
                title=_(u'label_ativa_loginGrafico', default=u'Ativar o login grafico do portal vindula'),
                description=_(u'help_ativa_loginGrafico', default=u'Se selecionado ativa a tela grafica de login para os usuários'),
                default=True
                )
    
    @invariant
    def validateStartEnd(data):
        if not data.ativa_loginClassico and not data.ativa_loginGrafico:
            raise StartBeforeEnd(_(u"Selecione pelo menos uma opção de login"))
        elif data.ativa_loginClassico and data.ativa_loginGrafico:
            raise StartBeforeEnd(_(u"Selecione so mente uma opção de login"))
    


class VindulaConfigLogin(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('myvindula-conf-login')    


    def render(self):
        pass
    
    def configurador(self):
        if 'control-panel-objects' in  getSite().keys():
            control = getSite()['control-panel-objects']
            if 'vindula_vindulaconfiglogin' in control.keys():
                return control['vindula_vindulaconfiglogin']
            else:
                return False
        else:
            return False
    
    def check_redirect(self):
        if self.configurador():
            control = self.configurador()
            return control.ativa_redirect
        else:
            return True
        