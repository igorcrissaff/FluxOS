#from django.contrib.admin.apps import SimpleAdminConfig
from django.apps import AppConfig

class DashBoardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.dashboard'
    verbose_name = 'Dashboard'