from five import grok

from vindula.myvindula import MessageFactory as _


from plone.app.layout.navigation.interfaces import INavigationRoot




class ControlPanelView(grok.View):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('vindula-control-panel')
    
    