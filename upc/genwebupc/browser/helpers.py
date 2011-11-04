# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from App.config import getConfiguration
from Products.CMFPlone.interfaces import IPloneSiteRoot
from OFS.interfaces import IFolder
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from five import grok
from OFS.interfaces import IApplication
import json


DORSALS = {"1": "Víctor Valdés", "2": "Dani Alves", "3": "Piqué", "4": "Cesc", "5": "Puyol", "6": "Xavi", "7": "David Villa", "8": "A. Iniesta", "9": "Alexis", "10": "Messi", "11": "Thiago", "12": "Unknown", "13": "Pinto", "14": "Mascherano", "15": "Keita", "16": "Sergio", "17": "Pedro"}


class getZEO(BrowserView):
    """ Funcio que agafa el numero de zeo al que esta assignat la instancia de genweb.
        Per aixo, el buildout s'ha d'afegir una linea a la zope-conf-additional:
        zope-conf-additional =
           <product-config genweb>
               zeo 9
           </product-config>
    """

    def dorsal(self):
        config = getConfiguration()
        configuration = config.product_config.get('genwebconfig', dict())
        zeo = configuration.get('zeo')
        return zeo

    def nomDorsal(self):
        return DORSALS[self.dorsal()]


def listPloneSites(zope):
    out = []
    for item in zope.values():
        if IFolder.providedBy(item):
            for site in item.values():
                if IPloneSiteRoot.providedBy(site):
                    out.append(site)
    return out


class listPloneSitesView(grok.View):
    grok.name('listPloneSites')
    grok.context(IApplication)
    grok.require('zope2.View')

    def render(self):
        context = aq_inner(self.context)
        out = []
        for item in context.values():
            #if IPloneSiteRoot.providedBy(item):
            #    out.append(item)
            if IFolder.providedBy(item):
                for site in item.values():
                    if IPloneSiteRoot.providedBy(site):
                        out.append(item.id + '/' + site.id)
        return json.dumps(out)


class getFlavourSitesView(grok.View):
    grok.name('getFlavourSites')
    grok.context(IApplication)
    grok.require('zope2.View')

    def render(self):
        context = aq_inner(self.context)
        plonesites = listPloneSites(context)
        out = {}
        for plonesite in plonesites:
            portal_skins = getToolByName(plonesite, 'portal_skins')
            out[plonesite.id] = portal_skins.getDefaultSkin()
        return json.dumps(out)


class getFlavourSiteView(grok.View):
    grok.name('getFlavourSite')
    grok.context(IPloneSiteRoot)
    grok.require('zope2.View')

    def render(self):
        context = aq_inner(self.context)
        portal_skins = getToolByName(context, 'portal_skins')
        return portal_skins.getDefaultSkin()
