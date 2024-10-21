from django.contrib import admin
from .models import Person, Task, StatusModel, Pc, TaskSection

admin.site.register(Person)
admin.site.register(Task)
admin.site.register(StatusModel)
admin.site.register(TaskSection)
@admin.register(Pc)
class PcAdmin(admin.ModelAdmin):
    list_display = ("title", "telefon_number", "ip", "rdb_user", "note")
    ordering = ["title"]
    list_per_page = 15
    search_fields = ["title", "telefon_number", "ip", "rdb_user"]

