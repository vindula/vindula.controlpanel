# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName

def installControlPanel(context):    
    portal = context.getSite()

    # Set Global Allow False
    portal.portal_types.get('News Item').global_allow = False
    portal.portal_types.get('Folder').global_allow = False
    portal.portal_types.get('Document').global_allow = False
    portal.portal_types.get('Link').global_allow = False

    # Creating Control Panel Objects
    cpanel_objects = portal.get('control-panel-objects', None)
    cpanel_objects_old = portal.get('control-panel-objects-old', None)

    copy_objs = None
    if not cpanel_objects or cpanel_objects.portal_type != 'ObjectsControlPanel':
        if cpanel_objects and cpanel_objects.portal_type != 'ObjectsControlPanel':
            portal.portal_types.get('Folder').global_allow = True
            portal.manage_renameObject(cpanel_objects.getId(), cpanel_objects.getId() + "-old")
            portal.portal_types.get('Folder').global_allow = False
        try:
            portal.portal_types.get('ObjectsControlPanel').global_allow = True
            portal.invokeFactory('ObjectsControlPanel', 
                                  id='control-panel-objects', 
                                  title='Control Panel Objects',
                                  description='Pasta que guarda os objetos de configuração do Vindula.',
                                  excludeFromNav = True)
            
            if cpanel_objects_old:
                copy_objs = portal[cpanel_objects_old.getId()].manage_copyObjects(portal[cpanel_objects_old.getId()].objectIds())
            cpanel_objects = portal['control-panel-objects']
            if copy_objs:
                cpanel_objects.manage_pasteObjects(copy_objs)
                portal.portal_types.get('Folder').global_allow = True
                portal.manage_delObjects([cpanel_objects_old.getId()])
                portal.portal_types.get('Folder').global_allow = False
            portal.portal_types.get('ObjectsControlPanel').global_allow = False
        except:
            print 'Erro criando ObjectsControlPanel'
        
    if cpanel_objects:
        # Creating Control Panel Objects
        types = ['vindula.controlpanel.content.alertdisplay',
                 'vindula.controlpanel.content.vindulaconfigall',
                 'vindula.controlpanel.content.aniversariantesconfig',
                 'VindulaCategories','ThemeConfig','ContentRedirectUser',
                 'ThemeLoginConfig','ContainerTopicsControlPanel','UpdateUser']
        
        if cpanel_objects.get('vindula_categories', None):
            categories_old = cpanel_objects.get('vindula_categories')
            
            new_object = {}
            new_object['id'] = 'VindulaCategories'
            new_object['title'] = 'vindula_categories'
            new_object['orgstructure'] = categories_old.orgstructure
            new_object['list_macros'] = categories_old.list_macros
#            try:
#                new_object['order_list'] = tuple(categories_old.order_list)
#            except:
#                pass
            try:
                new_object['folder_image'] = categories_old.folder_image
            except:
                pass
            try:
                new_object['orgaoEdital'] = categories_old.orgaoEdital
            except:
                pass
            try:
                new_object['modalidadeEdital'] = categories_old.modalidadeEdital
            except:
                pass
            new_object['excludeFromNav'] = True
            
            try:
                categories_new = cpanel_objects.invokeFactory('VindulaCategories', 
                                                               **new_object)
                cpanel_objects.manage_renameObject(categories_old.getId(), categories_old.getId() + "-old")
                cpanel_objects.manage_renameObject(categories_new, 'vindula_categories')
            except:
                pass
        
        for type in types:
            if portal.portal_types.get(type):
                if len(type.split('.')) >= 3:
                    id = 'vindula_' + type.split('.')[3]
                else:
                    id = type
                    
                if not id in cpanel_objects.objectIds():
                    cpanel_objects.setConstrainTypesMode(0)
                    portal.portal_types.get(type).global_allow = True        
                    cpanel_objects.invokeFactory(type, id=id, excludeFromNav=True)
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
        portal.portal_types.get('Folder').global_allow = True
        
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
        
        portal.portal_types.get('Folder').global_allow = False
        
