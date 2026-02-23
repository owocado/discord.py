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

from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import msgspec
from msgspec.structs import asdict

from .asset import Asset
from .utils import snowflake_time, _get_as_snowflake
from .enums import DisplayNameEffect, DisplayNameFont, try_enum

if TYPE_CHECKING:
    from datetime import datetime
    from typing_extensions import Self

    from .state import ConnectionState
    from .types.user import (
        AvatarDecorationData,
        PrimaryGuild as PrimaryGuildPayload,
        DisplayNameStyle as DisplayNameStylePayload,
        UserCollectibles as CollectiblePayload,
    )

# fmt: off
__all__ = (
    'PrimaryGuild',
    'AvatarDecoration',
    'NamePlate',
)
# fmt: on


class _PrimaryGuild:
    """Represents the primary guild identity of a :class:`User`

    .. versionadded:: 2.6

    Attributes
    -----------
    id: Optional[:class:`int`]
        The ID of the user's primary guild, if any.
    tag: Optional[:class:`str`]
        The primary guild's tag.
    identity_enabled: Optional[:class:`bool`]
        Whether the user has their primary guild publicly displayed.
        If ``None``, the user has a public guild but has not reaffirmed the guild identity after a change.

        .. warning::

            Users can have their primary guild publicly displayed while still having an :attr:`id` of ``None``.
            Be careful when checking this attribute!
    """

    __slots__ = ('id', 'identity_enabled', 'tag', '_badge', '_state')

    def __init__(self, *, state: ConnectionState, data: PrimaryGuildPayload) -> None:
        self._state = state
        self._update(data)

    def _update(self, data: PrimaryGuildPayload):
        self.id = _get_as_snowflake(data, 'identity_guild_id')
        self.identity_enabled = data['identity_enabled']
        self.tag = data.get('tag', None)
        self._badge = data.get('badge')

    @property
    def badge(self) -> Optional[Asset]:
        """Optional[:class:`Asset`]: Returns the primary guild's asset"""
        if self._badge is not None and self.id is not None:
            return Asset._from_primary_guild(self._state, self.id, self._badge)
        return None

    @property
    def created_at(self) -> Optional[datetime]:
        """Optional[:class:`datetime.datetime`]: Returns the primary guild's creation time in UTC."""
        if self.id is not None:
            return snowflake_time(self.id)
        return None

    @classmethod
    def _default(cls, state: ConnectionState) -> Self:
        payload: PrimaryGuildPayload = {'identity_enabled': False}  # type: ignore
        return cls(state=state, data=payload)

    def __repr__(self) -> str:
        return f'<PrimaryGuild id={self.id} identity_enabled={self.identity_enabled} tag={self.tag!r}>'


class PrimaryGuild(msgspec.Struct, kw_only=True):
    identity_guild_id: str | None = None
    identity_enabled: bool | None = None
    tag: str | None = None
    badge: str | None = None

    @classmethod
    def _default(cls, **kwargs):
        return cls(**kwargs)

    @property
    def guild_id(self) -> int | None:
        return int(self.identity_guild_id) if self.identity_guild_id else None

    @property
    def enabled(self) -> bool | None:
        return self.identity_enabled

    def get_badge(self, state: ConnectionState) -> Asset | None:
        if self.guild_id is not None and self.badge is not None:
            return Asset._from_primary_guild(state, self.guild_id, self.badge)
        return None

    def is_null(self):
        return self.identity_guild_id is None and self.identity_enabled is None and self.tag is None and self.badge is None

    def to_dict(self) -> PrimaryGuildPayload:
        return asdict(self)  # pyright: ignore

    def _update(self, obj: PrimaryGuild | None) -> Self:
        self.identity_guild_id = obj.identity_guild_id if obj is not None else None
        self.identity_enabled = obj.identity_enabled if obj is not None else None
        self.tag = obj.tag if obj is not None else None
        self.badge = obj.badge if obj is not None else None
        return self


class AvatarDecoration(msgspec.Struct, kw_only=True):
    asset: str
    sku_id: str | None = None
    expires_at: int | None = None

    @classmethod
    def from_data(cls, data: AvatarDecorationData | None):
        return cls(**data) if data else None

    @property
    def shop_url(self) -> str:
        """The URL of the avatar decoration asset."""
        return f'https://discord.com/shop#itemSkuId={self.sku_id}'

    @property
    def _sku_id(self):
        return int(self.sku_id) if self.sku_id else None

    def to_dict(self) -> AvatarDecorationData:
        return asdict(self)  # pyright: ignore

    def _update(self, obj: AvatarDecoration | None):
        self.asset = obj.asset if obj is not None else ''
        self.sku_id = obj.sku_id if obj is not None else None
        self.expires_at = obj.expires_at if obj is not None else None
        return self


class NamePlate(msgspec.Struct, kw_only=True):
    asset: str
    label: str
    palette: str
    sku_id: str | None = None
    expires_at: int | None = None

    @property
    def shop_url(self) -> str:
        """The URL of the avatar decoration asset."""
        return f'https://discord.com/shop#itemSkuId={self.sku_id}'

    def _update(self, obj: NamePlate | None):
        self.asset = obj.asset if obj is not None else ''
        self.label = obj.label if obj is not None else ''
        self.palette = obj.palette if obj is not None else ''
        self.sku_id = obj.sku_id if obj is not None else None
        self.expires_at = obj.expires_at if obj is not None else None
        return self

    def to_dict(self) -> CollectiblePayload:
        return {'nameplate': asdict(self)}  # pyright: ignore


class UserCollectible(msgspec.Struct, kw_only=True):
    nameplate: NamePlate

    def to_dict(self) -> CollectiblePayload:
        return asdict(self)  # pyright: ignore

    def _update(self, obj: UserCollectible | None):
        if obj is None:
            self.nameplate = None
            return self
        if self.nameplate:
            self.nameplate._update(obj.nameplate)
        return self


class DisplayNameStyle(msgspec.Struct, kw_only=True):
    font_id: int
    effect_id: int
    colors: list[int] = msgspec.field(default_factory=list)

    @property
    def effect(self):
        return try_enum(DisplayNameEffect, self.effect_id)

    @property
    def font(self):
        return try_enum(DisplayNameFont, self.font_id)

    def to_dict(self) -> DisplayNameStylePayload:
        return asdict(self)  # pyright: ignore
