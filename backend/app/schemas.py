from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, HttpUrl, ConfigDict


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    name: str
    role: str
    locale: str


class ContentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    abstract: str
    canonical_url: str
    topics: list[str]
    resource_type: str
    language: str
    licence: str
    published_at: datetime | None


class AssessmentIn(BaseModel):
    skill_id: int
    current_level: float = Field(ge=0, le=5)
    target_level: float = Field(ge=0, le=5)
    confidence: float = Field(default=0.5, ge=0, le=1)
    evidence_url: HttpUrl | None = None


class FeedbackIn(BaseModel):
    content_id: int | None = None
    useful: bool
    note: str = Field(default="", max_length=2000)

