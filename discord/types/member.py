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

from typing import Optional, TypedDict, List, Literal
from .snowflake import SnowflakeList, Snowflake
from .user import User, AvatarDecorationData, Clan
from typing_extensions import NotRequired


class Nickname(TypedDict):
    nick: str


class PartialMember(TypedDict):
    roles: SnowflakeList
    joined_at: str
    deaf: bool
    mute: bool
    flags: int
    banner: Optional[str]
    bio: str


class Member(PartialMember, total=False):
    avatar: str
    user: User
    nick: str
    premium_since: Optional[str]
    pending: bool
    permissions: str
    communication_disabled_until: str
    banner: NotRequired[Optional[str]]
    avatar_decoration_data: NotRequired[AvatarDecorationData]
    unusual_dm_activity_until: Optional[str]
    clan: Optional[Clan]


class _OptionalMemberWithUser(PartialMember, total=False):
    avatar: str
    nick: str
    premium_since: Optional[str]
    pending: bool
    permissions: str
    communication_disabled_until: str
    avatar_decoration_data: NotRequired[AvatarDecorationData]
    unusual_dm_activity_until: Optional[str]
    clan: Optional[Clan]


class MemberWithUser(_OptionalMemberWithUser):
    user: User


class UserWithMember(User, total=False):
    member: _OptionalMemberWithUser


JoinType = Literal[0, 1, 2, 3, 4, 5, 6]


class MemberSearch(TypedDict):
    member: MemberWithUser
    source_invite_code: Optional[str]
    join_source_type: JoinType
    inviter_id: Optional[Snowflake]


class MemberSearchResults(TypedDict):
    guild_id: Snowflake
    members: List[MemberSearch]
    page_result_count: int
    total_result_count: int


class PrivateMember(MemberWithUser):
    bio: str
    banner: Optional[str]
    unusual_dm_activity_until: NotRequired[Optional[str]]
