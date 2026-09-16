from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..core.db import get_db
from ..core.security import verify_password, create_token
from ..models import User, ContentItem, Source, Skill, Assessment, LearningPlan, Feedback
from ..schemas import LoginIn, TokenOut, UserOut, ContentOut, AssessmentIn, FeedbackIn
from ..services.recommendations import stakeholder_feed, skill_gap_summary
from ..services.ingestion import ingest_source
from ..services.digests import build_digest
from .deps import current_user, admin_user

router = APIRouter(prefix="/api/v1")


@router.post("/auth/login", response_model=TokenOut)
def login(body: LoginIn, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == body.email))
    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(401, "Incorrect email or password")
    return TokenOut(access_token=create_token(user.email, user.role))


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(current_user)):
    return user


@router.get("/feed", response_model=list[ContentOut])
def feed(limit: int = Query(30, ge=1, le=100), db: Session = Depends(get_db), user: User = Depends(current_user)):
    return stakeholder_feed(db, user, limit)


@router.get("/skills")
def skills(db: Session = Depends(get_db), _: User = Depends(current_user)):
    return db.scalars(select(Skill).order_by(Skill.category, Skill.name)).all()


@router.put("/assessments")
def assess(body: AssessmentIn, db: Session = Depends(get_db), user: User = Depends(current_user)):
    if not db.get(Skill, body.skill_id):
        raise HTTPException(404, "Skill not found")
    row = db.scalar(select(Assessment).where(Assessment.user_id == user.id, Assessment.skill_id == body.skill_id))
    values = body.model_dump(mode="json")
    if row:
        for key, value in values.items(): setattr(row, key, value)
    else:
        row = Assessment(user_id=user.id, **values); db.add(row)
    db.commit()
    return {"status": "saved"}


@router.get("/skill-gaps")
def gaps(db: Session = Depends(get_db), user: User = Depends(current_user)):
    return skill_gap_summary(db, user.id)


@router.get("/learning-plans")
def plans(db: Session = Depends(get_db), user: User = Depends(current_user)):
    return db.scalars(select(LearningPlan).where(LearningPlan.user_id == user.id)).all()


@router.get("/digests/{cadence}")
def digest(cadence: str, db: Session = Depends(get_db), user: User = Depends(current_user)):
    try:
        return build_digest(db, user, cadence)
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc


@router.post("/feedback", status_code=201)
def feedback(body: FeedbackIn, db: Session = Depends(get_db), user: User = Depends(current_user)):
    db.add(Feedback(user_id=user.id, **body.model_dump())); db.commit()
    return {"status": "recorded"}


@router.post("/admin/sources/{source_id}/ingest")
def ingest(source_id: int, db: Session = Depends(get_db), _: User = Depends(admin_user)):
    source = db.get(Source, source_id)
    if not source: raise HTTPException(404, "Source not found")
    return {"created": ingest_source(db, source)}


@router.patch("/admin/content/{content_id}/approve")
def approve(content_id: int, db: Session = Depends(get_db), _: User = Depends(admin_user)):
    item = db.get(ContentItem, content_id)
    if not item: raise HTTPException(404, "Content not found")
    item.status = "approved"; db.commit()
    return {"status": "approved"}
