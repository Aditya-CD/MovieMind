MovieMind: Recommendation Engine
================================

The MovieMind backend is a high-performance Python API designed to deliver content-based movie recommendations. It utilizes a vectorized NLP pipeline and a popularity-aware ranking algorithm to suggest films based on metadata similarity and audience validation.

1\. Problem Statement
---------------------

The objective was to engineer a system capable of providing accurate recommendations from the TMDB 5,000 dataset without relying on user history. The system is purely **content-driven**, making it ideal for solving the "cold-start" problem in recommendation engines.

2\. Architecture & Feature Engineering
--------------------------------------

The engine processes movie overviews, genres, keywords, and key contributors. Specific design choices include:

-   **Cast & Crew Optimization:** Restricted to the top 3 billed actors and the Director to emphasize the most influential contributors and reduce feature sparsity.

-   **Noise Reduction:** Production companies were removed after empirical testing showed they added high-frequency noise without improving recommendation quality.

-   **Temporal Segmentation:** Release dates were converted into **decade-based tokens** (e.g., `2000s`). This incorporates temporal similarity into the vector space without introducing the numeric bias of raw year values.

3\. Mathematical Strategy
-------------------------

### Vectorization: TF-IDF vs. Bag-of-Words

Moving beyond basic CountVectorization, this version implements **TF-IDF (Term Frequency-Inverse Document Frequency)** to down-weight common stop words and emphasize discriminative terms.

-   **N-Grams (1,2):** Introduced bigrams to capture contextual phrases like "dark knight" or "space war."

-   **Configuration:** `max_df=0.7`, `min_df=2`, and `sublinear_tf=True` to scale term frequency logarithmically.

### Similarity & Ranking

-   **Cosine Similarity:** Chosen for its ability to measure angular similarity independent of document length, which is optimal for textual metadata.

-   **Popularity-Aware Ranking:** To avoid recommending obscure films that match textually but lack quality, a **logarithmic popularity scaling** was applied using `vote_count`.

    $$FinalScore = CosineSim \times \log(VoteCount + 1)$$

    This ensures a balance between content relevance and global audience validation.

4\. Technical Evolution
-----------------------

| **Feature** | **Version 1 (Baseline)** | **Version 2 (Current)** |
| --- | --- | --- |
| **Vectorization** | Bag-of-Words | **TF-IDF** |
| **Context** | Unigrams Only | **Unigrams + Bigrams** |
| **Ranking** | Pure Similarity | **Popularity-Aware Ranking** |
| **Temporal Data** | Ignored | **Decade Segmentation** |
| **Feature Set** | Raw Metadata | **Weighted Feature Engineering** |

5\. Performance & Scalability
-----------------------------

-   **Memory Efficiency:** Utilized sparse matrices for similarity computation to minimize RAM overhead.

-   **Vectorization over Loops:** Used NumPy-based vectorized operations for ranking, significantly reducing latency compared to standard Python loops.

-   **FastAPI Integration:** Selected FastAPI for its asynchronous capabilities and automatic OpenAPI documentation.

6\. Project Structure
---------------------

Plaintext

```
backend/
├── app/
│   ├── main.py          # FastAPI routes and CORS configuration
│   └── recommender.py   # Core logic for similarity and ranking
├── models/
│   ├── movies.pkl       # Processed metadata
│   ├── similarity.pkl   # Pre-computed similarity matrix
│   └── tfidf.pkl        # Fitted TF-IDF vectorizer
├── scripts/
│   └── model_builder.py # Data cleaning and model training script
└── requirements.txt     # Dependency manifest

```

7\. Limitations & Future Scope
------------------------------

While highly effective for content discovery, the current model:

-   Does not incorporate user-based collaborative filtering.

-   Is a static model (does not learn from real-time user feedback).

**Future Roadmap:** Integration of **Sentence-BERT embeddings** for deeper semantic understanding and implementing an **Approximate Nearest Neighbors (ANN)** index for sub-millisecond scalability on larger datasets.

* * * * *

**Developed for the MovieMind Portfolio Project.**