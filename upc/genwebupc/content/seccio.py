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
from Products.Archetypes.atapi import AnnotationStorage
from Products.ATContentTypes.configuration import zconf

schema = atapi.Schema((
    atapi.TextField('text',
              required=False,
              searchable=True,
              primary=True,
              storage = AnnotationStorage(migrate=True),
              validators = ('isTidyHtmlWithCleanup',),
              #validators = ('isTidyHtml',),
              default_output_type = 'text/x-html-safe',
              widget = atapi.RichWidget(
                        description = _(u'descripcio_text_seccio', default=u'Descripcio'),
                        label = _(u'label_text_seccio', default=u'Body Text'),
                        rows = 8,
                        allow_file_upload = zconf.ATDocument.allow_document_upload),
    ),
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




