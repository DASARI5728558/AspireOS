from sqlalchemy import select
from sqlalchemy.orm import Session
from ..models import ContentItem, User, Assessment


def stakeholder_feed(db: Session, user: User, limit: int = 30):
    items = db.scalars(select(ContentItem).where(ContentItem.status == "approved").order_by(ContentItem.published_at.desc()).limit(200)).all()
    interests = set(user.interests or [])
    role = user.role

    def score(item):
        topic_overlap = len(interests.intersection(item.topics or []))
        role_match = 1 if role in (item.stakeholder_roles or []) else 0
        language_match = 1 if item.language in {user.locale, "en"} else 0
        return 3 * role_match + 2 * topic_overlap + language_match

    return sorted(items, key=score, reverse=True)[:limit]


def skill_gap_summary(db: Session, user_id: int):
    rows = db.scalars(select(Assessment).where(Assessment.user_id == user_id)).all()
    return [{"skill": a.skill.name, "current": a.current_level, "target": a.target_level,
             "gap": round(max(0, a.target_level - a.current_level), 2), "confidence": a.confidence}
            for a in sorted(rows, key=lambda x: x.target_level - x.current_level, reverse=True)]

