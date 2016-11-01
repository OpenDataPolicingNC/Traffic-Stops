from django.contrib import admin, messages
from tsdata.models import Dataset, Import, CensusProfile
from tsdata.tasks import import_dataset


class DatasetAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'state', 'date_received', 'destination')
    list_filter = ('state',)
    ordering = ('-date_received',)
    search_fields = ('name', 'url')
    date_hierarchy = 'date_received'
    actions = ['import_dataset']

    def import_dataset(self, request, queryset):
        if queryset.count() > 1:
            self.message_user(request, "Please select one dataset at a time",
                              level=messages.ERROR)
            return
        import_dataset.delay(queryset[0].pk)
        msg = "{} successfully queued for import.".format(queryset[0].name)
        self.message_user(request, msg)
    import_dataset.short_description = "Import selected dataset"


class ImportAdmin(admin.ModelAdmin):
    list_display = ('id', 'dataset', 'date_started', 'date_finished',
                    'successful')
    list_filter = ('successful',)
    date_hierarchy = 'date_started'
    search_fields = ('dataset__name', 'dataset__state', 'dataset__url')
    ordering = ('-date_started',)


class CensusProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'location', 'state', 'geography',
                    'white', 'black', 'hispanic', 'total', 'source')
    list_filter = ('state', 'geography', 'source')
    search_fields = ('location', 'state', 'geography')
    ordering = ('location',)


admin.site.register(Dataset, DatasetAdmin)
admin.site.register(Import, ImportAdmin)
admin.site.register(CensusProfile, CensusProfileAdmin)
