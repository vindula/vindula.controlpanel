# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName

def installControlPanel(context):    
    portal = context.getSite()
    portal_workflow = getToolByName(portal, 'portal_workflow')

    # Creating Control Panel Folder
    if not 'control-panel-objects' in portal.objectIds():
        portal.invokeFactory('Folder', 
                              id='control-panel-objects', 
                              title='Control Panel Objects',
                              description='Pasta que guarda os objetos de configuração do Vindula.',
                              excludeFromNav = True)
        
    folder = portal['control-panel-objects']
    

    # Creating Control Panel Objects
    
    types = ['vindula.controlpanel.content.categories', 
             'vindula.controlpanel.content.themeconfig']
        
    for type in types:
        if portal.portal_types.get(type):
            id = 'vindula_' + type.split('.')[3]
            if not id in folder.objectIds():
                folder.setConstrainTypesMode(0)
                portal.portal_types.get(type).global_allow = True        
                folder.invokeFactory(type, id=id, excludeFromNav=True)
                print 'Create %s object.' % id          
                portal.portal_types.get(type).global_allow = False