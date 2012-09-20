from django.db import models
from django.db.models import Q


class MildModeratedModelManager(models.Manager):
    def contribute_to_class(self, model, name):
        super(MildModeratedModelManager, self).contribute_to_class(model, name)

        self.bind_post_init_signal(model)

    def bind_post_init_signal(self, model):
        models.signals.post_init.connect(self.save_is_public_flag, model)

    def save_is_public_flag(self, sender, instance, **kwargs):
        instance._is_public_old = instance.is_public

    def for_user(self, user):
        return super(MildModeratedModelManager, self).get_query_set().filter(
            Q(
                Q(is_public=True) |\
                Q(updated_by=user) |\
                Q(updated_by__isnull=True, created_by=user)
            )
        )

    def public(self):
        return super(MildModeratedModelManager, self).get_query_set().filter(
            is_public=True
        )

    def can_be_approved_by_user(self, user):
        return user.is_superuser \
                or user.groups.filter(name='Professionals').count()

    def can_be_autoapproved_by_user(self, user):
        return self.can_be_approved_by_user(user)

    def create(self, user, **kwargs):
        obj = self.model(**kwargs)
        self._for_write = True
        obj.save(user, force_insert=True, using=self.db)
        return obj
