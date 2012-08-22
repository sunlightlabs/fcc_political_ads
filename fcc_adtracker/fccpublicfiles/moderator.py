from moderation import moderation
from moderation.moderator import GenericModerator
from fccpublicfiles.models import Person, Role, Organization, \
    PoliticalBuy, PoliticalSpot
from doccloud.models import Document


class DefaultModerator(GenericModerator):
    auto_approve_for_staff = False
    notify_user = False
    notify_moderator = False

class PoliticalBuyModerator(DefaultModerator):
    fields_exclude = ['broadcasters']

moderation.register(Person, DefaultModerator)
moderation.register(Role, DefaultModerator)
moderation.register(Organization, DefaultModerator)
#moderation.register(Document, DefaultModerator)
moderation.register(PoliticalBuy, PoliticalBuyModerator)
moderation.register(PoliticalSpot, DefaultModerator)
