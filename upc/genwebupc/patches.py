#########################################
# Scripts d'un sol ús per usar via debug
#########################################
#
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from OFS.interfaces import IFolder
from Products.LDAPUserFolder.LDAPUserFolder import LDAPUserFolder
import logging
logger = logging.getLogger('upc.genwebupc')

def listPloneSites(context):
    out = []
    for item in context.values():
        if IPloneSiteRoot.providedBy(item):
            out.append(item)
        if IFolder.providedBy(item):
            for site in item.values():
                if IPloneSiteRoot.providedBy(site):
                    out.append(site)
    return out

def addLDAPServer(portal):
    LDAPUserFolder.manage_addServer(portal.acl_users.ldapUPC.acl_users, "ldap.upc.edu", '636', use_ssl=1)
    logger.info("Successfully installed LDAP server in %s" % portal.id)

def changeLDAPservers(app):
    sites = listPloneSites(app)
    for site in sites:
        addLDAPServer(site)
#
##########################################
# /Scripts d'un sol ús per usar via debug
#########################################


# Aquesta part queda Superseeded pel paquet upc.genweb.patches!!!!!!!
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

# Patching del ATContentypes/content/File.py Class ATFile
# Required per tal de poder veure flash en condicions
from Products.ATContentTypes.content.file import ATFile

inlineMimetypes= ('application/msword',
                      'application/x-msexcel', # ?
                      'application/vnd.ms-excel',
                      'application/vnd.ms-powerpoint',
                      'application/x-shockwave-flash',
                      'application/pdf')

ATFile.inlineMimetypes = inlineMimetypes


# Patching per que no salti el modified quan es crea un blob
from plone.app.contentrules import handlers
from Products.Archetypes.interfaces import IObjectInitializedEvent
from Acquisition import aq_inner, aq_parent

def modified(event):
    """When an object is modified, execute rules assigned to its parent
    """

    if handlers.is_portal_factory(event.object):
        return

    if hasattr(event.object,'getId'):
        if event.object.getId().split('.')[0]=='file':
            return

    # Let the special handler take care of IObjectInitializedEvent
    if not IObjectInitializedEvent.providedBy(event):
        handlers.execute(aq_parent(aq_inner(event.object)), event)

handlers.modified = modified



# Patching del Blob a GW3
# Required per tal de poder veure flash en condicions 
from plone.app.blob.content import ATBlob

def new_index_html(self, REQUEST, RESPONSE):
    """ download the file inline """
    field = self.getPrimaryField()
    if field.getContentType(self) in ATFile.inlineMimetypes:
         # return the PDF and Office file formats inline
        return field.index_html(self, REQUEST, RESPONSE)
    return field.download(self, REQUEST, RESPONSE)

ATBlob.index_html = new_index_html

