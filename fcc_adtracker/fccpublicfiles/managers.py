from django.db import models
from django.db.models import Q

import random


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


class PoliticalDocStatusManager(models.Manager):
    """PoliticalDocStatusManager provides methods for querying PoliticalBuys for 'completedness'. Yeah."""

    def non_adbuy_docs(self):
        qs = super(PoliticalDocStatusManager, self).get_query_set()
        return qs.filter(
            Q(is_invoice=True) | Q(is_invalid=True)
        )

    def has_total_spent_raw(self):
        qs = super(PoliticalDocStatusManager, self).get_query_set()
        return qs.filter(
            Q(total_spent_raw__isnull=False) | Q(total_spent_raw__gt=0)
        )

    def needs_entry(self, **kwargs):
        '''A list of PoliticalBuys that aren't invoices or invalid docs, or are already complete'''
        qs = super(PoliticalDocStatusManager, self).get_query_set()
        dma_id_filter = kwargs.get('dma_id_filter', None)
        if dma_id_filter:
            qs = qs.filter(dma_id__in=dma_id_filter)
        return qs.exclude(id__in=self.has_total_spent_raw()).exclude(id__in=self.non_adbuy_docs())

    def get_one_that_needs_entry(self, **kwargs):
        dma_id_filter = kwargs.get('dma_id_filter', None)
        qs = self.needs_entry(dma_id_filter=dma_id_filter)
        cnt = qs.count()
        rnd = random.randint(0, cnt - 1)

        return qs[rnd]
