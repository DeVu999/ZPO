from functools import reduce

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.movie import Movie, Rating
from app.schemas.movie import MovieCreate, MovieUpdate


class MovieService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Movie]:
        return self.db.query(Movie).all()

    def get_by_id(self, movie_id: int) -> Movie:
        movie = self.db.query(Movie).filter(Movie.id == movie_id).first()
        if not movie:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Film nie znaleziony",
            )
        return movie

    def create(self, data: MovieCreate) -> Movie:
        movie = Movie(**data.model_dump())
        self.db.add(movie)
        self.db.commit()
        self.db.refresh(movie)
        return movie

    def update(self, movie_id: int, data: MovieUpdate) -> Movie:
        movie = self.get_by_id(movie_id)
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(movie, key, value)
        self.db.commit()
        self.db.refresh(movie)
        return movie

    def delete(self, movie_id: int) -> None:
        movie = self.get_by_id(movie_id)
        self.db.delete(movie)
        self.db.commit()

    def rate_movie(self, movie_id: int, user_id: int, score: int) -> Rating:
        if score < 1 or score > 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ocena musi być w skali 1-5",
            )
        self.get_by_id(movie_id)

        existing = (
            self.db.query(Rating)
            .filter(Rating.movie_id == movie_id, Rating.user_id == user_id)
            .first()
        )
        if existing:
            existing.score = score
            self.db.commit()
            self.db.refresh(existing)
            return existing

        rating = Rating(movie_id=movie_id, user_id=user_id, score=score)
        self.db.add(rating)
        self.db.commit()
        self.db.refresh(rating)
        return rating

    def get_user_ratings(self, user_id: int) -> list[Rating]:
        return self.db.query(Rating).filter(Rating.user_id == user_id).all()

    def get_average_rating(self, movie_id: int) -> float | None:
        ratings = (
            self.db.query(Rating).filter(Rating.movie_id == movie_id).all()
        )
        if not ratings:
            return None
        scores = list(map(lambda r: r.score, ratings))
        avg = reduce(lambda acc, s: acc + s, scores, 0) / len(scores)
        return round(avg, 2)

    def get_rating_count(self, movie_id: int) -> int:
        return (
            self.db.query(Rating).filter(Rating.movie_id == movie_id).count()
        )

    def get_top_movies(self, genre: str | None = None, limit: int = 10) -> list[dict]:
        movies = self.db.query(Movie).all()
        if genre:
            movies = list(filter(lambda m: m.genre.lower() == genre.lower(), movies))

        scored = list(
            map(
                lambda m: {
                    "id": m.id,
                    "title": m.title,
                    "description": m.description,
                    "genre": m.genre,
                    "avg": self.get_average_rating(m.id) or 0,
                    "count": self.get_rating_count(m.id),
                },
                movies,
            )
        )

        scored = list(filter(lambda s: s["count"] > 0, scored))
        scored.sort(key=lambda s: s["avg"], reverse=True)
        return scored[:limit]
