# -*- coding: utf-8 -*-
from five import grok
from zope.interface import Interface
from plone.app.layout.navigation.interfaces import INavigationRoot
from vindula.myvindula.user import BaseFunc
from vindula.controlpanel.browser.models import RegistrationCompanyInformation


class ControlPanelView(grok.View):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('vindula-control-panel')
    
    
class MacroLogoTopView(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('vindula-macro-logotop')
    
    
class MacroFooterView(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('vindula-macro-footer')
    
class CompanyInformation(grok.View, BaseFunc):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('vindula-company-information')
    
    def load_from(self):
        return RegistrationCompanyInformation().registration_processes(self)
    