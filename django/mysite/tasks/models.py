import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
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
    СОЗДАН = "создана"
    ВЫПОЛНЕН = "выполнена"
    ОТМЕНЕН = "отменена"


class StatusModel(TimeStampMixin, UUINMixin):
    title = models.CharField(verbose_name=_("status_title"), max_length=64, unique=True)

    class Meta:
        db_table = '"task"."status"'
        verbose_name = _("Status")
        verbose_name_plural = _("Statuses")

    def __str__(self):
        return self.title

    @classmethod
    def get_default_pk(cls):
        created_status = cls.objects.get(title="Создана")
        print("get status", created_status)
        return created_status.id

class Task(TimeStampMixin, UUINMixin):
    title = models.CharField(verbose_name=_('title'), max_length=255)
    note = models.TextField(verbose_name=_('note'), blank=True)
    is_visible = models.BooleanField(verbose_name=_('is_visible'), default=True)
    status = models.ForeignKey("StatusModel", verbose_name=_("Status"), on_delete=models.CASCADE,
                               related_name="status", default=StatusModel.get_default_pk)
    creator = models.ForeignKey("Person", verbose_name=_("creator"), on_delete=models.CASCADE,
                                related_name="creator")
    executor = models.ForeignKey("Person", verbose_name=_('executor'), on_delete=models.CASCADE,
                                 related_name="executor")

    class Meta:
        db_table = '"task"."task"'
        indexes = [models.Index(fields=["status", "creator_id", "executor_id"])]
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('task', kwargs={'id': self.id})


class NoteChanal(models.TextChoices):
    TELEGRAMM = "telegramm", _("telegramm")
    ABSENT = "absent", _("absent")


class Person(TimeStampMixin, UUINMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_executer = models.BooleanField(verbose_name=_("is_executer"), null=False, default=False, db_index=True)
    note_chanal = models.TextField(verbose_name=_("NoteChanal"), choices=NoteChanal.choices,
                                   null=True, default="telegramm")
    telegramm_id = models.CharField(verbose_name=_("telegram_id"), max_length=255, blank=True)

    class Meta:
        db_table = '"task"."person"'
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Person.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.person.save()
