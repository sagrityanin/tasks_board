from django.contrib import admin
from .models import Person, Task, StatusModel

admin.site.register(Person)
admin.site.register(Task)
admin.site.register(StatusModel)
