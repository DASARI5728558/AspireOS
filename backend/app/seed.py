import json
from pathlib import Path
from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import User, Source, Skill, ContentItem, Assessment, LearningPlan
from .core.security import hash_password


def seed(db: Session):
    if db.scalar(select(User.id).limit(1)):
        return
    user = User(email="learner@aspireos.example.com", password_hash=hash_password("ChangeMe123!"), name="Demo Learner",
                role="learner", locale="en", interests=["digital-economy", "ai", "employability"])
    admin = User(email="admin@aspireos.example.com", password_hash=hash_password("ChangeMe123!"), name="AspireOS Admin", role="admin")
    db.add_all([user, admin]); db.flush()
    source_path = Path("/app/infra/sources.json")
    if not source_path.exists(): source_path = Path(__file__).parents[2] / "infra" / "sources.json"
    records = json.loads(source_path.read_text()) if source_path.exists() else []
    sources = []
    for record in records:
        source = Source(**record); db.add(source); sources.append(source)
    db.flush()
    skills = [
        Skill(code="DIG-LIT", name="Digital Literacy", category="Foundational", description="Safe and effective use of digital systems"),
        Skill(code="DATA-LIT", name="Data Literacy", category="Analytical", description="Interpret, question and communicate with data"),
        Skill(code="AI-LIT", name="AI Literacy", category="Emerging Technology", description="Use and govern AI responsibly"),
        Skill(code="CRI-THK", name="Critical Thinking", category="Cognitive", description="Evaluate evidence and competing claims"),
        Skill(code="COM-01", name="Professional Communication", category="Human", description="Communicate clearly across stakeholders"),
    ]
    db.add_all(skills); db.flush()
    for skill, current, target in [(skills[0], 3, 4), (skills[1], 2, 4), (skills[2], 1.5, 4), (skills[3], 3, 4)]:
        db.add(Assessment(user_id=user.id, skill_id=skill.id, current_level=current, target_level=target, confidence=.65))
    db.add(LearningPlan(user_id=user.id, title="AI and Data Decision Readiness", milestones=[
        {"title": "Complete baseline assessment", "status": "done"},
        {"title": "Study responsible AI resources", "status": "in_progress"},
        {"title": "Submit evidence project", "status": "todo"}], progress=33))
    if sources:
        db.add(ContentItem(source_id=sources[0].id, canonical_url="https://www.worldbank.org/en/publication/wdr2021",
                           title="World Development Report 2021: Data for Better Lives",
                           abstract="A public institutional resource on the development value, governance and safeguards of data.",
                           topics=["data", "digital-economy", "governance"], stakeholder_roles=["learner", "faculty", "government", "institution"],
                           resource_type="report", licence="link-only", status="approved"))
    db.commit()
