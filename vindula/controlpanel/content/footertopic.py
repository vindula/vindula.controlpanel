# -*- coding: utf-8 -*-
from vindula.controlpanel import MessageFactory as _

from AccessControl import ClassSecurityInfo
from zope.interface import Interface

from Products.ATContentTypes.content.folder import ATFolder
from vindula.controlpanel.content.interfaces import IFooterTopic

from zope.interface import implements
from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from vindula.controlpanel.config import *


# Interface and schema
FooterTopic_schema =  ATFolder.schema.copy() + Schema((


))
finalizeATCTSchema(FooterTopic_schema, folderish=True)

class FooterTopic(ATFolder):
    """ FooterTopic """

    security = ClassSecurityInfo()
    implements(IFooterTopic)
    portal_type = 'FooterTopic'
    _at_rename_after_creation = True
    schema = FooterTopic_schema

registerType(FooterTopic, PROJECTNAME)