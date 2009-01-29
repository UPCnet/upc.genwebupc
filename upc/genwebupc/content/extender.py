from zope.component import adapts
from zope.interface import implements
from Products.Poi.interfaces import IIssue 
from Products.Archetypes.atapi import StringField
from archetypes.schemaextender.interfaces import ISchemaModifier
from Products.Collage.interfaces import ICollageAlias


class CollageSchemaModifier(object):
    """ Modifico el schema del Collage link
    """
    implements(ISchemaModifier)
    adapts(ICollageAlias)

    def __init__(self, context):
        self.context = context
   
    def fiddle(self, schema):
        #import pdb; pdb.set_trace()
        schema['target'].keepReferencesOnCopy = True



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


