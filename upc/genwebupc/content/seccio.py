# -*- coding: utf-8 -*-
from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

#from Products.Archetypes.public import DisplayList

from upc.genwebupc.interfaces import ISeccio
from AccessControl import ClassSecurityInfo

from upc.genwebupc.config import PROJECTNAME
from upc.genwebupc import GenwebMessageFactory as _

from Products.ATContentTypes.content.document import ATDocument
from Products.ATContentTypes.content.document import ATDocumentSchema

schema = atapi.Schema((


),
)

Seccio_Schema = ATDocumentSchema.copy() + \
    schema.copy()

finalizeATCTSchema(Seccio_Schema, folderish=True, moveDiscussion=False)

class Seccio(ATDocument):
    """
    """
    security = ClassSecurityInfo()
    implements(ISeccio)

    meta_type = 'Seccio'
    _at_rename_after_creation = True

    schema = Seccio_Schema 

atapi.registerType(Seccio, PROJECTNAME)




