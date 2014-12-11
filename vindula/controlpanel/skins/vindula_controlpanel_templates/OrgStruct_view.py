##bind context=context
##parameters= layout=True
# -*- coding: utf-8 -*-

def getOrgStru(ctx,layout):
    if ctx.portal_type != 'Plone Site' and ctx.portal_type != 'OrganizationalStructure':
        return getOrgStru(ctx.aq_parent,layout)
    elif ctx.portal_type == 'OrganizationalStructure':
        # if layout:
        #     if ctx.activ_personalit:
        #         return ctx
        #     else:
        #         return getOrgStru(ctx.aq_parent,layout)
        # else:
        #     return ctx
        return ctx
    
    return ctx

return getOrgStru(context,layout)