MovieMind: An Intelligent Content-Based Movie Recommender
=========================================================

MovieMind is a full-stack recommendation platform that utilizes a vectorized NLP pipeline to suggest films based on plot similarity and metadata engineering. It balances textual relevance with audience validation through a popularity-aware ranking algorithm.


* * * * *

System Architecture
-----------------------

The project is split into a **High-Performance FastAPI Backend** and a **Modern React Frontend**. Unlike basic recommenders, MovieMind incorporates:

-   **Feature Engineering:** Optimized metadata extraction (Top 3 Cast, Director, and Decade-based segmentation).

-   **NLP Pipeline:** TF-IDF Vectorization with Unigram/Bigram support to capture semantic context.

-   **Hybrid Ranking:** A custom scoring function that weights Cosine Similarity against logarithmic popularity scaling.

* * * * *

Live Demo & Preview
----------------------

-   **Live Application:** 

-   **API Documentation:** 

* * * * *

Installation & Setup
------------------------

### 1\. Backend Setup (Python)

Navigate to the `backend/` directory and ensure you have Python 3.9+ installed.

Bash

```
cd backend

# Install dependencies
pip install -r requirements.txt

# Step 1: Generate ML Artifacts (Pickles)
python scripts/model_builder.py

# Step 2: Start the FastAPI Server
uvicorn app.main:app --reload

```

**Verification:** Once running, verify the engine is live by visiting:

`http://127.0.0.1:8000/recommend/Batman%20Begins`

### 2\. Frontend Setup (React)

Navigate to the `frontend/` directory.

Bash

```
cd frontend

# Install dependencies
npm install

# Configure API (Add your TMDB Key in src/services/api.js)
npm start

```

**Access:** The UI will be available at `http://localhost:3000`.

* * * * *

Recommendation Logic & Improvements
--------------------------------------

### Technical Evolution

| **Metric** | **Previous Version** | **MovieMind (Current)** |
| --- | --- | --- |
| **Algorithm** | Bag-of-Words | **TF-IDF with Sublinear Scaling** |
| **Context** | Unigrams | **Unigram + Bigram Support** |
| **Ranking** | Pure Similarity | **Popularity-Aware (Vote Count Weighting)** |
| **Temporal Data** | Ignored | **Decade-Based Tokenization** |

### Mathematical Foundation

The system computes the **Cosine Similarity** between sparse TF-IDF vectors. To ensure recommendations are both relevant and high-quality, the similarity score is adjusted:

$$FinalScore = CosineSim \times \log(VoteCount + 1)$$

* * * * *

Project Structure
--------------------

Plaintext

```
MovieMind/
├── backend/
│   ├── app/                # FastAPI routes & Recommender logic
│   ├── models/             # Pickle artifacts (Similarity matrix, TF-IDF)
│   ├── scripts/            # model_builder.py training script
│   └── requirements.txt    # Python dependencies
└── frontend/
    ├── src/
    │   ├── components/     # UI components (HeroCard, SearchBar, etc.)
    │   └── services/       # API integration layer
    └── App.css             # Cinematic glassmorphism styling

```

* * * * *

Key Features
---------------

-   **Smart Search:** Real-time autocomplete fetching from a dataset of 4,800+ movies.

-   **Cinematic UI:** Glassmorphism design with backdrop-filter blurs and custom particle backgrounds.

-   **Responsive Grid:** A strict CSS Grid implementation ensuring a perfect 5-column layout on desktop.

-   **Decade Filtering:** Automatically suggests movies from similar eras to preserve stylistic consistency.

* * * * *

Trade-offs & Limitations
---------------------------

-   **Static Model:** The system currently uses a pre-computed similarity matrix and does not learn from real-time user feedback.

-   **Cold Start:** While excellent for new users (no history needed), it lacks personalization based on individual user behavior.

-   **Scalability:** For datasets larger than 100k+ rows, an **Approximate Nearest Neighbors (ANN)** approach would be required to replace the current matrix.

* * * * *

**Developed by [Your Name] as a Portfolio Project.**