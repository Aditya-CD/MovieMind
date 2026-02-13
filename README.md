# MovieMind: An Intelligent Content-Based Movie Recommender

MovieMind is a full-stack recommendation platform that utilizes a vectorized NLP pipeline to suggest films based on plot similarity and metadata engineering. It balances textual relevance with audience validation through a popularity-aware ranking algorithm.

<img width="1902" height="943" alt="Screenshot" src="https://github.com/user-attachments/assets/c8a27f34-6c1a-499c-b09b-de52c6573182" />

---

## System Architecture

The project is split into a **High-Performance FastAPI Backend** and a **Modern React Frontend**. Unlike basic recommenders, MovieMind incorporates:

* **Feature Engineering:** Optimized metadata extraction (Top 3 Cast, Director, and Decade-based segmentation).
* **NLP Pipeline:** TF-IDF Vectorization with Unigram/Bigram support to capture semantic context.
* **Hybrid Ranking:** A custom scoring function that weights Cosine Similarity against logarithmic popularity scaling.
* **Cloud-Native Model Storage:** Utilizes a custom "Self-Healing" logic to fetch large ML artifacts (200MB+) from Hugging Face Datasets on-the-fly, keeping the production image lightweight.

---

## Live Demo & Preview

* **Live Application:** [https://moviemind-ag.vercel.app/](https://moviemind-ag.vercel.app/)
* **API Documentation:** [https://developer.themoviedb.org/docs](https://developer.themoviedb.org/docs)

[![Hugging Face Dataset](https://img.shields.io/badge/Hugging%20Face-Dataset-blue)](https://huggingface.co/)

---

## Quick Start (Docker - Recommended)

The fastest way to run the full stack locally:

```bash
docker-compose up --build
```

Frontend: [http://localhost](http://localhost)
Backend: [http://localhost:8000](http://localhost:8000)

---

## Manual Development Setup

<details>
<summary>View Manual Instructions</summary>

### Backend

```bash
cd backend
pip install -r requirements.txt
python scripts/model_builder.py
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm start
```

</details>

---

## Recommendation Logic & Improvements

Technical Evolution

| **Metric**     | **Previous Version** | **MovieMind (Current)**                     |
| -------------- | -------------------- | ------------------------------------------- |
| Algorithm      | Bag-of-Words         | **TF-IDF with Sublinear Scaling**           |
| Context        | Unigrams             | **Unigram + Bigram Support**                |
| Ranking        | Pure Similarity      | **Popularity-Aware (Vote Count Weighting)** |
| Temporal Data  | Ignored              | **Decade-Based Tokenization**               |
| Data Precision | float64 (Standard)   | **float32 Quantized (50% RAM reduction)**   |
| Model Hosting  | Local Git LFS        | **Hugging Face Dataset Registry**           |
| Deployment     | Manual Scripting     | **Docker Compose Orchestration**            |

Mathematical Foundation

The system computes the **Cosine Similarity** between sparse TF-IDF vectors. To ensure recommendations are both relevant and high-quality, the similarity score is adjusted:

FinalScore = CosineSim × log(VoteCount + 1)

---

## Project Structure

```
MovieMind/
├── docker-compose.yml      # Multi-container orchestration
├── backend/
│   ├── Dockerfile          # Python 3.12-slim environment
│   ├── app/                # FastAPI routes & Recommender logic
│   ├── models/             # Runtime-downloaded pickle artifacts
│   ├── scripts/            # model_builder.py training script
│   └── requirements.txt    # Python dependencies
└── frontend/
    ├── Dockerfile          # Multi-stage build (Node + Nginx)
    ├── nginx.conf          # Reverse proxy configuration
    ├── src/
    │   ├── components/     # UI components (HeroCard, SearchBar, etc.)
    │   └── services/       # API integration layer
    └── App.css             # Cinematic glassmorphism styling
```

---

## Key Features

* **Smart Search:** Real-time autocomplete fetching from a dataset of 4,800+ movies.
* **Cinematic UI:** Glassmorphism design with backdrop-filter blurs and custom particle backgrounds.
* **Responsive Grid:** A strict CSS Grid implementation ensuring a perfect 5-column layout on desktop.
* **Decade Filtering:** Automatically suggests movies from similar eras to preserve stylistic consistency.
* **Containerized Deployment:** Fully reproducible multi-container environment using Docker Compose.

---

## Trade-offs & Limitations

* **Static Model:** The system currently uses a pre-computed similarity matrix and does not learn from real-time user feedback.
* **Cold Start:** While excellent for new users (no history needed), it lacks personalization based on individual user behavior.
* **Memory Constraints:** While optimized to float32, the system is currently bound by the RAM limits of the hosting provider (Render Free Tier).
* **Artifact Cold Start:** The first startup may take approximately 30 seconds while the system streams model artifacts from Hugging Face.

---

Developed by Aditya Gupta
