from django.contrib.auth.models import User
from django.db import models
from .managers import MildModeratedModelManager


class MildModeratedModel(models.Model):
    # user info
    created_by  = models.ForeignKey(User, null=True, editable=False, related_name='%(app_label)s_%(class)s_created')
    updated_by  = models.ForeignKey(User, null=True, editable=False, related_name='%(app_label)s_%(class)s_updated')
    approved_by = models.ForeignKey(User, null=True, editable=False, related_name='%(app_label)s_%(class)s_approved')

    # timestamp info
    created_at  = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at  = models.DateTimeField(auto_now=True, null=True, editable=False)
    approved_at = models.DateTimeField(auto_now=True, null=True, editable=False)

    # actual moderation flag
    is_public = models.BooleanField(default=False)

    notes = models.TextField(max_length=255, null=True, blank=True)

    # override the default manager
    objects = MildModeratedModelManager()

    class Meta:
        abstract = True


