from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.recommender import recommend

app = FastAPI(title="Movie Recommender API")

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict later in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Movie Recommender API is running"}


@app.get("/recommend/{movie_name}")
def get_recommendations(movie_name: str):
    results = recommend(movie_name)

    if not results:
        raise HTTPException(status_code=404, detail="Movie not found")

    return {"movie": movie_name, "recommendations": results}
