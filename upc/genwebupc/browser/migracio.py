from Acquisition import aq_inner, aq_parent

from zope.component import getMultiAdapter
from Products.GenericSetup import profile_registry, EXTENSION
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFCore.utils import getToolByName

from Products.Five.browser import BrowserView

import logging


class migracio(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        logger = logging.getLogger('Genweb 4: Migrator')
        logger.warn('Running Migration')

        setup = getToolByName(self.context, 'portal_setup')
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
        pw = getToolByName(self.context, 'portal_workflow')
        try:
            pw.manage_delObjects('simpleTask_workflow')
            logger.warn("[Esborrar workflow simpleTask] S'ha esborrat el simpleTask_workflow")
        except:
            logger.warn('[Esborrar workflow simpleTask] El simpleTask_workflow ja estava esborrat')

        # Problema amb el SimpleAttachment, treure el 'Large Plone Folder' dels recursos 'linkables'
        kupuTool = getToolByName(self.context, 'kupu_library_tool', None)
        linkable = list(kupuTool.getPortalTypesForResourceType('linkable'))
        if 'Large Plone Folder' in linkable:
            linkable.remove('Large Plone Folder')
            kupuTool.updateResourceTypes(({'resource_type': 'linkable',
                                           'old_type': 'linkable',
                                           'portal_types': linkable},))

            logger.warn("[Esborrar 'Large Plone Folder'] S'ha esborrat amb exit el tipus 'Large Plone Folder' dels recursos 'linkables' del Kupu")
