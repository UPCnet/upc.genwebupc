# Parchejem el Poi
from Products.Poi import config

config.ISSUE_MIME_TYPES = ('text/x-web-intelligent', 'text/html')
config.DEFAULT_ISSUE_MIME_TYPE = 'text/html'

# Parchejem el Survey
from Products.PloneSurvey import config as configSurvey
from Products.Archetypes.utils import DisplayList

configSurvey.SELECT_INPUT_TYPE = DisplayList((
    ('radio', 'Radio Buttons', 'label_radio_buttons'),
    ('checkbox', 'Check Boxes', 'label_check_boxes'),
    ))

# Parchejat tambe el GenericSetup en en upc.genwebupctheme/upc/genwebupctheme/__init__.py
from Products.Collage.content._alias import CollageAlias
from Products.ATContentTypes.content.base import ATCTContent
from Products.Archetypes import atapi
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.Collage.utilities import CollageMessageFactory as _

CollageAliasSchema = ATCTContent.schema.copy() + atapi.Schema((
    atapi.ReferenceField(
        name='target',
        mutator='set_target',
        accessor='get_target',
        relationship='Collage_aliasedItem',
        multiValued = 0,
        allowed_types = (),
        keepReferencesOnCopy = True,
        widget=ReferenceBrowserWidget(
            label=_(u'label_alias_target', default="Selected target object"),
            startup_directory='/',
        ),
    ),
))

CollageAlias.schema = CollageAliasSchema

# Parchejat tambe el GenericSetup en en upc.genwebupctheme/upc/genwebupctheme/__init__.py
