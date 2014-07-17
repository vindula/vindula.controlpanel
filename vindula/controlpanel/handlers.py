 #-*- coding: utf-8 -*-
from zope.component import getUtility
from Products.CMFCore.utils import getToolByName

from zope.app.component.hooks import getSite
from Products.CMFCore.interfaces import ISiteRoot

from vindula.myvindula.models.user_session_token import UserSessionToken

import logging

def to_utf8(value):
    return unicode(value, 'utf-8') 

logger = logging.getLogger('vindula.content')


def userLogged(event, isLogin=True):
    """ Handler for User Login in Site """
    acl_user = getToolByName(getSite(), 'acl_users')
    groups_tool = getToolByName(getSite(), "portal_groups")
    membership = getSite().portal_membership
    check_redirect = getSite().restrictedTraverse('@@myvindula-conf-login').check_redirect()
    
    try: rules = getSite()['control-panel-objects']['ContentRedirectUser']
    except: relues = None
    request = getSite().REQUEST  

    if request.other.get('came_from') not in ('myvindula-first-registre', getSite().portal_url()+'/', '', None):
        request.response.redirect(request.other.get('came_from'), lock=True)
        return
    
    elif rules and not 'myvindula-first-registre' in request.other.get('came_from','') and check_redirect:
        user_login = membership.getAuthenticatedMember()
        groups_user = [i.id for i in groups_tool.getGroupsByUserId(user_login.getUserName())]
        
        for rule in rules.objectValues():
            if checaEstado(rule):
                if user_login.id in rule.getUserORgroups():
                    url = rule.getRedirectPath().absolute_url()
                    
                    request.other["came_from"]= url
                    request.response.redirect(url, lock=True)
                    return
                else:
                    for group in groups_user:
                        if group in rule.getUserORgroups():
                            url = rule.getRedirectPath().absolute_url()
                            
                            request.other["came_from"]=url
                            request.response.redirect(url, lock=True)
                            return
        
        url = getSite().portal_url()
        request.other["came_from"]=url
        request.response.redirect(url, lock=True)
        
    elif not isLogin:
        url = getSite().absolute_url()
        request.other["came_from"]=url
        request.response.redirect(url, lock=True)
        
def userLoggedOut(event):
    """ A user logged out. """
    portal_object = getSite()
    membership = getSite().portal_membership
    
    if not membership.isAnonymousUser():
        user_login = membership.getAuthenticatedMember()
        
        if user_login:
            username = user_login.getUserName()
            if isinstance(username, str):
                username = username.decode('utf-8')
            datas = UserSessionToken().store.find(UserSessionToken,
                                                  UserSessionToken.username==username,
                                                  UserSessionToken.deleted==False).order_by(UserSessionToken.date_created)
            
            for data in datas:
                data.invalidateToken()
                                            
def checaEstado(obj):
        states = ['published','internal']
        pw = getSite().portal_workflow
        if pw.getInfoFor(obj,'review_state') in states:
            return True
        else:
            return False