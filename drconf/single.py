import os
import django
os.environ.update({"DJANGO_SETTINGS_MODULE":"drconf.settings"})
django.setup()
