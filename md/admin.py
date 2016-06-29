from django.contrib import admin
from md.models import Agency


class AgencyAdmin(admin.ModelAdmin):
    pass


admin.site.register(Agency, AgencyAdmin)