def updateTopicsControlPanel(context):
    portal = context.getSite()
    control_panel = getToolByName(portal, 'portal_controlpanel')
    groups = control_panel.getGroups('site')
    ##
    #CODIGO COMENTADO PARA NAO GERAR SEMPRE OS CONTEUDOS DO CONTROL PANEL
    ##
#    try:
#        folder_topics = portal.get('control-panel-objects').get('ContainerTopicsControlPanel')
#    except:
#        folder_topics = None
#    
#    if folder_topics:
#        try:
#            for group in groups:
#                products = control_panel.enumConfiglets(group=group['id'])
#                id_topic = 'topic_%s' % group['id']
#                if not folder_topics.get(id_topic):
#                    folder_topics.invokeFactory('TopicControlPanel', id=id_topic, title=group['title'], usersOrGroupsTopic=['admin'], excludeFromNav=True)
#                for product in products:
#                    topic = folder_topics.get(id_topic)
#                    id_prod = 'subtopic_%s' % product['id']
#                    if not topic.get(id_prod):
#                        topic.invokeFactory('SubtopicControlPanel',
#                                             id=id_prod,
#                                             title=product['title'],
#                                             description=product['description'],
#                                             viewName=product['url'].replace(portal.portal_url()+'/', ''),
#                                             excludeFromNav=True,
#                                            )
#        except ValueError:
#            pass
#    
#    cp_objects = portal.get('control-panel-objects', None)
#    if cp_objects:
#        cp_objects = cp_objects.objectValues()
#    if cp_objects and folder_topics:
#        id_topic = 'vindula-control-panel'
#        try:
#            if not folder_topics.get(id_topic):
#                folder_topics.invokeFactory('TopicControlPanel', id=id_topic, title='Vindula Control Panel', usersOrGroupsTopic=['admin'], excludeFromNav=True)
#            for object in cp_objects:
#                topic = folder_topics.get(id_topic)
#                id_prod = 'subtopic_%s' % object.id
#                if not topic.get(id_prod):
#                    topic.invokeFactory('SubtopicControlPanel',
#                                         id=id_prod,
#                                         title=object.id,
#                                         description=object.Description(),
#                                         viewName=object.absolute_url().replace(portal.portal_url()+'/', ''),
#                                         excludeFromNav=True,
#                                         useAjaxMode = True,
#                                        )
#        except ValueError:
#            pass
    
        
def installTheme(context): 
    portal = context.getSite()
    portal_workflow = getToolByName(portal, 'portal_workflow')
    
    
    if not 'links' in portal.objectIds():
        portal.portal_types.get('Folder').global_allow = True
        portal.invokeFactory('Folder', 
                              id='links', 
                              title='Links Úteis',
                              excludeFromNav = True)
        
        pasta = portal['links']
        pasta.setConstrainTypesMode(1)
        pasta.setLocallyAllowedTypes(('Link',))
        
        try:portal_workflow.doActionFor(pasta, 'publish')
        except:portal_workflow.doActionFor(pasta, 'publish_internally')              
        
        portal.portal_types.get('Folder').global_allow = False          
        
        
def installSteps(context):
    portal = context.getSite()

    if 'control-panel-objects' in portal.objectIds():
        control = portal['control-panel-objects']
        
        if 'vindula_wizard' in control.objectIds():
            wizard = control['vindula_wizard']
            
            passos = [{'id':'theme',
                       'url':'/control-panel-objects/vindula_themeconfig/edit',
                       'title':'Layout Portal',
                       'description':'Editar o layout do portal vindula',
                       'status':True
                       },
                      {'id':'categories',
                       'url':'/control-panel-objects/vindula_categories/edit',
                       'title':'Categorias',
                       'description':'Editar as categorias do portal vindula',
                       'status':True
                       },
                      {'id':'company',
                       'url':'/vindula-company-information',
                       'title':'Informações da empresa',
                       'description':'Editar as informações impresariais',
                       'status':True
                       },
                      {'id':'users',
                       'url':'/@@usergroup-userprefs',
                       'title':'Usuários e Grupos',
                       'description':'Editar as informações dos usuários',
                       'status':True
                       }]
            
            for passo in passos:
                if not passo.get('id') in wizard.objectIds():
                    wizard.invokeFactory('Steps',**passo)