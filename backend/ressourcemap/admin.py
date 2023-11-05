from django.contrib import admin
from .models import Map, Ressource, RessourceCategory, RessourceNode

class CustomModelAdmin(admin.ModelAdmin):
    # Customize foreign key representation
    def display_related_name(self, obj, field_name):
        related_obj = getattr(obj, field_name)
        return related_obj.name if related_obj else None

    def custom_related_name(self, obj):
        return f'{self.display_related_name(obj, "map")}, {self.display_related_name(obj, "ressource")}'

    custom_related_name.short_description = 'Custom Foreign Key Display'

# Register your models with the custom admin class
admin.site.register(Map, CustomModelAdmin)
admin.site.register(Ressource, CustomModelAdmin)
admin.site.register(RessourceCategory, CustomModelAdmin)
admin.site.register(RessourceNode, CustomModelAdmin)
