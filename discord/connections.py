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

from typing import TYPE_CHECKING, Any, Dict, Optional

from .enums import ConnectionType, try_enum

if TYPE_CHECKING:
    from .types.user import PartialConnection as PartialConnectionPayload

__all__ = (
    'PartialConnection',
)


class PartialConnection:
    """Represents a partial Discord profile connection.

    This is the info you get for other users' connections.

    .. versionadded:: 2.0

    .. container:: operations

        .. describe:: x == y

            Checks if two connections are equal.

        .. describe:: x != y

            Checks if two connections are not equal.

        .. describe:: hash(x)

            Return the connection's hash.

        .. describe:: str(x)

            Returns the connection's name.

    Attributes
    ----------
    id: :class:`str`
        The connection's account ID.
    name: :class:`str`
        The connection's account name.
    type: :class:`ConnectionType`
        The connection service type (e.g. youtube, twitch, etc.).
    verified: :class:`bool`
        Whether the connection is verified.
    visible: :class:`bool`
        Whether the connection is visible on the user's profile.
    metadata: Optional[:class:`Metadata`]
        Various metadata about the connection.

        The contents of this are always subject to change.
    """

    __slots__ = ('id', 'name', 'type', 'verified', 'visible', 'metadata')

    def __init__(self, data: PartialConnectionPayload):
        self._update(data)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} id={self.id!r} name={self.name!r} type={self.type!r} visible={self.visible}>'

    def __hash__(self) -> int:
        return hash((self.type.value, self.id))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, PartialConnection):
            return self.id == other.id and self.name == other.name
        return False

    def __ne__(self, other: object) -> bool:
        if isinstance(other, PartialConnection):
            return self.id != other.id or self.name != other.name
        return True

    def _update(self, data: PartialConnectionPayload):
        self.id: str = data['id']
        self.name: str = data['name']
        self.type: ConnectionType = try_enum(ConnectionType, data['type'])
        self.verified: bool = data['verified']
        self.visible: bool = True  # If we have a partial connection, it's visible

        self.metadata: Dict[str, Any] = data.get('metadata', {})

    @property
    def url(self) -> Optional[str]:
        """Optional[:class:`str`]: Returns a URL linking to the connection's profile, if available."""
        if self.type == ConnectionType.twitch:
            return f'https://www.twitch.tv/{self.name}'
        elif self.type == ConnectionType.youtube:
            return f'https://www.youtube.com/channel/{self.id}'
        elif self.type == ConnectionType.steam:
            return f'https://steamcommunity.com/profiles/{self.id}'
        elif self.type == ConnectionType.reddit:
            return f'https://www.reddit.com/u/{self.name}'
        elif self.type == ConnectionType.twitter:
            return f'https://twitter.com/{self.name}'
        elif self.type == ConnectionType.spotify:
            return f'https://open.spotify.com/user/{self.id}'
        elif self.type == ConnectionType.xbox:
            xbox_page = 'https://account.xbox.com/en-US/Profile'
            return self.name if ' ' in self.name else f'{xbox_page}?Gamertag={self.name}'
        elif self.type == ConnectionType.github:
            return f'https://github.com/{self.name}'
        elif self.type == ConnectionType.tiktok:
            return f'https://tiktok.com/@{self.name}'
        elif self.type == ConnectionType.ebay:
            return f'https://www.ebay.com/usr/{self.name}'
        elif self.type == ConnectionType.instagram:
            return f'https://www.instagram.com/{self.name}'
        elif self.type == ConnectionType.playstation:
            return f'https://psnprofiles.com/{self.name}'
        elif self.type == ConnectionType.domain:
            return f'https://{self.name}'
        elif self.type == ConnectionType.roblox:
            return f'https://www.roblox.com/users/{self.id}/profile'
        else:
            return None

    @property
    def hyperlink(self) -> str:
        return f'[{self.name or '\u200b'}]({self.url})' if self.url and self.url.startswith('https') else self.name

