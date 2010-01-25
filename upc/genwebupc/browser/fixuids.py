from Acquisition import aq_inner, aq_parent

import re

from httplib import HTTP
from urlparse import urlparse

from zope.component import getMultiAdapter

from Products.CMFCore.utils import getToolByName

from Products.Five.browser import BrowserView

from Products.CMFPlone import PloneMessageFactory as _

from Products.statusmessages.interfaces import IStatusMessage

from BeautifulSoup import BeautifulSoup

class fixUIDs(BrowserView):

    def __call__(self):
        context = aq_inner(self.context)
        s = context.getRawText()
        if s == "" or s == "<br />":
            return context.REQUEST.RESPONSE.redirect(context.absolute_url())
        count = 0
        soup = BeautifulSoup(s)
        for tag in soup.findAll(['a', 'img']):
            if tag.has_key('href'):
                url = tag['href']
            elif tag.has_key('src'):
                url = tag['src']
            else:
                continue
            if url.startswith("http://") or url.startswith("@@") or url.startswith("resolveuid") or url.startswith("plone_") or url.startswith("prefs_"):
                pass
            else:
                catalog = getToolByName(context, 'portal_catalog')
                try:
                    #query_url = '/' + context.absolute_url(relative=True) + url
                    instance = aq_parent(self).id
                    query_url = "/%s/%s%s" % (instance, instance, url)
                    if self.request['URL'] == 'http://nohost':
                        # For tests, we don't have a mount point
                        query_url = url
                    brain = catalog(path=dict(query=query_url))[0]
                    new_url = "resolveuid/%s" % brain.UID
                    s = s.replace(url, new_url)
                    IStatusMessage(self.request).addStatusMessage(\
                                                                  _("Fix: %s => %s" % (url, new_url)),
                                                                 type="info")
                    count = count + 1
                except:
                    IStatusMessage(self.request).addStatusMessage(\
                                                                  _("Not fixed: %s (QUERY: %s)" % (url, query_url)),
                                                                  type="error")
        context.setText(s)
        context.reindexObject()

        IStatusMessage(self.request).addStatusMessage(\
                                                      _("%s URLs fixed." % count),
                                                      type="info")
        return context.REQUEST.RESPONSE.redirect(context.absolute_url())

    def checkURL(self, url):
        """Checks if a URL is accessable.
        """
        try:
            purl = urlparse(url)
            h = HTTP(purl[1])
            h.putrequest('HEAD', purl[2])
            h.endheaders()
            if h.getreply()[0] == 200: 
                return 1
            else:
                return 0
        except:
            return 0
  
class fixAllUIDs(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        context = aq_inner(self.context)
        request = self.request
        catalog = getToolByName(context,'portal_catalog')
        brains = catalog.searchResults(Type='Page')
        brains += catalog.searchResults(Type='News Item')
        brains += catalog.searchResults(Type='Event')
        print "BRAINS: %s" % len(brains)
        for brain in brains:
            view = getMultiAdapter((brain.getObject(), request), name="fix-uids")
            view = view.__of__(context)
            view()
            print "FIX %s" % brain.getURL()
        print "Fix UIDs finished"
        IStatusMessage(self.request).addStatusMessage(\
                _("%s content objects fixed" % len(brains)),
                type="info")
        return context.REQUEST.RESPONSE.redirect(context.absolute_url())
