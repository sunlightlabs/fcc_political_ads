from django.contrib.admin import ModelAdmin

class MildModeratedModelAdmin(ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save(request)
