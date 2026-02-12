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

# Ensure models folder exists
MODEL_DIR.mkdir(parents=True, exist_ok=True)


def convert(obj):
    return [i["name"] for i in ast.literal_eval(obj)]


def convert_cast(obj):
    L = []
    for i in ast.literal_eval(obj)[:3]:
        L.append(i["name"])
    return L


def fetch_director(obj):
    return [i["name"] for i in ast.literal_eval(obj) if i["job"] == "Director"]


def build_model():
    print("Loading datasets...")

    movies = pd.read_csv(DATA_DIR / "tmdb_5000_movies.csv")
    credits = pd.read_csv(DATA_DIR / "tmdb_5000_credits.csv")

    movies = movies.merge(credits, on="title")

    # Release date processing
    movies["release_date"] = pd.to_datetime(movies["release_date"], errors="coerce")
    movies["year"] = movies["release_date"].dt.year.astype("Int64")
    movies["decade"] = (movies["year"] // 10) * 10
    movies["decade"] = movies["decade"].astype(str) + "s"

    movies = movies[
        [
            "id",
            "title",
            "overview",
            "genres",
            "keywords",
            "cast",
            "crew",
            "decade",
            "vote_count",
        ]
    ]

    movies.dropna(inplace=True)
    movies = movies[movies["decade"] != "<NA>s"]

    print("Performing feature engineering...")

    movies["genres"] = movies["genres"].apply(convert)
    movies["keywords"] = movies["keywords"].apply(convert)
    movies["cast"] = movies["cast"].apply(convert_cast)
    movies["crew"] = movies["crew"].apply(fetch_director)
    movies["overview"] = movies["overview"].apply(lambda x: x.split())
    movies["decade"] = movies["decade"].apply(lambda x: [x])

    for col in ["genres", "keywords", "cast", "crew"]:
        movies[col] = movies[col].apply(lambda x: [i.replace(" ", "") for i in x])

    movies["tags"] = (
        movies["overview"]
        + movies["genres"]
        + movies["keywords"]
        + movies["cast"]
        + movies["crew"]
        + movies["decade"]
    )

    new_df = movies[["id", "title", "tags", "vote_count"]].copy()
    new_df["tags"] = new_df["tags"].apply(lambda x: " ".join(x).lower())

    print("Training TF-IDF model...")

    tfidf = TfidfVectorizer(
        max_features=7000,
        stop_words="english",
        max_df=0.7,
        min_df=2,
        ngram_range=(1, 2),
        sublinear_tf=True,
    )

    vectors = tfidf.fit_transform(new_df["tags"])
    vectors = normalize(vectors)
    similarity = cosine_similarity(vectors)

    print("Saving model artifacts...")

    with open(MODEL_DIR / "movies.pkl", "wb") as f:
        pickle.dump(new_df, f)

    with open(MODEL_DIR / "similarity.pkl", "wb") as f:
        pickle.dump(similarity, f)

    with open(MODEL_DIR / "tfidf.pkl", "wb") as f:
        pickle.dump(tfidf, f)

    print("Model built and saved successfully.")


if __name__ == "__main__":
    build_model()
