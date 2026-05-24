from __future__ import annotations

import re
from html import escape
from typing import TYPE_CHECKING

from sqlalchemy import select

from src.core.hooks import hooks
from src.database.models.plugin import InstalledPlugin

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.core.registry import ComponentRegistry

PLUGIN_NAME = "plg_content_autolink"


async def _settings(db: "AsyncSession" | None) -> dict[str, object]:
    if db is None:
        return {}
    plugin = (
        await db.execute(select(InstalledPlugin).where(InstalledPlugin.name == PLUGIN_NAME))
    ).scalar_one_or_none()
    return plugin.settings if plugin and isinstance(plugin.settings, dict) else {}


def _linked_once(content: str, term: str, url: str) -> str:
    clean_term = term.strip()
    clean_url = url.strip()
    if not clean_term or not clean_url:
        return content
    pattern = re.compile(rf"(?<![>/])\b({re.escape(clean_term)})\b", re.IGNORECASE)
    href = escape(clean_url, quote=True)
    return pattern.sub(rf'<a href="{href}">\1</a>', content, count=1)


async def autolink_article(*, article: object, db: "AsyncSession" | None = None, **_: object) -> None:
    settings = await _settings(db)
    terms = settings.get("terms")
    if not isinstance(terms, dict):
        return
    content = str(getattr(article, "content", "") or "")
    updated = content
    for term, url in terms.items():
        updated = _linked_once(updated, str(term), str(url))
    if updated == content:
        return
    setattr(article, "content", updated)
    if db is not None:
        await db.commit()


def setup(registry: "ComponentRegistry") -> None:
    hooks.on("content.article.saved", autolink_article)
