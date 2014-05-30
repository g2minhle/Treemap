#!/usr/bin/env python

'''distutils setup for PyGraphics.
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: setup.py 1855 2008-03-01 11:29:25Z Paul Gries $'

VERSION='2.1'

long_description='''PyGraphics provides a set of easy-to-use procedural media
manipulation tools and is intended for new programmers.  It is based on a
Jython library developed by Mark Guzdial at Georgia Tech.'''

from distutils.core import setup
setup(name='PyGraphics',
      version=VERSION,
      author='Jen Campbell, Paul Gries, Leo Kaliazine, Chris Maddison, Hardeep Singh, Devin Jeanpierre',
      license='GPL',
      url='http://code.google.com/p/pygraphics',
      author_email='pgries@cs.toronto.edu',
      description='Easily-accessible library for media manipulation',
      long_description=long_description,
      extra_path = "pygraphics",
      classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Intended Audience :: Developers',
        #'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows', # XP
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        #'Topic :: Games/Entertainment',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],

      package_dir={"": "cpython"},
      py_modules=[
        'picture',
        'color',
        'media',
        'pixel',
        'sound'
      ],
      packages=[
        'mediawindows'
      ])
