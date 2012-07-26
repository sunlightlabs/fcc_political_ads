from moderation import moderation
from fccpublicfiles.models import Address, Person, Role, Organization, \
    PublicDocument, PoliticalBuy, PoliticalSpot

moderation.register(Address)
moderation.register(Person)
moderation.register(Role)
moderation.register(Organization)
moderation.register(PublicDocument)
moderation.register(PoliticalBuy)
moderation.register(PoliticalSpot)
