from django.contrib import admin
from md.models import Agency


class AgencyAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ("name",),
    }


admin.site.register(Agency, AgencyAdmin)
