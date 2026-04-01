# Machine Learning

A collection of machine learning projects and experiments covering classification, clustering, sentiment analysis, and a full-stack movie recommendation system.

## Projects

### 1. Movie Recommendation System
A modern, full-stack movie recommendation application with a beautiful web interface.

- **Input Methods:** Search by movie name, genre, or actor
- **Algorithms:** Collaborative Filtering, SVD Matrix Factorization, KMeans Clustering
- **Tech Stack:** FastAPI, Pandas, Scikit-learn, Pydantic
- **Features:** Glassmorphism UI, real-time recommendations, responsive design

```bash
cd movie-recommendation-system
pip install -r requirements.txt
python app.py
# Visit http://localhost:8000
```

### 2. Classification Task
`classification_task1_(1)[1].ipynb` — A Jupyter notebook implementing classification algorithms on structured data, including data preprocessing, model training, evaluation metrics, and comparison of classifiers.

### 3. Clustering
`clustering[1].ipynb` — Unsupervised learning notebook demonstrating clustering techniques (e.g., K-Means, hierarchical clustering) with visualization of cluster assignments and evaluation.

### 4. Sentiment Analysis
`sentiment_analysis[1].ipynb` — NLP-based sentiment analysis pipeline covering text preprocessing, feature extraction, and sentiment classification on text data.

## Tech Stack

- **Language:** Python 3.8+
- **Libraries:** Scikit-learn, Pandas, NumPy, Matplotlib, Seaborn
- **Web Framework:** FastAPI (for recommendation system)
- **Notebooks:** Jupyter

## Getting Started

```bash
# Clone the repository
git clone https://github.com/VivekRahal/Machine-Learning.git
cd Machine-Learning

# For notebooks — launch Jupyter
jupyter notebook

# For movie recommendation system
cd movie-recommendation-system
pip install -r requirements.txt
python app.py
```

## Repository Structure

```
Machine-Learning/
├── classification_task1_(1)[1].ipynb    # Classification experiments
├── clustering[1].ipynb                  # Clustering algorithms
├── sentiment_analysis[1].ipynb          # Sentiment analysis pipeline
└── movie-recommendation-system/         # Full-stack recommendation app
    ├── app.py                           # FastAPI application
    ├── models.py                        # Pydantic models
    ├── recommendation_engine.py         # ML recommendation engine
    ├── data_generator.py                # Sample data generator
    ├── movies.csv                       # Movie dataset
    ├── ratings.csv                      # Ratings dataset
    ├── requirements.txt                 # Python dependencies
    └── static/                          # Frontend assets
```

## License

Open-sourced for educational purposes.
