from django.contrib import admin
from .models import PoliticalDocument, PoliticalAd


class PoliticalAdAdmin(admin.ModelAdmin):
    pass

admin.site.register(PoliticalAd, PoliticalAdAdmin)


class PoliticalAdInline(admin.StackedInline):
    model = PoliticalAd
        

class PoliticalDocumentAdmin(admin.ModelAdmin):
   list_display = ('station', 'documentcloud_doc', 'advertiser', 'ordered_by')
   inlines = [
       PoliticalAdInline,
   ]
   class Media:
       js = ('admin/js/bootstrap-typeahead.min.js',)
       css = {
           'all': ('admin/css/fcc_admin.css',)
       }

admin.site.register(PoliticalDocument, PoliticalDocumentAdmin)