""" Everything must be public by default! 
In spite of the class name below we are not choosing what content goes up
"""

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from mildmoderator.managers import MildModeratedModelManager
from django.contrib import messages


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
    is_public = models.BooleanField(default=True)

    notes = models.TextField(max_length=255, null=True, blank=True)

    # override the default manager
    objects = MildModeratedModelManager()

    class Meta:
        abstract = True

    def save(self, user, *args, **kwargs):
        # people shouldn't be setting PK's manually, otherwise this check will not work
        # FWIW, Django uses it as its internal check, too.

        # option 1: no pk, just set created_by

        # option 2: pk, set updated_by

        # option 3: user has permission to approve
        # and is_public is True when it was False before, set approved_by

        klass = self.__class__

        if not self.pk:
            self.created_by = user
            #can_autoapprove = klass.objects.can_be_autoapproved_by_user(user)
            #self.is_public = can_autoapprove
            self.is_public = True
        else:
            self.updated_by = user

            #if klass.objects.can_be_approved_by_user(user):
            #    if (not self._is_public_old) and self.is_public: # Field has changed to True
            #        self.approved_by = user
            #else:
            #    self.is_public = False

        return super(MildModeratedModel, self).save(*args, **kwargs)
        
    def save_no_update(self):
        this_user = self.updated_by
        self.save(this_user)




