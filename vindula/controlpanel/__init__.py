from zope.i18nmessageid import MessageFactory

# Set up the i18n message factory for our package
MessageFactory = MessageFactory('vindula.controlpanel')


from plone.app.relationfield.widget import RelationListDataManager
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from z3c.relationfield.relation import RelationValue

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