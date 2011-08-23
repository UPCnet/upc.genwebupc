from zope.component import adapts
from zope.interface import implements
#from Products.Poi.interfaces import IIssue 

from Products.Archetypes.atapi import BooleanField
from Products.Archetypes.atapi import StringField
from Products.Archetypes.atapi import BooleanWidget

from archetypes.schemaextender.interfaces import ISchemaModifier
#from Products.Collage.interfaces import ICollageAlias
from Products.ATContentTypes.interface.link import IATLink

from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender

# GW4 nevera
#class CollageSchemaModifier(object):
#    """ Modifico el schema del Collage link
#    """
#    implements(ISchemaModifier)
#    adapts(ICollageAlias)
#
#    def __init__(self, context):
#        self.context = context
#   
#    def fiddle(self, schema):
#        #import pdb; pdb.set_trace()
#        schema['target'].keepReferencesOnCopy = True
#
#
#
#class PoiIssueSchemaModifier(object):
#    """Modifico el schema del PoiIssue
#    """
#    implements(ISchemaModifier)
#    adapts(IIssue)
#    
#    def __init__(self, context):
#        self.context = context
#    
#    def fiddle(self, schema):
#        schema['details'].widget.rows = 15
#        schema['steps'].widget.rows = 6


# Any field you tack on must have ExtensionField as its first subclass:
class _StringExtensionField(ExtensionField, BooleanField):
    pass


class ATLinkSchemaModifier(object):
    """Afegeix un check nou al contingut enllas"""
    adapts(IATLink)
    implements(IOrderableSchemaExtender)

    _fields = [
            _StringExtensionField('obrirfinestra',
                required=False,
                searchable=True,
                widget=BooleanWidget(
                       label='Open in a new window',
                       label_msgid='upc.genweb.banners_label_Obrirennovafinestra',
                       i18n_domain='upc.genweb.banners',
                )
            )
        ]

    def __init__(self, newsItem):
        pass

    def getFields(self):
        return self._fields

    def getOrder(self, original):
        new = original.copy()  # contract requires us to make a new one
        defaultSchemaFields = new['default']  # fields from the "default" schemata
        defaultSchemaFields.remove('obrirfinestra')
        defaultSchemaFields.insert(defaultSchemaFields.index('remoteUrl') + 1,
                                   'obrirfinestra')  # stick "channel" after "description"
        return new
