from moderation import moderation
from moderation.moderator import GenericModerator
from broadcasters.models import Broadcaster, BroadcasterAddress


class DefaultModerator(GenericModerator):
    auto_approve_for_staff = False

#moderation.register(Broadcaster, DefaultModerator)
#moderation.register(BroadcasterAddress, DefaultModerator)
