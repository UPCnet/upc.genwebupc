from zope.component import adapts
from zope.interface import implements
from Products.Poi.interfaces import IIssue 
from Products.Archetypes.atapi import StringField
from archetypes.schemaextender.interfaces import ISchemaModifier

class PoiIssueSchemaModifier(object):
    """Modifico el schema del PoiIssue
    """
    implements(ISchemaModifier)
    adapts(IIssue)
    
    def __init__(self, context):
        self.context = context
    
    def fiddle(self, schema):
        schema['details'].widget.rows = 15
        schema['steps'].widget.rows = 6


