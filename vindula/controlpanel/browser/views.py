# -*- coding: utf-8 -*-
from five import grok
from plone.app.layout.navigation.interfaces import INavigationRoot


class ControlPanelView(grok.View):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('vindula-control-panel')