from Acquisition import aq_inner, aq_parent

from zope.component import getMultiAdapter
from Products.GenericSetup import profile_registry, EXTENSION
from Products.CMFPlone.interfaces import IPloneSiteRoot
from OFS.interfaces import IFolder
from Products.CMFCore.utils import getToolByName

from Products.Five.browser import BrowserView

import logging
import mechanize

def migracio(context):
    """Funcio que realitza la migracio de GW3 a GW4"""
    logger = logging.getLogger('Genweb 4: Migrator')
    logger.warn('Running Migration')

    setup = getToolByName(context, 'portal_setup')
    ir = setup.getImportStepRegistry()
    ir.listSteps()
    logger.warn('%s', ir.listSteps())

    try:
        ir.unregisterStep('upc.genweb.logosfooter.various')
        ir.unregisterStep('cachesettings')
        ir.unregisterStep('meetings-QI-dependencies')
        ir.unregisterStep('meetings-Update-RoleMappings')
        ir.unregisterStep('meetings-postInstall')
        ir.unregisterStep('meetings-GS-dependencies')
        ir.unregisterStep('upc.genweb.banners.various')
        ir.unregisterStep('upc.genweb.descriptorTIC-postInstall')
        logger.warn("[Desregistrar steps de GS invalids] S'han desregistrat tots els steps correctament.")
    except:
        logger.warn("[Desregistrar steps de GS invalids] Alguns dels steps no s'han trobat ja estaven esborrats o no existeixen")

    # Esborro el workflow que fa petar el migrador de Plone, despres ja es tornara a afegir
    pw = getToolByName(context, 'portal_workflow')
    try:
        pw.manage_delObjects('simpleTask_workflow')
        logger.warn("[Esborrar workflow simpleTask] S'ha esborrat el simpleTask_workflow")
    except:
        logger.warn('[Esborrar workflow simpleTask] El simpleTask_workflow ja estava esborrat')

    # Problema amb el SimpleAttachment, treure el 'Large Plone Folder' dels recursos 'linkables'
    kupuTool = getToolByName(context, 'kupu_library_tool', None)
    linkable = list(kupuTool.getPortalTypesForResourceType('linkable'))
    if 'Large Plone Folder' in linkable:
        linkable.remove('Large Plone Folder')
        kupuTool.updateResourceTypes(({'resource_type': 'linkable',
                                       'old_type': 'linkable',
                                       'portal_types': linkable},))

        logger.warn("[Esborrar 'Large Plone Folder'] S'ha esborrat amb exit el tipus 'Large Plone Folder' dels recursos 'linkables' del Kupu")

    if 'Seccio' in linkable:
        linkable.remove('Seccio')
        kupuTool.updateResourceTypes(({'resource_type': 'linkable',
                                       'old_type': 'linkable',
                                       'portal_types': linkable},))

        logger.warn("[Esborrar 'Seccio'] S'ha esborrat amb exit el tipus 'Seccio' dels recursos 'linkables' del Kupu")

    # Eliminem la transform del fck
    transformstool = getToolByName(context, 'portal_transforms', None)
    try:
        transformstool.manage_delObjects('fck_ruid_to_url')
        logger.warn("Lesborrat de la transform de l'FCK ha estat satisfactoria")
    except:
        logger.warn("Encara que s'ha intentat, l'esborrat de la transform de l'FCK ha fallat")

    # Canviem el rol per defecte dels usuaris autenticats via LDAP
    acl_users = getToolByName(context, 'acl_users')
    acl_users.ldapUPC.acl_users.manage_edit("ldapUPC", "cn", "cn", "ou=Users,dc=upc,dc=edu", 2, "Authenticated",
            "ou=Groups,dc=upc,dc=edu", 2, "cn=ldap.upc,ou=Users,dc=upc,dc=edu", "secret", 1, "cn",
            "top,person", 0, 0, "SSHA", 1, '')
    logger.warn("S'ha canviat el rol dels usuaris autenticats via LDAP")

    return 'Purgat completat.'


class migracioView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        return migracio(self.context)


def browserUpgrader(plonesite):
    import requests
    host = "localhost"
    port = "8080"
    #logger = logging.getLogger('Genweb 4: Migrator')

    r = requests.post("http://%s:%s/%s/%s/@@plone-upgrade?form.submitted=True&submit=Actualitzaci\xf3"
% (host, port, plonesite.id, plonesite.id), auth=('admin', 'admin'))


def listPloneSites(context):
    out = []
    for item in context.values():
        #if IPloneSiteRoot.providedBy(item):
        #    out.append(item)
        if IFolder.providedBy(item):
            for site in item.values():
                if IPloneSiteRoot.providedBy(site):
                    out.append(site)
    return out


class migracioMassiva(BrowserView):

    def __call__(self):
        context = aq_inner(self.context)
        logger = logging.getLogger('Genweb 4: Migrator')
        for plonesite in listPloneSites(context):
            # import ipdb; ipdb.set_trace()
            logger.info("Upgradant el site %s a GW4" % plonesite.id)
            # Purgat i varis
            logger.info("Preparant el site %s" % plonesite.id)
            migracio(plonesite)
            logger.info("Preparacio acabada")

            #Upgrade de Plone
            logger.info("Upgradant el site %s a Plone 4" % plonesite.id)
            browserUpgrader(plonesite)

            # Reinstalacio del upc.genwebupc
            product = 'upc.genwebupc'
            logger.info("Reinstalling product %s in site %s" % (product, plonesite))
            qi = getattr(plonesite, 'portal_quickinstaller', None)
            try:
                qi.reinstallProducts(products=[product])
            except:
                logger.info("Failed reinstall in %s" % plonesite.id)
            import transaction
            transaction.commit()
            logger.info("Successful installed in %s" % plonesite.id)
