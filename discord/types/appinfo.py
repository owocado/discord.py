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

from typing import TypedDict, List, Optional, Dict, Literal, Any
from typing_extensions import NotRequired

from .user import PartialUser, User
from .team import Team
from .snowflake import Snowflake
from .emoji import Emoji


class InstallParams(TypedDict):
    scopes: List[str]
    permissions: str


class BaseAppInfo(TypedDict):
    id: Snowflake
    name: str
    verify_key: str
    icon: Optional[str]
    summary: str
    description: str
    flags: int
    approximate_user_install_count: NotRequired[int]
    cover_image: NotRequired[str]
    terms_of_service_url: NotRequired[str]
    privacy_policy_url: NotRequired[str]
    rpc_origins: NotRequired[List[str]]
    interactions_endpoint_url: NotRequired[Optional[str]]
    redirect_uris: NotRequired[List[str]]
    role_connections_verification_url: NotRequired[Optional[str]]
    install_params: NotRequired[InstallParams]


class AppInfo(BaseAppInfo):
    owner: User
    bot_public: bool
    bot_require_code_grant: bool
    bot: NotRequired[User]
    team: NotRequired[Team]
    guild_id: NotRequired[Snowflake]
    primary_sku_id: NotRequired[Snowflake]
    slug: NotRequired[str]
    hook: NotRequired[bool]
    max_participants: NotRequired[int]
    tags: NotRequired[List[str]]
    custom_install_url: NotRequired[str]


class ApplicationIntegrationTypeConfiguration(TypedDict, total=False):
    oauth2_install_params: InstallParams


class PartialAppInfo(BaseAppInfo, total=False):
    hook: bool
    approximate_guild_count: int
    integration_types_config: NotRequired[
        Dict[Literal['0', '1'], ApplicationIntegrationTypeConfiguration]
    ]
    type: Optional[int]
    guild_id: Optional[Snowflake]
    storefront_available: bool
    bot_public: bool
    bot_require_code_grant: bool
    max_participants: Optional[int]
    embedded_activity_config: Dict[str, Any] # TODO
    integration_type: int



class GatewayAppInfo(TypedDict):
    id: Snowflake
    flags: int


class ListAppEmojis(TypedDict):
    items: List[Emoji]


class ApplicationInstallParams(TypedDict):
    scopes: List[str]
    permissions: int


class BaseApplication(TypedDict):
    id: Snowflake
    name: str
    description: str
    icon: Optional[str]
    cover_image: NotRequired[Optional[str]]
    type: Optional[int]
    primary_sku_id: NotRequired[Snowflake]
    summary: NotRequired[Literal['']]


class RoleConnectionApplication(BaseApplication):
    bot: NotRequired[PartialUser]


class RoleConnectionMetadata(TypedDict):
    type: Literal[1, 2, 3, 4, 5, 6, 7, 8]
    key: str
    name: str
    description: str
    name_localizations: NotRequired[Dict[str, str]]
    description_localizations: NotRequired[Dict[str, str]]


class PartialRoleConnection(TypedDict):
    platform_name: Optional[str]
    platform_username: Optional[str]
    metadata: Dict[str, str]


class RoleConnection(PartialRoleConnection):
    application: RoleConnectionApplication
    application_metadata: List[RoleConnectionMetadata]


class AppRPC(TypedDict):
    id: Snowflake
    name: str
    icon: Optional[str]
    description: str
    summary: str
    type: Optional[int]
    is_monetized: bool
    hook: bool
    storefront_available: bool
    integration_types_config: Dict[Literal["0", "1"], Dict[str, str]]
    verify_key: str
    flags: int
