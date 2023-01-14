from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import FormMixin

import logging
import os

from tasks.forms import TaskListForm
from tasks.models import Pc
from tasks.service.menu_make import get_menu, get_sidebar
from .celery_producer import send_telegram


class ListPcMixin(LoginRequiredMixin, FormMixin, ListView):
    allow_empty = True
    paginate_by = int(os.getenv("PC_ON_PAGE_COUNT"))
    http_method_names = ["get"]
    template_name = "tasks/task_list.html"
    context_object_name = "pc_list"

    def get(self, request, *args, **kwargs):
        self.request = request
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty and len(self.object_list) == 0:
            raise Http404(u"Empty list and '%(class_name)s.allow_empty' is False."
                          % {'class_name': self.__class__.__name__})
        context = self.get_context_data(object_list=self.object_list, form=self.form)
        context["len"] = len(self.object_list)
        return render(request, "tasks/pc_list.html", context=context)

    def get_queryset(self):
        if sort_field := self.request.GET.get("sort_form"):
            return Pc.objects.all().order_by(sort_field)
        return Pc.objects.all()

    def get_context(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = get_menu(self.request)
        context["sidebar"] = get_sidebar(self.request)
        return context
