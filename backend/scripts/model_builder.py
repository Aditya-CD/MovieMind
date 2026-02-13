import numpy as np
import pandas as pd
import ast
import pickle
import gc
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize

# --- DIRECTORY SETUP ---
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "models"

MODEL_DIR.mkdir(parents=True, exist_ok=True)


# --- HELPER FUNCTIONS ---
def convert(obj):
    try:
        return [i["name"] for i in ast.literal_eval(obj)]
    except:
        return []


def convert_cast(obj):
    try:
        L = []
        for i in ast.literal_eval(obj)[:3]:
            L.append(i["name"])
        return L
    except:
        return []


def fetch_director(obj):
    try:
        directors = [i["name"] for i in ast.literal_eval(obj) if i["job"] == "Director"]
        return directors[0] if directors else ""
    except:
        return ""


# --- MAIN BUILDER ---
def build_model():
    print("Loading datasets...")
    try:
        movies_raw = pd.read_csv(DATA_DIR / "tmdb_5000_movies.csv")
        credits_raw = pd.read_csv(DATA_DIR / "tmdb_5000_credits.csv")
    except FileNotFoundError:
        print("Error: CSV files not found in data/ folder.")
        return

    # Merge data
    df = movies_raw.merge(credits_raw, on="title")

    # --- DATA CLEANING ---
    df.drop_duplicates(subset="title", inplace=True)
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
    df.dropna(subset=["overview", "release_date"], inplace=True)

    df["year"] = df["release_date"].dt.year.astype("Int64")
    df["decade"] = (df["year"] // 10) * 10
    df["decade_str"] = df["decade"].astype(str) + "s"
    df = df[df["decade_str"] != "<NA>s"]

    # CRITICAL: Reset index to ensure matrix synchronization
    df.reset_index(drop=True, inplace=True)

    print(f"Cleaned dataset. Total movies: {len(df)}")

    # --- FEATURE ENGINEERING ---
    print("Performing feature engineering...")
    df["genres_list"] = df["genres"].apply(convert)
    df["keywords_list"] = df["keywords"].apply(convert)
    df["cast_list"] = df["cast"].apply(convert_cast)
    df["director"] = df["crew"].apply(fetch_director)

    # Creating ML tags
    df["tags"] = (
        df["overview"].apply(lambda x: x.split())
        + df["genres_list"].apply(lambda x: [i.replace(" ", "") for i in x])
        + df["keywords_list"].apply(lambda x: [i.replace(" ", "") for i in x])
        + df["cast_list"].apply(lambda x: [i.replace(" ", "") for i in x])
        + df["director"].apply(lambda x: [x.replace(" ", "")] if x else [])
        + df["decade_str"].apply(lambda x: [x])
    )

    # 1. Main DataFrame for searching
    new_df = df[["id", "title", "tags", "vote_count"]].copy()
    new_df["tags"] = new_df["tags"].apply(lambda x: " ".join(x).lower())

    # 2. Detailed DataFrame for the UI
    enriched_final = df[
        [
            "id",
            "title",
            "overview",
            "genres_list",
            "cast_list",
            "director",
            "vote_average",
            "vote_count",
            "popularity",
            "release_date",
            "runtime",
        ]
    ].copy()

    # --- MODEL TRAINING ---
    print("Training TF-IDF model...")
    tfidf = TfidfVectorizer(
        max_features=7000,
        stop_words="english",
        ngram_range=(1, 2),
        sublinear_tf=True,
    )

    vectors = tfidf.fit_transform(new_df["tags"])
    vectors = normalize(vectors)

    # OPTIMIZATION: Convert matrix to float32 to save 50% RAM
    print("Computing similarity matrix (float32 optimized)...")
    similarity = cosine_similarity(vectors).astype("float32")

    # --- SAVING ARTIFACTS ---
    print("Saving optimized artifacts to models/ folder...")

    with open(MODEL_DIR / "movies.pkl", "wb") as f:
        pickle.dump(new_df, f)

    with open(MODEL_DIR / "movies_enriched.pkl", "wb") as f:
        pickle.dump(enriched_final, f)

    with open(MODEL_DIR / "similarity.pkl", "wb") as f:
        pickle.dump(similarity, f)

    with open(MODEL_DIR / "tfidf.pkl", "wb") as f:
        pickle.dump(tfidf, f)

    print("Success! All optimized artifacts are synchronized.")

    # Force memory release
    del similarity, vectors, tfidf, df, new_df, enriched_final
    gc.collect()


if __name__ == "__main__":
    build_model()
