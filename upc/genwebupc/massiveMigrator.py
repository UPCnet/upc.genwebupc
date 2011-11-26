#!/usr/bin/python
# Script que agafa les instancies a un entorn en concret i fa la migracio a GW4
# Usage: massiveMigrator.py host port_frontend
# e.g.: mantenimentBlobs.py sylarc.upc.edu 11001
#

import requests
import sys
import json
import logging

host = sys.argv[1]
port = sys.argv[2]

user = 'admin'
password = 'tzmLidT8'

logger = logging.getLogger('Script Migracio GW4')
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)

skinmap = {'Tema genwebUPC Master': 'GenwebUPC_Master',
           'Tema genwebUPC Neutre2': 'GenwebUPC_Neutre2',
           'Tema genwebUPC Neutre3': 'GenwebUPC_Neutre3',
           'Tema genwebUPC Unitat': 'GenwebUPC_Unitat',
           'GenwebUPC_Master': 'GenwebUPC_Master',
           'GenwebUPC_Neutre2': 'GenwebUPC_Neutre2',
           'GenwebUPC_Neutre3': 'GenwebUPC_Neutre3',
           'GenwebUPC_Unitat': 'GenwebUPC_Unitat',
           'Plone Default': 'Plone Default'}

getSites = requests.get("http://%s:%s/@@listPloneSites" % (host, port))
getSkins = requests.get("http://%s:%s/@@getFlavourSites" % (host, port))
getLanguages = requests.get("http://%s:%s/@@getLanguagesSites" % (host, port))
getDefaultLanguage = requests.get("http://%s:%s/@@getDefaultLanguageSites" % (host, port))
getDefaultWF = requests.get("http://%s:%s/@@getDefaultWFSites" % (host, port))

plonesites = json.loads(getSites.content)
skins = json.loads(getSkins.content)
languages = json.loads(getLanguages.content)
deflang = json.loads(getDefaultLanguage.content)
defwf = json.loads(getDefaultWF.content)

logger.info('=========================================')
logger.info(plonesites)
logger.info(skins)
logger.info(languages)
logger.info(deflang)
logger.info(defwf)
logger.info('=========================================')

for plonesite in plonesites:
    # Purgat + preparacio
    logger.info("%s: Purgat" % plonesite.split('/')[1])
    purgat = requests.get("http://%s:%s/%s/purge" % (host, port, plonesite), auth=(user, password))

    # Upgrade a Plone 4
    logger.info("%s: Upgrade a Plone 4" % plonesite.split('/')[1])
    upgrade = requests.post("http://%s:%s/%s/@@plone-upgrade?form.submitted=True&submit=Upgrade" % (host, port, plonesite), auth=(user, password))

    # Reinstall GW
    logger.info("%s: Reinstalacio" % plonesite.split('/')[1])
    uninstall = requests.post("http://%s:%s/%s/portal_quickinstaller?products%%3Alist=upc.genwebupc&uninstallProducts%%3Amethod=Uninstall" % (host, port, plonesite), auth=(user, password))
    install = requests.post("http://%s:%s/%s/portal_quickinstaller/installProducts?products%%3Alist=upc.genwebupc&Install" % (host, port, plonesite), auth=(user, password))

    # Reaplica el sabor
    logger.info("%s: Reaplicant el sabor" % plonesite.split('/')[1])
    flavour = requests.get("http://%s:%s/%s/portal_skins/manage_properties?default_skin=%s&request_varname=plone_skin&submit=Save" % (host, port, plonesite, skinmap[skins[plonesite.split('/')[1]]]), auth=(user, password))

    # Reaplica els llenguatges
    logger.info("%s: Reaplicant els llenguatges" % plonesite.split('/')[1])
    # &form.available_languages%3Alist=ca&form.available_languages%3Alist=en
    langstrdef = "&form.available_languages%3Alist="
    langstr = ""
    for language in languages[plonesite.split('/')[1]]:
        langstr = langstr + langstrdef + language

    from BeautifulSoup import BeautifulSoup

    languagesauth = requests.get("http://%s:%s/%s/@@language-controlpanel" % (host, port, plonesite), auth=(user, password))
    soup = BeautifulSoup(languagesauth.content)
    authenticator = soup.find("input", dict(type='hidden', name='_authenticator'))

    languagesreq = requests.get("http://%s:%s/%s/@@language-controlpanel?fieldset.current=&form.default_language=%s&form.default_language-empty-marker=1%s&form.available_languages-empty-marker=1&form.actions.save=Desa&_authenticator=%s" % (host, port, plonesite, deflang[plonesite.split('/')[1]], langstr, authenticator.get('value')), auth=(user, password))

    # Afegeix les carpetes de templates de TinyMCE
    logger.info("%s: Creant carpetes Tiny" % plonesite.split('/')[1])
    templates = requests.get("http://%s:%s/%s/@@afegirPlantillesTiny" % (host, port, plonesite), auth=(user, password))

    # Reaplica el WF per defecte del site
    logger.info("%s: Reaplicant WF" % plonesite.split('/')[1])
    dwf = requests.get("http://%s:%s/%s/@@reaplicarDefaultWF?wf=%s" % (host, port, plonesite, defwf[plonesite.split('/')[1]][0]), auth=(user, password))

    # Canvia el editor per defecte a tots els users de cada site
    logger.info("%s: Canvia editor per defecte" % plonesite.split('/')[1])
    tiny = requests.get("http://%s:%s/%s/@@canviaFCKperTiny" % (host, port, plonesite), auth=(user, password))

    # TODO, afegir plantilles
