"""
Scrapy - a screen scraping framework written in Python
"""

version_info = (0, 16, 2)
__version__ = "0.16.2"

import sys, os, warnings

if sys.version_info < (2,6):
    print "Scrapy %s requires Python 2.6 or above" % __version__
    sys.exit(1)

# ignore noisy twisted deprecation warnings
warnings.filterwarnings('ignore', category=DeprecationWarning, module='twisted')

# monkey patches to fix external library issues
from scrapy.xlib import urlparse_monkeypatches

# optional_features is a set containing Scrapy optional features
optional_features = set()

try:
    import OpenSSL
except ImportError:
    pass
else:
    optional_features.add('ssl')

try:
    import boto
except ImportError:
    pass
else:
    optional_features.add('boto')

try:
    import libxml2
except ImportError:
    pass
else:
    optional_features.add('libxml2')
