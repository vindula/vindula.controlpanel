# -*- coding: utf-8 -*-
def getOrgStru(ctx):
    if ctx.portal_type != 'Plone Site' and ctx.portal_type != 'OrganizationalStructure':
        return getOrgStru(ctx.aq_parent)
    elif ctx.portal_type == 'OrganizationalStructure':
        if ctx.activ_personalit:
            return ctx
        else:
            return getOrgStru(ctx.aq_parent)
    
    return ctx

return getOrgStru(context)