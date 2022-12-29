import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class TimeStampMixin(models.Model):
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUINMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Status(models.TextChoices):
    CREATED = "created", _("created")
    EXECUTED = "executed", _("executed")
    DEPRECATED = "deprecated", _("deprecated")


class Task(TimeStampMixin, UUINMixin):
    title = models.CharField(verbose_name=_('title'), max_length=255)
    note = models.TextField(verbose_name=_('note'), blank=True)
    is_visible = models.BooleanField(verbose_name=_('is_visible'), default=True)
    status = models.TextField(verbose_name=_("Status"), choices=Status.choices, null=False, default="created")
    creator = models.ForeignKey("Person", verbose_name=_("creator"), on_delete=models.CASCADE,
                                related_name="creator", blank=True)
    executor = models.ForeignKey("Person", verbose_name=_('executor'), on_delete=models.CASCADE,
                                 related_name="executor")

    class Meta:
        db_table = "task"
        indexes = [models.Index(fields=["status", "creator_id", "executor_id"])]
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('task', kwargs={'id': self.id})


class NoteChanal(models.TextChoices):
    TELEGRAMM = "telegramm", _("telegramm")


class Person(TimeStampMixin, UUINMixin):
    name = models.CharField(verbose_name=_('name'), max_length=255, unique=True)
    is_executer = models.BooleanField(verbose_name=_("is_executer"), null=False, default=False, db_index=True)
    # note_chanal = models.TextField(verbose_name=_("NoteChanal"), choices=NoteChanal.choices,
    # null=False, default="telegramm")
    # telegramm_id = models.CharField(verbose_name=_("telegram_id"), max_length=255, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "user"
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.name

