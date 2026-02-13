import os
import pickle
import numpy as np
import pandas as pd
import requests
from pathlib import Path

# --- CONFIGURATION ---
# Your Hugging Face Resolve URL
HF_BASE_URL = "https://huggingface.co/datasets/Aadiii03/moviemind-models/resolve/main"
MODEL_FILES = ["movies.pkl", "movies_enriched.pkl", "similarity.pkl"]

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)


def download_if_missing():
    """Downloads model artifacts from Hugging Face if not found locally."""
    for file_name in MODEL_FILES:
        file_path = MODEL_DIR / file_name
        if not file_path.exists():
            print(f"--- {file_name} missing. Downloading from Hugging Face... ---")
            url = f"{HF_BASE_URL}/{file_name}"
            try:
                with requests.get(url, stream=True, timeout=30) as r:
                    r.raise_for_status()
                    with open(file_path, "wb") as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                print(f"Successfully downloaded {file_name}")
            except Exception as e:
                print(f"Error downloading {file_name}: {e}")
                raise SystemExit(
                    "Required model files could not be retrieved. Server stopping."
                )


# --- LOAD ARTIFACTS ---
download_if_missing()


def load_artifacts():
    print("Loading artifacts into memory...")
    with open(MODEL_DIR / "movies.pkl", "rb") as f:
        m = pickle.load(f)
    with open(MODEL_DIR / "movies_enriched.pkl", "rb") as f:
        me = pickle.load(f)
    with open(MODEL_DIR / "similarity.pkl", "rb") as f:
        s = pickle.load(f)

    m = m.reset_index(drop=True)
    me = me.reset_index(drop=True)
    return m, me, s


movies, movies_enriched, similarity = load_artifacts()


# --- HELPER & CORE LOGIC ---
def get_movie_details(idx):
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
    movie_search = movies[movies["title"].str.lower() == movie_name.lower()]
    if movie_search.empty:
        return None

    movie_pos = movie_search.index[0]
    sim_scores = similarity[movie_pos]

    vote_counts = movies["vote_count"].fillna(0).values
    popularity_boost = np.log(vote_counts + 1)
    final_scores = sim_scores * popularity_boost

    top_indices = final_scores.argsort()[::-1][1 : top_n + 1]

    selected_movie = get_movie_details(movie_pos)
    recommendations = [get_movie_details(i) for i in top_indices]

    return {"selected_movie": selected_movie, "recommendations": recommendations}


def get_all_movie_titles():
    return sorted(movies["title"].tolist())
