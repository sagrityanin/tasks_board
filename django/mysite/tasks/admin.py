from django.contrib import admin
from .models import Person, Task, StatusModel, Pc

admin.site.register(Person)
admin.site.register(Task)
admin.site.register(StatusModel)
# admin.site.register(Pc)
@admin.register(Pc)
class PcAdmin(admin.ModelAdmin):
    list_display = ("title", "telefon_number", "ip", "rdb_user", "note")
    # list_display_links = ("title", )
    ordering = ["title"]
    # list_editable = ("title", "telefon_number", "ip", "rdb_user", "note")
    list_per_page = 15
    # actions = ['set_published', 'set_draft']
    search_fields = ["title", "telefon_number", "ip", "rdb_user"]

