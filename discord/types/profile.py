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

from typing import List, Optional, TypedDict
from typing_extensions import NotRequired

from .appinfo import ApplicationInstallParams, RoleConnection
from .emoji import Emoji
from .member import PrivateMember as ProfileMember
from .snowflake import Snowflake
from .user import APIUser, PartialConnection, PremiumType


class ProfileUser(APIUser):
    bio: str
    pronouns: Optional[str]


class ProfileMetadata(TypedDict):
    guild_id: NotRequired[int]
    bio: str
    banner: NotRequired[Optional[str]]
    emoji: Optional[Emoji]
    accent_color: NotRequired[Optional[int]]
    theme_colors: NotRequired[List[int]]
    pronouns: str


class MutualGuild(TypedDict):
    id: str
    nick: Optional[str]


class ProfileApplication(TypedDict):
    id: Snowflake
    verified: bool
    popular_application_command_ids: NotRequired[List[Snowflake]]
    primary_sku_id: NotRequired[Snowflake]
    flags: int
    custom_install_url: NotRequired[str]
    install_params: NotRequired[ApplicationInstallParams]


class ProfileBadge(TypedDict):
    id: str
    description: str
    icon: str
    link: NotRequired[str]


class Profile(TypedDict):
    user: ProfileUser
    connected_accounts: List[PartialConnection]
    premium_since: Optional[str]
    premium_type: Optional[PremiumType]
    premium_guild_since: Optional[str]
    user_profile: Optional[ProfileMetadata]
    badges: List[ProfileBadge]
    guild_badges: List[ProfileBadge]
    mutual_guilds: NotRequired[List[MutualGuild]]
    guild_member: NotRequired[ProfileMember]
    guild_member_profile: NotRequired[Optional[ProfileMetadata]]
    legacy_username: Optional[str]
    mutual_friends_count: NotRequired[int]
    application_role_connections: NotRequired[List[RoleConnection]]
    application: NotRequired[ProfileApplication]
