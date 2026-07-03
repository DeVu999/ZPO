from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.movie import MovieCreate, MovieOut, MovieUpdate, RatingCreate, RatingOut
from app.services.movie_service import MovieService

router = APIRouter(prefix="/api/movies", tags=["movies"])


@router.get("", response_model=list[MovieOut])
def get_all(db: Session = Depends(get_db)):
    service = MovieService(db)
    movies = service.get_all()
    return [
        MovieOut(
            id=m.id,
            title=m.title,
            description=m.description,
            genre=m.genre,
            created_at=m.created_at,
            average_rating=service.get_average_rating(m.id),
            rating_count=service.get_rating_count(m.id),
        )
        for m in movies
    ]


@router.get("/top")
def get_top(
    genre: str | None = None,
    limit: int = Query(default=10, le=50),
    db: Session = Depends(get_db),
):
    service = MovieService(db)
    return service.get_top_movies(genre=genre, limit=limit)


@router.get("/{movie_id}", response_model=MovieOut)
def get_by_id(movie_id: int, db: Session = Depends(get_db)):
    service = MovieService(db)
    m = service.get_by_id(movie_id)
    return MovieOut(
        id=m.id,
        title=m.title,
        description=m.description,
        genre=m.genre,
        created_at=m.created_at,
        average_rating=service.get_average_rating(m.id),
        rating_count=service.get_rating_count(m.id),
    )


@router.post("", response_model=MovieOut, status_code=201)
def create(
    data: MovieCreate,
    current: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = MovieService(db)
    m = service.create(data)
    return MovieOut(
        id=m.id,
        title=m.title,
        description=m.description,
        genre=m.genre,
        created_at=m.created_at,
    )


@router.patch("/{movie_id}", response_model=MovieOut)
def update(
    movie_id: int,
    data: MovieUpdate,
    current: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = MovieService(db)
    m = service.update(movie_id, data)
    return MovieOut(
        id=m.id,
        title=m.title,
        description=m.description,
        genre=m.genre,
        created_at=m.created_at,
        average_rating=service.get_average_rating(m.id),
        rating_count=service.get_rating_count(m.id),
    )


@router.delete("/{movie_id}", status_code=204)
def delete(
    movie_id: int,
    current: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = MovieService(db)
    service.delete(movie_id)


@router.post("/{movie_id}/rate", response_model=RatingOut)
def rate(
    movie_id: int,
    data: RatingCreate,
    current: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = MovieService(db)
    return RatingOut.model_validate(service.rate_movie(movie_id, current.id, data.score))


@router.get("/{movie_id}/ratings", response_model=list[RatingOut])
def get_ratings(movie_id: int, db: Session = Depends(get_db)):
    from app.models.movie import Rating as RatingModel
    ratings = (
        db.query(RatingModel).filter(RatingModel.movie_id == movie_id).all()
    )
    return [RatingOut.model_validate(r) for r in ratings]


@router.websocket("/ws")
async def movies_websocket(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Nowa ocena: {data}")
    except WebSocketDisconnect:
        pass
