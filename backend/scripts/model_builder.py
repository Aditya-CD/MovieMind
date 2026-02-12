import numpy as np
import pandas as pd
import ast
import pickle
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize

# Get project root dynamically
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "models"

MODEL_DIR.mkdir(parents=True, exist_ok=True)


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


def build_model():
    print("Loading datasets...")
    movies_raw = pd.read_csv(DATA_DIR / "tmdb_5000_movies.csv")
    credits_raw = pd.read_csv(DATA_DIR / "tmdb_5000_credits.csv")

    # Merge data
    df = movies_raw.merge(credits_raw, on="title")

    # --- CRITICAL FIX: CLEANING FIRST ---
    # 1. Remove duplicates to ensure 1-to-1 title mapping
    df.drop_duplicates(subset="title", inplace=True)

    # 2. Process dates and drop NAs immediately to keep rows synchronized
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
    df.dropna(subset=["overview", "release_date"], inplace=True)

    df["year"] = df["release_date"].dt.year.astype("Int64")
    df["decade"] = (df["year"] // 10) * 10
    df["decade_str"] = df["decade"].astype(str) + "s"
    df = df[df["decade_str"] != "<NA>s"]

    # 3. RESET INDEX: This is the most important line.
    # It ensures the DataFrame index 0, 1, 2... matches the Similarity Matrix row 0, 1, 2...
    df.reset_index(drop=True, inplace=True)

    print(f"Cleaned dataset. Total movies: {len(df)}")

    # --- FEATURE ENGINEERING ---
    print("Performing feature engineering...")
    df["genres_list"] = df["genres"].apply(convert)
    df["keywords_list"] = df["keywords"].apply(convert)
    df["cast_list"] = df["cast"].apply(convert_cast)
    df["director"] = df["crew"].apply(fetch_director)

    # Create tags for ML
    df["genres_tags"] = df["genres_list"].apply(
        lambda x: [i.replace(" ", "") for i in x]
    )
    df["keywords_tags"] = df["keywords_list"].apply(
        lambda x: [i.replace(" ", "") for i in x]
    )
    df["cast_tags"] = df["cast_list"].apply(lambda x: [i.replace(" ", "") for i in x])
    df["director_tag"] = df["director"].apply(
        lambda x: [x.replace(" ", "")] if x else []
    )
    df["overview_tags"] = df["overview"].apply(lambda x: x.split())
    df["decade_tags"] = df["decade_str"].apply(lambda x: [x])

    df["tags"] = (
        df["overview_tags"]
        + df["genres_tags"]
        + df["keywords_tags"]
        + df["cast_tags"]
        + df["director_tag"]
        + df["decade_tags"]
    )

    # Create the training dataframe
    new_df = df[["id", "title", "tags", "vote_count"]].copy()
    new_df["tags"] = new_df["tags"].apply(lambda x: " ".join(x).lower())

    # Create the detailed enriched dataframe from the SAME 'df'
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
    similarity = cosine_similarity(vectors)

    # --- SAVING ---
    print("Saving model artifacts...")
    with open(MODEL_DIR / "movies.pkl", "wb") as f:
        pickle.dump(new_df, f)

    with open(MODEL_DIR / "movies_enriched.pkl", "wb") as f:
        pickle.dump(enriched_final, f)

    with open(MODEL_DIR / "similarity.pkl", "wb") as f:
        pickle.dump(similarity, f)

    print("Success! All artifacts are synchronized.")


if __name__ == "__main__":
    build_model()
