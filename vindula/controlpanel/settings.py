# -*- coding: utf-8 -*-
"""
    Define add-on settings.
"""

from zope.interface import Interface
from zope import schema
from vindula.controlpanel import MessageFactory as _

from plone.z3cform import layout
from plone.directives import form
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper

class ISettings(Interface):
    """ Define settings data structure """
    
    timezoneVindula = schema.Int(
            title=_(u"Fuso horário"),
            description=_(u"Fuso horário utilzado no Vindula."),
            required=True,
            default=3
    )
    
class SettingsEditForm(RegistryEditForm):
    """
        Define form logic
    """
    schema = ISettings

SettingsEditView = layout.wrap_form(SettingsEditForm, ControlPanelFormWrapper)
SettingsEditView.label = u"Vindula: Timezone Settings"