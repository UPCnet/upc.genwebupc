# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

from five import grok
from hashlib import sha1
from plone import api
from zope.interface import Interface

import datetime


class enquestaRedirect(grok.View):
    grok.name('enquesta-asepeyo')
    grok.context(Interface)
    grok.require('zope2.View')

    def render(self):
        context = aq_inner(self.context)
        if api.user.is_anonymous():
            return self.request.response.redirect(context.absolute_url())
        logged_user = api.user.get_current()

        user_token = logged_user.getProperty('asepeyo_hash')
        if not user_token:
            user_seed = '%s %s' % (logged_user.id, datetime.datetime.now().isoformat())
            user_token = sha1(user_seed).hexdigest()
            logged_user.setMemberProperties(mapping={"asepeyo_hash": user_token})

        enquesta_url = 'http://www.encuestafacil.com/RespWeb/Qn.aspx?EID=1883359&ParamID=%s' % user_token
        return self.request.response.redirect(enquesta_url)


class enquestaTokens(grok.View):
    grok.name('enquesta-asepeyo-tokens')
    grok.context(Interface)
    grok.require('cmf.ManagePortal')

    def render(self):
        mdata = getToolByName(self.context, 'portal_memberdata')
        users = [api.user.get(a) for a in mdata._members]
        users = [user for user in users if user]
        return '\n'.join(['%s,%s' % (user.id, user.getProperty('asepeyo_hash')) for user in users if user.getProperty('asepeyo_hash')])
