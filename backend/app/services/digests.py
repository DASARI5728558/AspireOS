from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from ..models import User
from .recommendations import stakeholder_feed, skill_gap_summary


WINDOWS = {"daily": 1, "weekly": 7, "monthly": 31}


def build_digest(db: Session, user: User, cadence: str) -> dict:
    if cadence not in WINDOWS:
        raise ValueError("cadence must be daily, weekly or monthly")
    since = datetime.now(timezone.utc) - timedelta(days=WINDOWS[cadence])
    items = [i for i in stakeholder_feed(db, user, 100) if not i.published_at or i.published_at >= since]
    return {
        "cadence": cadence,
        "stakeholder": user.role,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "updates": [{"title": i.title, "url": i.canonical_url, "topics": i.topics, "source": i.source.name} for i in items[:20]],
        "priority_skill_gaps": skill_gap_summary(db, user.id)[:5],
        "recommended_action": "Choose one priority update, complete its linked activity, and record evidence of application.",
    }

