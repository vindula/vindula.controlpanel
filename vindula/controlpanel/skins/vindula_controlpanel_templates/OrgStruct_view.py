# -*- coding: utf-8 -*-
def getOrgStru(ctx):
    while ctx.portal_type != 'OrganizationalStructure' and\
      ctx.portal_type != 'Plone Site':
        ctx = ctx.aq_parent
    
    return ctx

ctx = getOrgStru(context)
if ctx.portal_type != 'Plone Site':
    if not ctx.activ_personalit:
        ctx = getOrgStru(ctx.aq_parent)

return ctx