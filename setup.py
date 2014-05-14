from distutils.core import setup
import py2exe, sys, os

setup(console=['enableds.py'],
      data_files=['cacert.pem', 'config.json'])
