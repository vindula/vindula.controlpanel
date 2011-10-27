# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName

def installControlPanel(context):    
    portal = context.getSite()
    portal_workflow = getToolByName(portal, 'portal_workflow')
    type = 'vindula.controlpanel.content.themeconfig'
    
    if portal.portal_types.get(type):
        if not 'vindula_themeconfig' in portal.objectIds():
            portal.portal_types.get(type).global_allow = True              
            portal.invokeFactory(type, 
                                 id='vindula_themeconfig', 
                                 excludeFromNav = True)
            print 'Create vindula_themeconfig object.'
            portal.portal_types.get(type).global_allow = False