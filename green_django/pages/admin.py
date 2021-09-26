from django.contrib import admin
from .models import *

admin.site.site_header = 'SYS Administration'
admin.site.site_title = "Admin Portal"


admin.site.register(Dashboard)
admin.site.register(Detail)
admin.site.register(SensorHisData)
