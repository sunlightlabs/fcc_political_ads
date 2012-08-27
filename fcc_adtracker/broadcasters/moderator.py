from moderation import moderation
from moderation.moderator import GenericModerator
from broadcasters.models import Broadcaster, BroadcasterAddress


class DefaultModerator(GenericModerator):
    auto_approve_for_staff = False
    # Note: Since moderation is turned off for these objects, I didn't
    # add the is_visible columns to the broadcasters models.
    # If you turn moderation back on, you will need to make that change
    # to preserve performance.
    visibility_column = 'is_visible'

#moderation.register(Broadcaster, DefaultModerator)
#moderation.register(BroadcasterAddress, DefaultModerator)
