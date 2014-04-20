# -*- encoding: utf-8 -*-

# Configuration file for production

from base import *

# website root directory
basedir = "/var/www"

# jinja2 templates directory
template_dir = '/home/user/cines/templates'

# output webpages filenames
bycine_file =  "%s/index.html" % basedir
settings_file = "%s/preferences.html" % basedir
about_file = "%s/about.html" % basedir