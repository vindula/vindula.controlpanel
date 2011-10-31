# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName

def installControlPanel(context):    
    portal = context.getSite()
    portal_workflow = getToolByName(portal, 'portal_workflow')
    type_theme = 'vindula.controlpanel.content.themeconfig'
    type_categories = 'vindula.controlpanel.content.categories'
    
    if portal.portal_types.get(type_theme):
        if not 'vindula_themeconfig' in portal.objectIds():
            portal.portal_types.get(type_theme).global_allow = True              
            portal.invokeFactory(type_theme, 
                                 id='vindula_themeconfig', 
                                 excludeFromNav = True)
            print 'Create vindula_themeconfig object.'
            portal.portal_types.get(type_theme).global_allow = False
    
    
    if portal.portal_types.get(type_categories):
        if not 'vindula_categories' in portal.objectIds():
            portal.portal_types.get(type_categories).global_allow = True              
            portal.invokeFactory(type_categories, 
                                 id='vindula_categories', 
                                 excludeFromNav = True)
            print 'Create vindula_categories object.'
            portal.portal_types.get(type_categories).global_allow = False