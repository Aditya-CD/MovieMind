import pickle
import numpy as np
import pandas as pd
from pathlib import Path

# Dynamic model path
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"


# Load artifacts once at startup
def load_artifacts():
    with open(MODEL_DIR / "movies.pkl", "rb") as f:
        m = pickle.load(f)
    with open(MODEL_DIR / "movies_enriched.pkl", "rb") as f:
        me = pickle.load(f)
    with open(MODEL_DIR / "similarity.pkl", "rb") as f:
        s = pickle.load(f)

    # CRITICAL: Synchronize indices immediately after loading
    # This ensures row 0 in 'm' is row 0 in 'me' and row 0 in 's'
    m = m.reset_index(drop=True)
    me = me.reset_index(drop=True)

    return m, me, s


movies, movies_enriched, similarity = load_artifacts()


def get_movie_details(idx):
    """Get enriched movie details by integer position (iloc)"""
    # Use .iloc to ensure we are grabbing the exact row matching the matrix
    movie = movies_enriched.iloc[idx]

    return {
        "id": int(movie["id"]),
        "title": movie["title"],
        "overview": movie["overview"] if pd.notna(movie["overview"]) else "",
        "genres": (
            movie["genres_list"] if isinstance(movie["genres_list"], list) else []
        ),
        "cast": movie["cast_list"] if isinstance(movie["cast_list"], list) else [],
        "director": movie["director"] if pd.notna(movie["director"]) else "",
        "vote_average": (
            float(movie["vote_average"]) if pd.notna(movie["vote_average"]) else 0.0
        ),
        "vote_count": int(movie["vote_count"]) if pd.notna(movie["vote_count"]) else 0,
        "release_date": (
            str(movie["release_date"]) if pd.notna(movie["release_date"]) else ""
        ),
        "runtime": int(movie["runtime"]) if pd.notna(movie["runtime"]) else 0,
    }


def recommend(movie_name: str, top_n: int = 5):
    """
    Finds the movie by title and returns the selected movie info
    plus popularity-weighted recommendations.
    """
    # 1. Case-insensitive search for the movie row
    movie_search = movies[movies["title"].str.lower() == movie_name.lower()]

    if movie_search.empty:
        return None

    # 2. Get the ACTUAL row position (0, 1, 2...)
    # Because we reset_index above, the first item's index is its position.
    movie_pos = movie_search.index[0]

    # 3. Calculate Scores
    sim_scores = similarity[movie_pos]

    # Apply Popularity Boost (Logarithmic scaling)
    # This ensures textually similar movies that are well-known rank higher
    vote_counts = movies["vote_count"].fillna(0).values
    popularity_boost = np.log(vote_counts + 1)
    final_scores = sim_scores * popularity_boost

    # 4. Get top indices (excluding the movie itself)
    # argsort gives us the positions (0, 1, 2...) which match our .iloc logic
    top_indices = final_scores.argsort()[::-1][1 : top_n + 1]

    # 5. Fetch details using the verified row position
    selected_movie = get_movie_details(movie_pos)
    recommendations = [get_movie_details(i) for i in top_indices]

    return {"selected_movie": selected_movie, "recommendations": recommendations}


def get_all_movie_titles():
    """Return all available movie titles for autocomplete"""
    return sorted(movies["title"].tolist())
