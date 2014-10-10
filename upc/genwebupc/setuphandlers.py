from Products.CMFCore.utils import getToolByName
from Products.PloneLDAP.factory import manage_addPloneLDAPMultiPlugin
from Products.LDAPUserFolder.LDAPUserFolder import LDAPUserFolder

from plone.app.controlpanel.site import ISiteSchema

import transaction
import os

LDAP_PASSWORD = os.environ.get('ldapbindpasswd', '')


def setupVarious(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('upc.genwebupc_various.txt') is None:
        return

    # Add additional setup code here
    #
    portal = context.getSite()
    transforms = getToolByName(portal, 'portal_transforms')
    transform = getattr(transforms, 'safe_html')
    valid = transform.get_parameter_value('valid_tags')
    nasty = transform.get_parameter_value('nasty_tags')
    # GW4 Valid tags
    gw4_valid = ['script', 'object', 'embed', 'param', 'iframe', 'applet']
    for tag in gw4_valid:
        # Acceptar a la llista de valides
        valid[tag] = 1
        # Eliminar de la llista no desitjades
        if tag in nasty:
            del nasty[tag]

    stripped = transform.get_parameter_value('stripped_attributes')
    # GW4 remove some stripped
    for tag in ['cellspacing', 'cellpadding', 'valign']:
        if tag in stripped:
            stripped.remove(tag)

    kwargs = {}
    kwargs['valid_tags'] = valid
    kwargs['nasty_tags'] = nasty
    kwargs['stripped_attributes'] = stripped

    for k in list(kwargs):
        if isinstance(kwargs[k], dict):
            v = kwargs[k]
            kwargs[k + '_key'] = v.keys()
            kwargs[k + '_value'] = [str(s) for s in v.values()]
            del kwargs[k]
    transform.set_parameters(**kwargs)
    transform._p_changed = True
    transform.reload()
    try:
            manage_addPloneLDAPMultiPlugin(portal.acl_users, "ldapUPC",
                title="ldapUPC", use_ssl=1, login_attr="cn", uid_attr="cn", local_groups=0,
                users_base="ou=Users,dc=upc,dc=edu", users_scope=2,
                roles="Authenticated", groups_base="ou=Groups,dc=upc,dc=edu",
                groups_scope=2, read_only=True, binduid="cn=ldap.serveis,ou=users,dc=upc,dc=edu", bindpwd=LDAP_PASSWORD,
                rdn_attr="cn", LDAP_server="ldap.upc.edu", encryption="SSHA")
            portal.acl_users.ldapUPC.acl_users.manage_edit("ldapUPC", "cn", "cn", "ou=Users,dc=upc,dc=edu", 2, "Authenticated",
                "ou=Groups,dc=upc,dc=edu", 2, "cn=ldap.serveis,ou=users,dc=upc,dc=edu", LDAP_PASSWORD, 1, "cn",
                "top,person", 0, 0, "SSHA", 1, '')
            plugin = portal.acl_users['ldapUPC']

            plugin.manage_activateInterfaces(['IGroupEnumerationPlugin', 'IGroupsPlugin', 'IPropertiesPlugin', 'IGroupIntrospection', 'IAuthenticationPlugin', 'IRolesPlugin', 'IUserEnumerationPlugin', 'IRoleEnumerationPlugin'])
            #Comentem la linia per a que no afegeixi
            #LDAPUserFolder.manage_addServer(portal.acl_users.ldapUPC.acl_users, "ldap.upc.edu", '636', use_ssl=1)

            LDAPUserFolder.manage_deleteLDAPSchemaItems(portal.acl_users.ldapUPC.acl_users, ldap_names = ['sn'], REQUEST = None)
            LDAPUserFolder.manage_addLDAPSchemaItem(portal.acl_users.ldapUPC.acl_users, ldap_name='sn', friendly_name='Last Name', public_name='name')

            # Move the ldapUPC to the top of the active plugins.
            # Otherwise member.getProperty('email') won't work properly.
            from Products.PluggableAuthService.interfaces.plugins import IPropertiesPlugin
            portal.acl_users.plugins.movePluginsUp(IPropertiesPlugin, ['ldapUPC'])
            #portal.acl_users.plugins.manage_movePluginsUp('IPropertiesPlugin', ['ldapUPC'], context.REQUEST.RESPONSE)
    except:
            pass

    #try:
            # Fora el sistema de cookies que fan buscar al LDAP cn=*
    #        portal.acl_users.manage_delObjects('credentials_cookie_auth')
    #except:
    #        pass

    plugin = portal.acl_users['ldapUPC']
    plugin.ZCacheable_setManagerId('RAMCache')

    portal_role_manager = portal.acl_users['portal_role_manager']
    portal_role_manager.assignRolesToPrincipal(["Manager"], "UPC.Plone.Admins")
    portal_role_manager.assignRolesToPrincipal(["Manager"], "UPCnet.Plone.Admins")
    portal_role_manager.assignRolesToPrincipal(["Manager"], "UPCnet.ATIC")
    portal_role_manager.assignRolesToPrincipal(["Manager"], "UPCNET.Frontoffice.2n.nivell")

    # deshabilitem inline editing
    site_properties = ISiteSchema(portal)
    site_properties.enable_inline_editing = False

    # configurem pagina per defecte
    portal.setLayout("homepage")

    # configurem els estats del calendari
    pct = getToolByName(portal, 'portal_calendar')
    pct.calendar_states = ('published', 'intranet')
    # Fixem el primer dia de la setmana com dilluns (0)
    pct.firstweekday = 0
    transaction.commit()
