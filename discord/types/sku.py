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

from typing import TypedDict, Optional, Literal
from typing_extensions import NotRequired

from .appinfo import PartialAppInfo


class SKU(TypedDict):
    id: str
    type: int
    application_id: str
    name: str
    slug: str
    flags: int


class Entitlement(TypedDict):
    id: str
    sku_id: str
    application_id: str
    user_id: Optional[str]
    type: int
    deleted: bool
    starts_at: NotRequired[str]
    ends_at: NotRequired[str]
    guild_id: NotRequired[str]
    consumed: NotRequired[bool]


class Price(TypedDict):
    amount: int
    currency: str
    currency_exponent: int
    premium: Optional[dict[str, dict[str, int]]]


class PublicSKU(SKU):
    product_line: int
    dependent_sku_id: Optional[int]
    manifest_labels: Optional[str]
    access_type: int
    features: list[str]
    release_date: Optional[str]
    premium: bool
    application: PartialAppInfo
    show_age_gate: bool
    price: Price


class PublishedSKU(TypedDict):
    id: str
    summary: Optional[str]
    sku: PublicSKU
    description: Optional[str]
    benefits: list[str]


EntitlementOwnerType = Literal[1, 2]
