#!/usr/bin/python
# Script que agafa les instancies a un entorn en concret i fa la migracio a GW4
# Usage: massiveMigrator.py host port_frontend
# e.g.: mantenimentBlobs.py sylarc.upc.edu 11001
#

import requests
import sys
import json

host = sys.argv[1]
port = sys.argv[2]

#logger = logging.getLogger('Genweb 4: Migrator')

getSites = requests.get("http://%s:%s/@@listPloneSites" % (host, port))

import ipdb; ipdb.set_trace( )
plonesites = json.loads(getSites.content)

for plonesite in plonesites:
    # Purgat + preparacio
    purgat = requests.get("http://%s:%s/%s/%s/purge" % (host, port, plonesite, plonesite), auth=('admin', 'admin'))

    # Upgrade a Plone 4
    upgrade = requests.post("http://%s:%s/%s/%s/@@plone-upgrade?form.submitted=True&submit=Upgrade" % (host, port, plonesite, plonesite), auth=('admin', 'admin'))

    # Reinstall GW
    uninstall = requests.post("http://%s:%s/%s/%s/portal_quickinstaller?products%%3Alist=upc.genwebupc&uninstallProducts%%3Amethod=Uninstall" % (host, port, plonesite, plonesite), auth=('admin', 'admin'))
    install = requests.post("http://%s:%s/%s/%s/portal_quickinstaller/installProducts?products%%3Alist=upc.genwebupc&Install" % (host, port, plonesite, plonesite), auth=('admin', 'admin'))
