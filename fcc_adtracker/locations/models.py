from django.db import models
from django.contrib.localflavor.us import us_states
from django.contrib.localflavor.us.models import USStateField


class Address(models.Model):
    address1 = models.CharField(blank=True, null=True, max_length=100)
    address2 = models.CharField(blank=True, null=True, max_length=100)
    city = models.CharField(max_length=50)
    state = USStateField()
    zipcode = models.CharField(blank=True, null=True, max_length=10)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)

    is_visible = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = u"Addresses"
        unique_together = ('address1', 'address2', 'city', 'state', 'zipcode')

    def _combined_address(self):
        address_bits = [self.city, self. state]
        for street in (self.address2, self.address1):
            if street != '':
                address_bits.insert(0, street)
        return u'{0} {1}'.format(u', '.join(address_bits), self.zipcode or u'')

    def combined_address():
        doc = "The combined_address property."

        def fget(self):
            return self._combined_address()
        return locals()
    combined_address = property(**combined_address())

    def __unicode__(self):
        return self.combined_address


class AddressLabel(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField()

    is_visible = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name



