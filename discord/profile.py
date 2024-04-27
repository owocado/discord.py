"""
The MIT License (MIT)

Copyright (c) 2021-present Dolfies

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

from __future__ import annotations

from typing import TYPE_CHECKING, Collection, List, Optional

from . import utils
from .asset import Asset, AssetMixin
from .colour import Colour
from .connections import PartialConnection
from .enums import PremiumType, try_enum
from .flags import ApplicationFlags
from .member import Member
from .mixins import Hashable
from .permissions import Permissions
from .user import User

if TYPE_CHECKING:
    from datetime import datetime

    from .abc import Snowflake
    from .guild import Guild
    from .state import ConnectionState
    from .types.appinfo import (
        ApplicationInstallParams as ApplicationInstallParamsPayload,
    )
    from .types.emoji import Emoji as EmojiPayload
    from .types.profile import (
        MutualGuild as MutualGuildPayload,
        Profile as ProfilePayload,
        ProfileApplication as ProfileApplicationPayload,
        ProfileBadge as ProfileBadgePayload,
        ProfileMetadata as ProfileMetadata,
    )

__all__ = (
    'ApplicationInstallParams',
    'ApplicationProfile',
    'MutualGuild',
    'ProfileBadge',
    'MemberUserProfile',
    'Profile',
)


class ApplicationInstallParams:
    """Represents an application's authorization parameters.

    .. container:: operations

        .. describe:: str(x)

            Returns the authorization URL.

    Attributes
    ----------
    application_id: :class:`int`
        The ID of the application to be authorized.
    scopes: List[:class:`str`]
        The list of :ddocs:`OAuth2 scopes <topics/oauth2#shared-resources-oauth2-scopes>` to add the application with.
    permissions: :class:`Permissions`
        The permissions to grant to the added bot.
    """

    __slots__ = ('application_id', 'scopes', 'permissions')

    def __init__(
        self, application_id: int, *, scopes: Optional[Collection[str]] = None, permissions: Optional[Permissions] = None
    ):
        self.application_id: int = application_id
        self.scopes: List[str] = [scope for scope in scopes] if scopes else ['bot', 'applications.commands']
        self.permissions: Permissions = permissions or Permissions(0)

    @classmethod
    def from_application(cls, application: Snowflake, data: ApplicationInstallParamsPayload) -> ApplicationInstallParams:
        return cls(
            application.id,
            scopes=data.get('scopes', []),
            permissions=Permissions(int(data.get('permissions', 0))),
        )

    def __repr__(self) -> str:
        return f'<ApplicationInstallParams application_id={self.application_id} scopes={self.scopes!r} permissions={self.permissions!r}>'

    def __str__(self) -> str:
        return self.url

    @property
    def url(self) -> str:
        """:class:`str`: The URL to add the application with the parameters."""
        return utils.oauth_url(self.application_id, permissions=self.permissions, scopes=self.scopes)

    def to_dict(self) -> dict:
        return {
            'scopes': self.scopes,
            'permissions': self.permissions.value,
        }


class ApplicationProfile(Hashable):
    """Represents a Discord application profile.

    Attributes
    ------------
    id: :class:`int`
        The application's ID.
    verified: :class:`bool`
        Indicates if the application is verified.
    popular_application_command_ids: List[:class:`int`]
        A list of the IDs of the application's popular commands.
    primary_sku_id: Optional[:class:`int`]
        The application's primary SKU ID, if any.
        This can be an application's game SKU, subscription SKU, etc.
    custom_install_url: Optional[:class:`str`]
        The custom URL to use for authorizing the application, if specified.
    install_params: Optional[:class:`ApplicationInstallParams`]
        The parameters to use for authorizing the application, if specified.
    """

    __slots__ = (
        'id',
        'verified',
        'popular_application_command_ids',
        'primary_sku_id',
        '_flags',
        'custom_install_url',
        'install_params',
    )

    def __init__(self, data: ProfileApplicationPayload) -> None:
        self.id: int = int(data['id'])
        self.verified: bool = data.get('verified', False)
        popular_app_command_ids = data.get('popular_application_command_ids') or []
        self.popular_application_command_ids: List[int] = [int(id) for id in popular_app_command_ids]
        self.primary_sku_id: Optional[int] = utils._get_as_snowflake(data, 'primary_sku_id')
        self._flags: int = data.get('flags', 0)

        params = data.get('install_params')
        self.custom_install_url: Optional[str] = data.get('custom_install_url')
        self.install_params: Optional[ApplicationInstallParams] = (
            ApplicationInstallParams.from_application(self, params) if params else None
        )

    def __repr__(self) -> str:
        return f'<ApplicationProfile id={self.id} verified={self.verified}>'

    @property
    def flags(self) -> ApplicationFlags:
        """:class:`ApplicationFlags`: The flags of this application."""
        return ApplicationFlags._from_value(self._flags)

    @property
    def install_url(self) -> Optional[str]:
        """:class:`str`: The URL to install the application."""
        return self.custom_install_url or self.install_params.url if self.install_params else None

    @property
    def primary_sku_url(self) -> Optional[str]:
        """:class:`str`: The URL to the primary SKU of the application, if any."""
        if self.primary_sku_id:
            return f'https://discord.com/store/skus/{self.primary_sku_id}/unknown'


class MutualGuild(Hashable):
    """Represents a mutual guild between a user and the client user.

    Attributes
    ------------
    id: :class:`int`
        The guild's ID.
    nick: Optional[:class:`str`]
        The guild specific nickname of the user.
    """

    __slots__ = ('id', 'nick', '_state')

    def __init__(self, *, state: ConnectionState, data: MutualGuildPayload) -> None:
        self._state = state
        self.id: int = int(data['id'])
        self.nick: Optional[str] = data.get('nick')

    def __repr__(self) -> str:
        return f'<MutualGuild guild={self.guild!r} nick={self.nick!r}>'

    @property
    def guild(self) -> Guild:
        """:class:`Guild`: The guild that the user is mutual with."""
        return self._state._get_or_create_unavailable_guild(self.id)


class ProfileBadge(AssetMixin, Hashable):
    """Represents a Discord profile badge.

    .. container:: operations

        .. describe:: x == y

            Checks if two badges are equal.

        .. describe:: x != y

            Checks if two badges are not equal.

        .. describe:: hash(x)

            Returns the badge's hash.

        .. describe:: str(x)

            Returns the badge's description.

    .. versionadded:: 2.1

    Attributes
    ------------
    id: :class:`str`
        The badge's ID.
    description: :class:`str`
        The badge's description.
    link: Optional[:class:`str`]
        The link associated with the badge, if any.
    """

    __slots__ = ('id', 'description', 'link', '_icon', '_state')

    def __init__(self, *, state: ConnectionState, data: ProfileBadgePayload) -> None:
        self._state = state
        self.id: str = data['id']
        self.description: str = data.get('description', '')
        self.link: Optional[str] = data.get('link')
        self._icon: str = data['icon']

    def __repr__(self) -> str:
        return f'<ProfileBadge id={self.id!r} description={self.description!r}>'

    def __hash__(self) -> int:
        return hash(self.id)

    def __str__(self) -> str:
        return self.description

    @property
    def animated(self) -> bool:
        """:class:`bool`: Indicates if the badge is animated. Here for compatibility purposes."""
        return False

    @property
    def url(self) -> str:
        """:class:`str`: Returns the URL of the badge icon."""
        return f'{Asset.BASE}/badge-icons/{self._icon}.png'


class MemberUserProfile:

    __slots__ = (
        '_state',
        'guild_id',
        'bio',
        'pronouns',
        'theme_colors',
        'emoji',
        'user_id',
        '_accent_color',
        '_banner',
    )

    def __init__(self, *, state: ConnectionState, data: ProfileMetadata, user_id: int) -> None:
        self._state = state
        self.user_id = user_id
        self.guild_id: Optional[int] = utils._get_as_snowflake(data, 'guild_id')
        self.bio: str = data.get('bio')
        self._accent_color: Optional[int] = data.get('accent_color')
        self.theme_colors: List[Colour] = [Colour(v) for v in (data.get('theme_colors') or [])]
        self.pronouns: Optional[str] = data.get('pronouns')
        self._banner: Optional[str] = data.get('banner')
        self.emoji: Optional[EmojiPayload] = data.get('emoji')

    @property
    def accent_colour(self) -> Optional[Colour]:
        if self._accent_color is None:
            return None
        return Colour(self._accent_color)

    @property
    def banner(self) -> Optional[Asset]:
        if self._banner is None:
            return None
        if self.guild_id:
            return Asset._from_guild_banner(self._state, self.guild_id, self.user_id, self._banner)
        return Asset._from_user_banner(self._state, self.user_id, self._banner)


class Profile:

    __slots__ = (
        '_state',
        'user',
        'connections',
        'premium_since',
        'premium_type',
        'premium_guild_since',
        'user_profile',
        'badges',
        'guild_badges',
        'mutual_guilds',
        'member',
        'member_profile',
        'application',
        'legacy_username',
    )

    if TYPE_CHECKING:
        id: int
        bot: bool
        _state: ConnectionState

    def __init__(self, *, state: ConnectionState, data: ProfilePayload, user_id: int, guild_id: int) -> None:
        self._state = state
        self.user: User = User(state=state, data=data['user'])
        self.user_profile: Optional[MemberUserProfile] = None
        if user_profile := data.get('user_profile'):
            self.user_profile = MemberUserProfile(state=state, data=user_profile, user_id=user_id)
        self.member: Optional[Member] = None
        if member := data.get('guild_member'):
            member['user'] = data['user']  # type: ignore
            guild = state._get_or_create_unavailable_guild(guild_id)
            self.member = Member(data=member, state=state, guild=guild)
        self.member_profile: Optional[MemberUserProfile] = None
        if member_profile := data.get('guild_member_profile'):
            self.member_profile = MemberUserProfile(state=state, data=member_profile, user_id=user_id)
        self.premium_type: Optional[PremiumType] = (
            try_enum(PremiumType, data['premium_type']) if data.get('premium_type') else None
        )
        self.premium_since: Optional[datetime] = utils.parse_time(data['premium_since'])
        self.premium_guild_since: Optional[datetime] = utils.parse_time(data['premium_guild_since'])
        self.connections: List[PartialConnection] = [
            PartialConnection(d) for d in (data.get('connected_accounts') or [])
        ]
        self.badges: List[ProfileBadge] = [ProfileBadge(state=state, data=d) for d in (data.get('badges') or [])]
        mutual_guilds = data.get('mutual_guilds') or []
        self.mutual_guilds: List[MutualGuild] = [MutualGuild(state=state, data=d) for d in mutual_guilds]

        application = data.get('application')
        self.application: Optional[ApplicationProfile] = ApplicationProfile(data=application) if application else None
        self.legacy_username: Optional[str] = data.get('legacy_username')

