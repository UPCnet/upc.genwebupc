from setuptools import setup, find_packages
import os

version = '4.0b1'

setup(name='upc.genwebupc',
      version=version,
      description="Paquet de funcionalitats de Genweb UPC",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='genwebupc genweb upc upcnet',
      author='PloneTeam@UPCnet',
      author_email='plone.team@upcnet.es',
      url='https://github.com/UPCnet/upc.genwebupc',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['upc'],
      include_package_data=True,
      zip_safe=False,
      extras_require = {
          'test': [
              'plone.app.testing',
          ]
      },
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'genweb.stack',
          'upc.genwebupctheme',
          'upc.genweb.banners',
          'upc.genweb.logosfooter',
          # 'Products.PloneSurvey',
          # 'upc.genweb.meetings',
          # 'upc.genweb.descriptorTIC',
          # 'upc.genweb.kbpuc',
          # 'upc.genweb.objectiusCG',
          # 'upc.genweb.patches',
          # 'upc.permalink',
          # 'upc.genweb.serveis',
          # 'upc.remotecontrol',
          # 'upcnet.simpleTask',
          'upcnet.cas',
          # 'Products.AJAXAddRemoveWidget',
          # 'Products.AddRemoveWidget',
          'Products.DataGridField',
          'Products.ZMySQLDA',
          'archetypes.schemaextender',
          'upc.genweb.recaptcha',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
