##bind context=context
##parameters= layout=True
# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName

def getOrgStru(ctx,layout):
    portal = getToolByName(ctx, 'portal_url').getPortalObject()

    if ctx != portal and ctx.portal_type != 'OrganizationalStructure':
        try:
            return getOrgStru(ctx.aq_parent,layout)
        except:
            pass

    elif ctx.portal_type == 'OrganizationalStructure':
        if layout:
            if ctx.activ_personalit:
                return ctx
            else:
                try:
                    return getOrgStru(ctx.aq_parent,layout)
                except:
                    pass
        else:
            return ctx
    
    return ctx

return getOrgStru(context,layout)