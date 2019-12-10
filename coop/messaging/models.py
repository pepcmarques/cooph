from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField

from coop.accounts.models import User

from enum import Enum


class MessageChoice(Enum):   # A subclass of Enum
    CREATE_COOP = "Create Cooperative Housing"

    @classmethod
    def choices(cls):
        return [(key.name, key.value) for key in cls]


class Message(models.Model):
    message_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_from')
    message_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_to')
    request = models.CharField(max_length=15, choices=MessageChoice.choices())
    note = models.CharField(max_length=255, unique=False, null=True)
    created = CreationDateTimeField(_('created'))
    modified = ModificationDateTimeField(_('modified'))

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.request
