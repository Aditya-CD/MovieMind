import pickle
import numpy as np
from pathlib import Path

# Dynamic model path
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"

# Load artifacts once at startup
with open(MODEL_DIR / "movies.pkl", "rb") as f:
    movies = pickle.load(f)

with open(MODEL_DIR / "similarity.pkl", "rb") as f:
    similarity = pickle.load(f)


def recommend(movie: str, top_n: int = 5):
    if movie not in movies["title"].values:
        return []

    movie_index = movies[movies["title"] == movie].index[0]
    sim_scores = similarity[movie_index]

    vote_counts = movies["vote_count"].fillna(0).values
    popularity_boost = np.log(vote_counts + 1)

    final_scores = sim_scores * popularity_boost

    top_indices = final_scores.argsort()[::-1][1 : top_n + 1]

    return movies.iloc[top_indices]["title"].tolist()
