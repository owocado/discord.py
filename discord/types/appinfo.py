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

from typing import Literal, Dict, TypedDict, List, Optional
from typing_extensions import NotRequired

from .user import User, PartialUser
from .team import Team
from .snowflake import Snowflake
from .emoji import Emoji


class InstallParams(TypedDict):
    scopes: List[str]
    permissions: str


class AppIntegrationTypeConfig(TypedDict):
    oauth2_install_params: NotRequired[InstallParams]


class LinkedGame(TypedDict, total=False):
    id: Snowflake
    type: int
    application: PartialAppInfo


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
    linked_games: NotRequired[List[LinkedGame]]


class AppInfo(BaseAppInfo):
    owner: User
    bot_public: bool
    bot_require_code_grant: bool
    team: NotRequired[Team]
    guild_id: NotRequired[Snowflake]
    primary_sku_id: NotRequired[Snowflake]
    slug: NotRequired[str]
    hook: NotRequired[bool]
    max_participants: NotRequired[int]
    tags: NotRequired[List[str]]
    install_params: NotRequired[InstallParams]
    custom_install_url: NotRequired[str]
    integration_types_config: NotRequired[Dict[Literal['0', '1'], AppIntegrationTypeConfig]]
    bot: NotRequired[User]


class PartialAppInfo(BaseAppInfo, total=False):
    hook: bool
    max_participants: int
    approximate_guild_count: int
    type: Optional[Literal[1, 2, 3, 4]]
    is_monetized: bool
    is_verified: bool
    is_discoverable: bool
    splash: Optional[str]
    primary_sku_id: Snowflake
    third_party_skus: List[ThirdPartySKU]
    bot: PartialUser
    overlay: bool
    aliases: List[str]
    guild_id: Optional[Snowflake]
    executables: List[ApplicationExecutable]
    storefront_available: bool
    bot_public: bool
    bot_require_code_grant: bool
    integration_types_config: Dict[Literal['0', '1'], AppIntegrationTypeConfig]
    embedded_activity_config: EmbeddedActivity
    integration_type: Literal[0, 1, 2]
    assets: List[AppAsset]
    supplemental_game_data: GameSupplemental


class GatewayAppInfo(TypedDict):
    id: Snowflake
    flags: int


class ListAppEmojis(TypedDict):
    items: List[Emoji]


class AppAsset(TypedDict):
    id: Snowflake
    type: Literal[1, 2]
    name: str


class ThirdPartySKU(TypedDict):
    id: Snowflake
    sku: Snowflake
    distributor: Literal[
        'discord',  # Discord Store
        'steam',  # Steam
        'twitch',  # Twitch
        'uplay',  # Ubisoft Connect
        'battlenet',  # Battle.net
        'origin',  # Origin
        'gog',  # GOG.com
        'epic',  # Epic Games Store
        'google_play',  # Google Play Store
        'xbox',
        'igdb',
        'gop',  # Gameopedia
        'gdco',
        'playstation',  # PlayStation Store
    ]


class ApplicationExecutable(TypedDict):
    os: Literal['win32', 'darwin', 'linux']
    name: str
    is_launcher: bool


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
    integration_types_config: Dict[Literal['0', '1'], Dict[str, str]]
    verify_key: str
    flags: int


class Platform(TypedDict):
    label_type: Literal[0, 1, 2]
    label_until: Optional[str]
    release_phase: Literal['in_development', 'activities_team', 'employee_release', 'soft_launch', 'global_launch']


class ClientPlatformConfig(TypedDict):
    web: Platform
    ios: Platform
    android: Platform


class EmbeddedActivity(TypedDict):
    activity_preview_video_asset_id: Optional[Snowflake]
    supported_platforms: List[Literal['web', 'ios', 'android']]
    default_orientation_lock_state: Literal[1, 2, 3]
    tablet_default_orientation_lock_state: Literal[1, 2, 3]
    requires_age_gate: bool
    legacy_responsive_aspect_ratio: bool
    free_period_starts_at: Optional[str]
    free_period_ends_at: Optional[str]
    client_platform_config: ClientPlatformConfig
    shelf_rank: int
    has_csp_exception: bool
    displays_advertisements: bool


class GameWebsite(TypedDict):
    category: int
    url: str


class GameSupplemental(TypedDict):
    application_id: Snowflake
    name: str
    summary: Optional[str]
    summary_localized: Optional[str]
    cover_image_url: Optional[str]
    artwork_urls: List[str]
    screenshot_urls: List[str]
    themes: List[str]
    platforms: List[int]
    genres: List[int]
    first_release_date: str
    websites: List[GameWebsite]
    publisher_names: List[str]
    developer_names: List[str]


class DetectableApplication(TypedDict):
    aliases: list[str]
    cover_image_hash: str | None
    executables: List[ApplicationExecutable]
    hook: bool
    icon_hash: str | None
    id: Snowflake
    linked_applications: list[LinkedGame]
    name: str
    overlay: bool
    overlay_compatibility_hook: bool
    overlay_methods: int
    overlay_warn: bool
    themes: list[str]
    third_party_skus: list[ThirdPartySKU]

