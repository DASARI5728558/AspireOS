from datetime import datetime, timezone
from urllib.parse import urlparse
import feedparser
import httpx
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..models import Source, ContentItem


BLOCKED_HOSTS = {"localhost", "127.0.0.1", "0.0.0.0"}


def safe_public_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme == "https" and bool(parsed.hostname) and parsed.hostname not in BLOCKED_HOSTS and not parsed.hostname.endswith(".local")


def ingest_source(db: Session, source: Source) -> int:
    if not source.feed_url or not safe_public_url(source.feed_url):
        return 0
    response = httpx.get(source.feed_url, timeout=15, follow_redirects=True, headers={"User-Agent": "AspireOS-CapabilityHub/1.0"})
    response.raise_for_status()
    feed = feedparser.loads(response.content)
    count = 0
    for entry in feed.entries[:50]:
        link = entry.get("link", "")
        if not safe_public_url(link) or db.scalar(select(ContentItem.id).where(ContentItem.canonical_url == link)):
            continue
        tags = [t.get("term", "").lower() for t in entry.get("tags", []) if t.get("term")]
        published = None
        if entry.get("published_parsed"):
            published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
        db.add(ContentItem(source_id=source.id, canonical_url=link, title=entry.get("title", "Untitled")[:500],
                           abstract=entry.get("summary", "")[:4000], topics=tags, stakeholder_roles=[],
                           resource_type="update", licence="link-only", status="pending_review", published_at=published))
        count += 1
    db.commit()
    return count

