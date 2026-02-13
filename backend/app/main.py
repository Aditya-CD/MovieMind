from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.recommender import recommend, get_all_movie_titles

app = FastAPI(title="MovieMind API")

# Update this origins list with your actual Vercel URL after you deploy the frontend
origins = [
    "http://localhost:3000",
    "http://localhost",
    "*",  # Allows all for initial deployment, but specify your Vercel URL later!
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "MovieMind API is running ", "version": "2.0"}


@app.get("/movies")
def get_movies():
    return {"movies": get_all_movie_titles()}


@app.get("/recommend/{movie_name}")
def get_recommendations(movie_name: str):
    results = recommend(movie_name)
    if not results:
        raise HTTPException(status_code=404, detail="Movie not found")
    return results
