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
password = 'admin'

logger = logging.getLogger('Script Migracio GW4')

skinmap = {'Tema genwebUPC Master': 'GenwebUPC_Master',
           'Tema genwebUPC Neutre2': 'GenwebUPC_Neutre2',
           'Tema genwebUPC Neutre3': 'GenwebUPC_Neutre3',
           'Tema genwebUPC Unitat': 'GenwebUPC_Unitat',
           'GenwebUPC_Master': 'GenwebUPC_Master',
           'GenwebUPC_Neutre2': 'GenwebUPC_Neutre2',
           'GenwebUPC_Neutre3': 'GenwebUPC_Neutre3',
           'GenwebUPC_Unitat': 'GenwebUPC_Unitat'}

getSites = requests.get("http://%s:%s/@@listPloneSites" % (host, port))
getSkins = requests.get("http://%s:%s/@@getFlavourSites" % (host, port))

plonesites = json.loads(getSites.content)
skins = json.loads(getSkins.content)

logger.info(skins)

for plonesite in plonesites:
    # Purgat + preparacio
    purgat = requests.get("http://%s:%s/%s/purge" % (host, port, plonesite), auth=(user, password))

    # Upgrade a Plone 4
    upgrade = requests.post("http://%s:%s/%s/@@plone-upgrade?form.submitted=True&submit=Upgrade" % (host, port, plonesite), auth=(user, password))

    # Reinstall GW
    uninstall = requests.post("http://%s:%s/%s/portal_quickinstaller?products%%3Alist=upc.genwebupc&uninstallProducts%%3Amethod=Uninstall" % (host, port, plonesite), auth=(user, password))
    install = requests.post("http://%s:%s/%s/portal_quickinstaller/installProducts?products%%3Alist=upc.genwebupc&Install" % (host, port, plonesite), auth=(user, password))

    # Reaplica el sabor
    flavour = requests.get("http://%s:%s/%s/portal_skins/manage_properties?default_skin=%s&request_varname=plone_skin&submit=Save" % (host, port, plonesite, skinmap[skins[plonesite.split('/')[1]]]), auth=(user, password))
