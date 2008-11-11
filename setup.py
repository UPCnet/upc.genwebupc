from setuptools import setup, find_packages

version = '3.0'

setup(name='upc.genwebupc',
      version=version,
      description="Paquet de funcionalitats de genwebupc",
      long_description="""\
""",
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
      url='https://devel.upcnet.es/trac/genwebupc',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['upc'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'upc.genwebupctheme',          
          'upc.genweb.banners',
          'upc.genweb.logosfooter',
          'upc.genweb.meetings',          
          'upc.permalink',
          'Products.AJAXAddRemoveWidget',
          'upcnet.simpleTask',          
          'plone.app.blob',
          'Products.PloneLDAP',
          'Products.FCKeditor',
          'Products.Ploneboard',
          'Products.PloneFormGen',
          'Products.LinguaPlone',
          'Products.Collage',
          'Products.AddRemoveWidget',
          'Products.DataGridField',
          'Products.PythonField',
          'Products.TemplateFields',
          'Products.TALESField',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
