from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.recommender import recommend, get_all_movie_titles

app = FastAPI(title="MovieMind API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "MovieMind API is running 🎬"}


@app.get("/movies")
def get_movies():
    """Get all available movie titles for autocomplete"""
    return {"movies": get_all_movie_titles()}


@app.get("/recommend/{movie_name}")
def get_recommendations(movie_name: str):
    results = recommend(movie_name)

    if not results:
        raise HTTPException(status_code=404, detail="Movie not found")

    return results
