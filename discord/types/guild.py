"""
The MIT License (MIT)

Copyright (c) 2015-present Rapptz

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from typing import List, Literal, Optional, TypedDict
from typing_extensions import NotRequired

from .scheduled_event import GuildScheduledEvent
from .sticker import GuildSticker
from .snowflake import Snowflake
from .channel import GuildChannel, StageInstance
from .voice import GuildVoiceState
from .welcome_screen import WelcomeScreen
from .activity import PartialPresenceUpdate
from .role import Role
from .member import Member
from .emoji import Emoji
from .user import APIUser
from .threads import Thread
from .soundboard import SoundboardSound


class Ban(TypedDict):
    reason: Optional[str]
    user: APIUser


class UnavailableGuild(TypedDict):
    id: Snowflake
    unavailable: NotRequired[bool]


class IncidentData(TypedDict):
    invites_disabled_until: NotRequired[Optional[str]]
    dms_disabled_until: NotRequired[Optional[str]]


class ModeratorReporting(TypedDict):
    moderator_reporting_enabled: bool
    moderator_report_channel_id: str


class Profile(TypedDict):
    badge: Optional[str]
    tag: Optional[str]


DefaultMessageNotificationLevel = Literal[0, 1]
ExplicitContentFilterLevel = Literal[0, 1, 2]
MFALevel = Literal[0, 1]
VerificationLevel = Literal[0, 1, 2, 3, 4]
NSFWLevel = Literal[0, 1, 2, 3]
PremiumTier = Literal[0, 1, 2, 3]
GuildFeature = Literal[
    'ANIMATED_BANNER',
    'ANIMATED_ICON',
    'APPLICATION_COMMAND_PERMISSIONS_V2',
    'AUTO_MODERATION',
    'BANNER',
    'COMMUNITY',
    'CREATOR_MONETIZABLE_PROVISIONAL',
    'CREATOR_STORE_PAGE',
    'DEVELOPER_SUPPORT_SERVER',
    'DISCOVERABLE',
    'FEATURABLE',
    'INVITE_SPLASH',
    'INVITES_DISABLED',
    'MEMBER_VERIFICATION_GATE_ENABLED',
    'MONETIZATION_ENABLED',
    'MORE_EMOJI',
    'MORE_STICKERS',
    'NEWS',
    'PARTNERED',
    'PREVIEW_ENABLED',
    'ROLE_ICONS',
    'ROLE_SUBSCRIPTIONS_AVAILABLE_FOR_PURCHASE',
    'ROLE_SUBSCRIPTIONS_ENABLED',
    'TICKETED_EVENTS_ENABLED',
    'VANITY_URL',
    'VERIFIED',
    'VIP_REGIONS',
    'WELCOME_SCREEN_ENABLED',
    'ENHANCED_ROLE_COLORS',
    'RAID_ALERTS_DISABLED',
    'SOUNDBOARD',
    'MORE_SOUNDBOARD',
    'GUESTS_ENABLED',
    'GUILD_TAGS',
    'PREMIUM_TIER_3_OVERRIDE',
    'CLAN_DISCOVERY_DISABLED',
    'CLAN',
]


class _BaseGuildPreview(UnavailableGuild):
    name: str
    icon: Optional[str]
    splash: Optional[str]
    discovery_splash: Optional[str]
    emojis: List[Emoji]
    stickers: List[GuildSticker]
    features: List[GuildFeature]
    description: Optional[str]
    incidents_data: Optional[IncidentData]
    sticker_count: Optional[int]
    approximate_member_count: int
    approximate_presence_count: int
    profile: NotRequired[Profile]


class _GuildPreviewUnique(TypedDict):
    emoji_count: Optional[int]
    sticker_count: Optional[int]
    primary_category_id: Optional[int]
    discovery_profile_features: NotRequired[List[GuildFeature]]
    badge_hash: NotRequired[Optional[str]]
    banner_hash: NotRequired[Optional[str]]
    play_style: NotRequired[int]
    game_application_ids: NotRequired[List[Snowflake]]
    search_terms: NotRequired[List[str]]
    member_count: NotRequired[int]


class GuildPreview(_BaseGuildPreview, _GuildPreviewUnique): ...


class Guild(_BaseGuildPreview):
    owner_id: Snowflake
    region: str
    afk_channel_id: Optional[Snowflake]
    afk_timeout: int
    verification_level: VerificationLevel
    default_message_notifications: DefaultMessageNotificationLevel
    explicit_content_filter: ExplicitContentFilterLevel
    roles: List[Role]
    mfa_level: MFALevel
    nsfw_level: NSFWLevel
    application_id: Optional[Snowflake]
    system_channel_id: Optional[Snowflake]
    system_channel_flags: int
    rules_channel_id: Optional[Snowflake]
    vanity_url_code: Optional[str]
    banner: Optional[str]
    premium_tier: PremiumTier
    preferred_locale: str
    public_updates_channel_id: Optional[Snowflake]
    stickers: List[GuildSticker]
    stage_instances: List[StageInstance]
    guild_scheduled_events: List[GuildScheduledEvent]
    icon_hash: NotRequired[Optional[str]]
    owner: NotRequired[bool]
    permissions: NotRequired[str]
    widget_enabled: NotRequired[bool]
    widget_channel_id: NotRequired[Optional[Snowflake]]
    joined_at: NotRequired[Optional[str]]
    large: NotRequired[bool]
    member_count: NotRequired[int]
    voice_states: NotRequired[List[GuildVoiceState]]
    members: NotRequired[List[Member]]
    channels: NotRequired[List[GuildChannel]]
    presences: NotRequired[List[PartialPresenceUpdate]]
    threads: NotRequired[List[Thread]]
    max_presences: NotRequired[Optional[int]]
    max_members: NotRequired[int]
    premium_subscription_count: NotRequired[int]
    max_video_channel_users: NotRequired[int]
    max_stage_video_channel_users: NotRequired[int]
    soundboard_sounds: NotRequired[List[SoundboardSound]]
    home_header: Optional[str]
    moderator_reporting: NotRequired[Optional[ModeratorReporting]]
    embed_enabled: NotRequired[bool]
    embed_channel_id: NotRequired[Optional[Snowflake]]
    owner_configured_content_level: NotRequired[int]
    premium_progress_bar_enabled_user_updated_at: NotRequired[Optional[str]]


class InviteGuild(TypedDict, total=False):
    id: Snowflake
    name: str
    splash: Optional[str]
    banner: Optional[str]
    description: Optional[str]
    icon: Optional[str]
    features: List[GuildFeature]
    verification_level: int
    vanity_url_code: Optional[str]
    nsfw_level: int
    nsfw: bool
    premium_subscription_count: int
    premium_tier: int
    welcome_screen: WelcomeScreen
    owner_configured_content_level: NotRequired[int]


class GuildWithCounts(Guild, _GuildPreviewUnique): ...


class GuildPrune(TypedDict):
    pruned: Optional[int]


class GuildMFALevel(TypedDict):
    level: MFALevel


class ChannelPositionUpdate(TypedDict):
    id: Snowflake
    position: Optional[int]
    lock_permissions: NotRequired[Optional[bool]]
    parent_id: NotRequired[Optional[Snowflake]]


class _RolePositionRequired(TypedDict):
    id: Snowflake


class RolePositionUpdate(_RolePositionRequired, total=False):
    position: Optional[Snowflake]


class DiscoveryCategory(TypedDict):
    id: int
    is_primary: bool
    name: str


class BulkBanUserResponse(TypedDict):
    banned_users: Optional[List[Snowflake]]
    failed_users: Optional[List[Snowflake]]


class GuildProfile(TypedDict):
    id: Snowflake
    name: str
    tag: str
    icon_hash: str | None
    member_count: int
    online_count: int
    description: str | None
    banner_hash: str | None
    game_application_ids: list[Snowflake]
    game_activity: dict[str, str]
    badge: int
    badge_color_primary: str
    badge_color_secondary: str
    badge_hash: str | None
    traits: list[str]
    features: list[str]
    visibility: int
