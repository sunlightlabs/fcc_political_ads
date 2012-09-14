from django.db import models
from django.db.models import Q


class ModeratedModelManager(models.Manager):
    def for_user(self, user=None):
        return super(ModeratedModelManager, self).get_query_set().filter(
            Q( 
                Q(is_public=True) |\
                Q(updated_by=user) |\
                Q(updated_by__isnull=True, created_by=user)
            )
        )

    def public(self):
        return super(ModeratedModelManager, self).get_query_set().filter(
            is_public=True
        )

        
        
