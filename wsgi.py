#! /usr/bin/env python
# -*- encoding:utf-8 -*-
import os
import sys


PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,PROJECT_DIR)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drconf.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
