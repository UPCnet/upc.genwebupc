from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView

from Products.CMFPlone.utils import _createObjectByType
from five import grok
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Acquisition import aq_inner
import logging


def migracio(context):
    """Funcio que realitza la migracio de GW3 a GW4"""
    logger = logging.getLogger('Genweb 4: Migrator')
    logger.warn('======================================================================')
    logger.warn('%s' % context.id)
    logger.info('Running Migration')

    setup = getToolByName(context, 'portal_setup')
    ir = setup.getImportStepRegistry()
    ir.listSteps()
    logger.info('%s', ir.listSteps())

    try:
        ir.unregisterStep('upc.genweb.logosfooter.various')
        ir.unregisterStep('cachesettings')
        ir.unregisterStep('meetings-QI-dependencies')
        ir.unregisterStep('meetings-Update-RoleMappings')
        ir.unregisterStep('meetings-postInstall')
        ir.unregisterStep('meetings-GS-dependencies')
        ir.unregisterStep('upc.genweb.banners.various')
        ir.unregisterStep('upc.genweb.descriptorTIC-postInstall')
        logger.info("[Desregistrar steps de GS invalids] S'han desregistrat tots els steps correctament.")
    except:
        logger.info("[Desregistrar steps de GS invalids] Alguns dels steps no s'han trobat ja estaven esborrats o no existeixen")

    # Esborro el workflow que fa petar el migrador de Plone, despres ja es tornara a afegir
    pw = getToolByName(context, 'portal_workflow')
    try:
        pw.manage_delObjects('simpleTask_workflow')
        logger.info("[Esborrar workflow simpleTask] S'ha esborrat el simpleTask_workflow")
    except:
        logger.info('[Esborrar workflow simpleTask] El simpleTask_workflow ja estava esborrat')

    # Problema amb el SimpleAttachment, treure el 'Large Plone Folder' dels recursos 'linkables'
    kupuTool = getToolByName(context, 'kupu_library_tool', None)
    linkable = list(kupuTool.getPortalTypesForResourceType('linkable'))
    if 'Large Plone Folder' in linkable:
        linkable.remove('Large Plone Folder')
        kupuTool.updateResourceTypes(({'resource_type': 'linkable',
                                       'old_type': 'linkable',
                                       'portal_types': linkable},))

        logger.info("[Esborrar 'Large Plone Folder'] S'ha esborrat amb exit el tipus 'Large Plone Folder' dels recursos 'linkables' del Kupu")

    if 'Seccio' in linkable:
        linkable.remove('Seccio')
        kupuTool.updateResourceTypes(({'resource_type': 'linkable',
                                       'old_type': 'linkable',
                                       'portal_types': linkable},))

        logger.info("[Esborrar 'Seccio'] S'ha esborrat amb exit el tipus 'Seccio' dels recursos 'linkables' del Kupu")

    # Eliminem la transform del fck
    transformstool = getToolByName(context, 'portal_transforms', None)
    try:
        transformstool.manage_delObjects('fck_ruid_to_url')
        logger.info("Lesborrat de la transform de l'FCK ha estat satisfactoria")
    except:
        logger.info("Encara que s'ha intentat, l'esborrat de la transform de l'FCK ha fallat")

    # Canviem el rol per defecte dels usuaris autenticats via LDAP
    acl_users = getToolByName(context, 'acl_users')
    acl_users.ldapUPC.acl_users.manage_edit("ldapUPC", "cn", "cn", "ou=Users,dc=upc,dc=edu", 2, "Authenticated",
            "ou=Groups,dc=upc,dc=edu", 2, "cn=ldap.upc,ou=Users,dc=upc,dc=edu", "secret", 1, "cn",
            "top,person", 0, 0, "SSHA", 1, '')
    logger.info("S'ha canviat el rol dels usuaris autenticats via LDAP")

    return 'Purgat completat.'


def crearObjecte(self, context, id, type_name, title, description, exclude=True, constrains=None):
    pt = getToolByName(context, 'portal_types')
    if not getattr(context, id, False) and type_name in pt.listTypeTitles().keys():
        #creem l'objecte i el publiquem
        _createObjectByType(type_name, context, id)
    #populem l'objecte
    created = context[id]
    self.doWorkflowAction(created)
    created.setTitle(title)
    created.setDescription(description)
    created._at_creation_flag = False
    created.setExcludeFromNav(exclude)
    if constrains:
        created.setConstrainTypesMode(1)
        if len(constrains) > 1:
            created.setLocallyAllowedTypes(tuple(constrains[0] + constrains[1]))
        else:
            created.setLocallyAllowedTypes(tuple(constrains[0]))
        created.setImmediatelyAddableTypes(tuple(constrains[0]))

    created.reindexObject()
    return created


class migracioView(BrowserView):
    """Vista principal que s'ocupa de la migracio"""
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        return migracio(self.context)


class afegirPlantillesTiny(grok.View):
    """Creacio dels objectes necessaris per a que funcioni el motor de templates de TinyMCE"""
    grok.name('afegirPlantillesTiny')
    grok.context(IPloneSiteRoot)
    grok.require('zope2.ViewManagementScreens')

    def render(self):
        context = aq_inner(self.context)
        pw = getToolByName(context, 'portal_workflow')
        templates = crearObjecte(context, 'templates', 'Folder', 'Templates', 'Plantilles per defecte administrades per l\'SCP.', constrains=(['Document']))
        plantilles = crearObjecte(context, 'plantilles', 'Folder', 'Plantilles', 'En aquesta carpeta podeu posar les plantilles per ser usades a l\'editor.', constrains = (['Document']))
        pw.doActionFor(templates, "restrict")
        return "OK"


class reaplicarDefaultWF(grok.View):
    """Reaplica el WF per defecte, donat un WF"""
    grok.name('reaplicarDefaultWF')
    grok.context(IPloneSiteRoot)
    grok.require('zope2.ViewManagementScreens')

    def render(self):
        context = aq_inner(self.context)
        wf = self.request.get('wf', None)
        if wf is not None:
            pw = getToolByName(context, 'portal_workflow')
            pw.setDefaultChain(wf)
            return wf
        else:
            return 'No workflow definit.'


class canviaFCKperTiny(grok.View):
    """Pues eso..."""
    grok.name('canviaFCKperTiny')
    grok.context(IPloneSiteRoot)
    grok.require('zope2.ViewManagementScreens')

    def render(self):
        context = aq_inner(self.context)
        logger = logging.getLogger('Genweb 4: Migrator')
        pm = getToolByName(context, 'portal_membership')
        for memberId in pm.listMemberIds():
            member = pm.getMemberById(memberId)
            editor = member.getProperty('wysiwyg_editor', None)
            if editor == 'TinyMCE':
                logger.info('%s: TinyMCE already selected, leaving alone' % memberId)
            else:
                member.setMemberProperties({'wysiwyg_editor': 'TinyMCE'})
                logger.info('%s: TinyMCE has been set' % memberId)

        return 'OK'
