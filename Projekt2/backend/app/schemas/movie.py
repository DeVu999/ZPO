from datetime import datetime

from pydantic import BaseModel


class MovieOut(BaseModel):
    id: int
    title: str
    description: str
    genre: str
    created_at: datetime
    average_rating: float | None = None
    rating_count: int = 0

    model_config = {"from_attributes": True}


class MovieCreate(BaseModel):
    title: str
    description: str = ""
    genre: str


class MovieUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    genre: str | None = None


class RatingOut(BaseModel):
    id: int
    movie_id: int
    user_id: int
    score: int
    created_at: datetime

    model_config = {"from_attributes": True}


class RatingCreate(BaseModel):
    score: int
