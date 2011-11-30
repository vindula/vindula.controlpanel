# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName

def installControlPanel(context):    
    portal = context.getSite()
    portal_workflow = getToolByName(portal, 'portal_workflow')


    # Set Global Allow False
     
    portal.portal_types.get('News Item').global_allow = False
        

    # Creating Control Panel Folder
    
    if not 'control-panel-objects' in portal.objectIds():
        portal.invokeFactory('Folder', 
                              id='control-panel-objects', 
                              title='Control Panel Objects',
                              description='Pasta que guarda os objetos de configuração do Vindula.',
                              excludeFromNav = True)
        
    folder_control_panel = portal['control-panel-objects']
    
    
    # Creating Banco de Imagens Folder

    if not 'banco-de-imagens' in portal.objectIds():
        portal.invokeFactory('Folder', 
                              id='banco-de-imagens',
                              title='Banco de Imagens',
                              description='Pasta que guarda todas as imagens do portal.',
                              excludeFromNav = True)
        
        folder_images_data = portal['banco-de-imagens']
        folder_images_data.setConstrainTypesMode(1)
        folder_images_data.setLocallyAllowedTypes(('Image', 'Folder'))
        portal_workflow.doActionFor(folder_images_data, 'publish')
    

    # Creating Control Panel Objects
    
    types = ['vindula.controlpanel.content.categories', 
             'vindula.controlpanel.content.themeconfig',
             'vindula.controlpanel.content.vindulanewsconfig',
             'vindula.controlpanel.content.vindularecadosconfig']
        
    for type in types:
        if portal.portal_types.get(type):
            id = 'vindula_' + type.split('.')[3]
            if not id in folder_control_panel.objectIds():
                folder_control_panel.setConstrainTypesMode(0)
                portal.portal_types.get(type).global_allow = True        
                folder_control_panel.invokeFactory(type, id=id, excludeFromNav=True)
                print 'Create %s object.' % id          
                portal.portal_types.get(type).global_allow = False