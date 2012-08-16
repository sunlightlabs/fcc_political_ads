from moderation import moderation
from moderation.moderator import GenericModerator
from fccpublicfiles.models import Person, Role, Organization, \
    PublicDocument, PoliticalBuy, PoliticalSpot


class DefaultModerator(GenericModerator):
    auto_approve_for_staff = False

moderation.register(Person, DefaultModerator)
moderation.register(Role, DefaultModerator)
moderation.register(Organization, DefaultModerator)
moderation.register(PublicDocument, DefaultModerator)
moderation.register(PoliticalBuy, DefaultModerator)
moderation.register(PoliticalSpot, DefaultModerator)
