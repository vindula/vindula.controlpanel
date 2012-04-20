from zope.i18nmessageid import MessageFactory

# Set up the i18n message factory for our package
MessageFactory = MessageFactory('vindula.controlpanel')

import logging
logger = logging.getLogger('vindula.controlpanel')
logger.info('Installing Product')

import os, os.path
from App.Common import package_home
from Products.CMFCore import utils as cmfutils

try: # New CMF
    from Products.CMFCore import permissions as CMFCorePermissions 
except: # Old CMF
    from Products.CMFCore import CMFCorePermissions

from Products.CMFCore import DirectoryView
from Products.CMFPlone.utils import ToolInit
from Products.Archetypes.atapi import *
from Products.Archetypes import listTypes
from Products.Archetypes.utils import capitalize
from config import *
    
from plone.app.relationfield.widget import RelationListDataManager
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from z3c.relationfield.relation import RelationValue

def initialize(context):
    import content

    # Initialize portal content
    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)

    cmfutils.ContentInit(
        PROJECTNAME + ' Content',
        content_types      = content_types,
        permission         = DEFAULT_ADD_CONTENT_PERMISSION,
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)
        
def set(self, value):
    """
    Sets the relationship target. Monkeypatches issues in original
    RelationListDataManager where manager assumes that every object has
    intid.
    """
    value = value or []
    new_relationships = []
    intids = getUtility(IIntIds)
    for item in value:
        try:
            to_id = intids.getId(item)
        except KeyError:
            to_id = intids.register(item)
        new_relationships.append(RelationValue(to_id))
    super(RelationListDataManager, self).set(new_relationships)

print "applying monkeypatch"
RelationListDataManager.set = set
 