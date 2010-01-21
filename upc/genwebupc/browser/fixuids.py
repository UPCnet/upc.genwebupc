from Acquisition import aq_inner

import re

from httplib import HTTP
from urlparse import urlparse

from zope.component import getMultiAdapter

from Products.CMFCore.utils import getToolByName

from Products.Five.browser import BrowserView

from Products.CMFPlone import PloneMessageFactory as _

from Products.statusmessages.interfaces import IStatusMessage

class fixUIDs(BrowserView):

    def __call__(self):
        context = aq_inner(self.context)        
        s = context.getRawText()
        count = 0
        urls = re.findall(r'(href|src)=[\'"]?([^\'" >]+)', s)
        for url in urls:
            url = url[1]
            url = url.strip('&quot;')
            if not url.startswith("http://") and not url.startswith("@@"):
                catalog = getToolByName(context, 'portal_catalog')
                try:
                    query_url = "/economia/economia" + url
                    brain = catalog(path=dict(query=query_url))[0]
                    new_url = "resolveuid/%s" % brain.UID
                    s = s.replace(url, new_url)
                    IStatusMessage(self.request).addStatusMessage(\
                                                                  _("Fix: %s => %s" % (url, new_url)),
                                                                 type="info")
                    count = count + 1
                except:
                    IStatusMessage(self.request).addStatusMessage(\
                                                                  _("Not fixed URL: %s" % url),
                                                                  type="error")
            elif url.startswith("http://"):
                # check URL
                #if not self.checkURL(url):
                #    IStatusMessage(self.request).addStatusMessage(\
                #                                                  _("URL '%s' was not accessable" % url),
                #                                                  type="error")
                pass
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
        for brain in brains:
            view = getMultiAdapter((brain.getObject(), request), name="fix-uids")
            view = view.__of__(context)
            view()
            IStatusMessage(self.request).addStatusMessage(\
                _("Fix UIDs for %s" % brain.getURL()),
                type="info")
            return context.REQUEST.RESPONSE.redirect(context.absolute_url())
