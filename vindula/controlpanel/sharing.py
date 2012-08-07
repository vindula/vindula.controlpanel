from zope.interface import implements
from plone.app.workflow.interfaces import ISharingPageRole
from Products.CMFCore import permissions as core_permissions

from vindula.controlpanel import MessageFactory as _

class EditPortletRole(object):
    implements(ISharingPageRole)
    
    title = _(u"title_editPortlet", default=u"Editar Portlet")
    required_permission = core_permissions.ManagePortal
