from setuptools import setup, find_packages

version = '0.1'

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
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
