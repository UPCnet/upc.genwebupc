from Acquisition import aq_inner

import re

from httplib import HTTP
from urlparse import urlparse

from zope.component import getMultiAdapter

from Products.CMFCore.utils import getToolByName

from Products.Five.browser import BrowserView


class fixUIDs(BrowserView):

    def __call__(self):
        context = aq_inner(self.context)        
        s = context.getRawText()
        urls = re.findall(r'(href|src)=[\'"]?([^\'" >]+)', s)
        for url in urls:
            url = url[1]
            url = url.strip('&quot;')
            if not url.startswith("http://"):
                catalog = getToolByName(context, 'portal_catalog')
                brain = catalog(path=dict(query='/%s' % url))[0]
                new_url = "resolveuid/%s" % brain.UID
                ns = s.replace(url, new_url)
                print "\nOLD:%s" % s
                print "\nNEW:%s" % ns
                context.setText(ns)     
            else:
                # check URL
                print "\nKEEP:%s" % s
                print "\nCHECK:%s" % self.checkURL(url)
        context.reindexObject()       

    def checkURL(self, url):
        """Checks if a URL is accessable.
        """
        try:
            p = urlparse(url)
            h = HTTP(p[1])
            h.putrequest('HEAD', p[2])
            h.endheaders()
            if h.getreply()[0] == 200: return 1
            else: return 0
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
        brains = catalog.searchResults(Type='Document')
        for brain in brains:
            brain.getObject().restrictedTraverse("@@fix-uids")
            print "Fix UIDs for %s" % brain.getURL()
            #view = getMultiAdapter((brain.getObject(), request), name="fix-uids")
            #view = view.__of__(context)
            #self.failUnless(view())        
