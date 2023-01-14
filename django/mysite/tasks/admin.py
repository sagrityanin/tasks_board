from django.contrib import admin
from .models import Person, Task, StatusModel, Pc

admin.site.register(Person)
admin.site.register(Task)
admin.site.register(StatusModel)
admin.site.register(Pc)
