# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName

def installControlPanel(context):    
    portal = context.getSite()

    # Set Global Allow False
    portal.portal_types.get('News Item').global_allow = False
    portal.portal_types.get('Folder').global_allow = False

    # Creating Control Panel Folder
    if not 'control-panel-objects' in portal.objectIds():
        portal.invokeFactory('Folder', 
                              id='control-panel-objects', 
                              title='Control Panel Objects',
                              description='Pasta que guarda os objetos de configuração do Vindula.',
                              excludeFromNav = True)
        
    folder_control_panel = portal['control-panel-objects']

    # Creating Control Panel Objects
    types = ['vindula.controlpanel.content.categories', 
             'vindula.controlpanel.content.alertdisplay',
             'vindula.controlpanel.content.vindulaconfigall',
             'vindula.controlpanel.content.aniversariantesconfig',
             'ThemeConfig','ContentRedirectUser', 'ThemeLoginConfig']
    
        
    for type in types:
        if portal.portal_types.get(type):
            if len(type.split('.')) >= 3:
                id = 'vindula_' + type.split('.')[3]
            else:
                id = type
                
            if not id in folder_control_panel.objectIds():
                folder_control_panel.setConstrainTypesMode(0)
                portal.portal_types.get(type).global_allow = True        
                folder_control_panel.invokeFactory(type, id=id, excludeFromNav=True)
                print 'Create %s object.' % id
                portal.portal_types.get(type).global_allow = False

    

def link_user_folder(context):
    ctx = context.getSite()
    portal = context.getSite()
    portal_workflow = getToolByName(portal, 'portal_workflow')
    
    # Creating Migration Users Folder
    if 'control-panel-objects' in ctx.objectIds():
        portal.portal_types.get('Folder').global_allow = True
        folder_control_panel = ctx['control-panel-objects']
        folders = [{'id':'link-user-folder',
                    'title':'Links da Barra Pessoal',
                    'description':'Pasta que guardar os links adicionais aos usuários.',
                    'AllowedTypes':('InternalLink',)},
                   {'id':'fieldset-myvindula',
                    'title':'Categorias para o perfil dos usuários',
                    'description':'Patas que guardar as categorias adicionais do perfil dos usuários',
                    'AllowedTypes':('FieldSetMyvindula',)}
                   ]
        
        for folder in folders:
            if not folder['id'] in folder_control_panel.objectIds():
                folder_control_panel.invokeFactory('Folder', 
                                                   id=folder['id'], 
                                                   title=folder['title'],
                                                   description=folder['description'],
                                                   excludeFromNav = True)
                                
                folder_data = folder_control_panel[folder['id']]
                folder_data.setConstrainTypesMode(1)
                folder_data.setLocallyAllowedTypes(folder['AllowedTypes'])
                
                try:portal_workflow.doActionFor(folder_data, 'publish')
                except:portal_workflow.doActionFor(folder_data, 'publish_internally')                

        portal.portal_types.get('Folder').global_allow = False

def CreateForderImage(context):
    portal = context.getSite()
    portal_workflow = getToolByName(portal, 'portal_workflow')

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
        
        try:portal_workflow.doActionFor(folder_images_data, 'publish')
        except:portal_workflow.doActionFor(folder_images_data, 'publish_internally')
        
        
def installTheme(context):    
    portal = context.getSite()
    portal_workflow = getToolByName(portal, 'portal_workflow')
    
    if not 'links' in portal.objectIds():
        portal.invokeFactory('Folder', 
                              id='links', 
                              title='Links Úteis',
                              excludeFromNav = True)
        
        pasta = portal['links']
        pasta.setConstrainTypesMode(1)
        pasta.setLocallyAllowedTypes(('Link',))
        
        try:portal_workflow.doActionFor(pasta, 'publish')
        except:portal_workflow.doActionFor(pasta, 'publish_internally')                        