import pandas as pd
import numpy as np
from typing import Tuple
import random

def generate_sample_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Generate sample movie and rating data for demonstration purposes.
    In production, this would be replaced with real data from a database.
    """
    
    # Sample movies with different genres
    movies_data = [
        {"movie_id": 1, "title": "The Shawshank Redemption", "genres": ["Drama"], "year": 1994},
        {"movie_id": 2, "title": "The Godfather", "genres": ["Crime", "Drama"], "year": 1972},
        {"movie_id": 3, "title": "The Dark Knight", "genres": ["Action", "Crime", "Drama"], "year": 2008},
        {"movie_id": 4, "title": "Pulp Fiction", "genres": ["Crime", "Drama"], "year": 1994},
        {"movie_id": 5, "title": "Forrest Gump", "genres": ["Drama", "Romance"], "year": 1994},
        {"movie_id": 6, "title": "Inception", "genres": ["Action", "Sci-Fi", "Thriller"], "year": 2010},
        {"movie_id": 7, "title": "The Matrix", "genres": ["Action", "Sci-Fi"], "year": 1999},
        {"movie_id": 8, "title": "Goodfellas", "genres": ["Biography", "Crime", "Drama"], "year": 1990},
        {"movie_id": 9, "title": "The Lord of the Rings: The Return of the King", "genres": ["Adventure", "Drama", "Fantasy"], "year": 2003},
        {"movie_id": 10, "title": "Fight Club", "genres": ["Drama"], "year": 1999},
        {"movie_id": 11, "title": "Star Wars: Episode IV - A New Hope", "genres": ["Adventure", "Fantasy", "Sci-Fi"], "year": 1977},
        {"movie_id": 12, "title": "The Lord of the Rings: The Fellowship of the Ring", "genres": ["Adventure", "Drama", "Fantasy"], "year": 2001},
        {"movie_id": 13, "title": "One Flew Over the Cuckoo's Nest", "genres": ["Drama"], "year": 1975},
        {"movie_id": 14, "title": "Goodfellas", "genres": ["Biography", "Crime", "Drama"], "year": 1990},
        {"movie_id": 15, "title": "Seven Samurai", "genres": ["Adventure", "Drama"], "year": 1954},
        {"movie_id": 16, "title": "City of God", "genres": ["Crime", "Drama"], "year": 2002},
        {"movie_id": 17, "title": "Life Is Beautiful", "genres": ["Comedy", "Drama", "Romance"], "year": 1997},
        {"movie_id": 18, "title": "The Silence of the Lambs", "genres": ["Crime", "Drama", "Thriller"], "year": 1991},
        {"movie_id": 19, "title": "It's a Wonderful Life", "genres": ["Drama", "Family", "Fantasy"], "year": 1946},
        {"movie_id": 20, "title": "Spirited Away", "genres": ["Animation", "Adventure", "Family"], "year": 2001}
    ]
    
    movies_df = pd.DataFrame(movies_data)
    
    # Generate sample ratings (user_id, movie_id, rating)
    np.random.seed(42)
    num_users = 100
    ratings_data = []
    
    for user_id in range(1, num_users + 1):
        # Each user rates between 5-15 movies
        num_ratings = np.random.randint(5, 16)
        rated_movies = np.random.choice(movies_df['movie_id'].values, num_ratings, replace=False)
        
        for movie_id in rated_movies:
            # Generate ratings with some user preferences
            if user_id <= 30:  # Users who prefer drama/crime
                if any(genre in ['Drama', 'Crime'] for genre in movies_df[movies_df['movie_id'] == movie_id]['genres'].iloc[0]):
                    rating = np.random.normal(4.2, 0.8)
                else:
                    rating = np.random.normal(3.2, 1.0)
            elif user_id <= 60:  # Users who prefer action/sci-fi
                if any(genre in ['Action', 'Sci-Fi'] for genre in movies_df[movies_df['movie_id'] == movie_id]['genres'].iloc[0]):
                    rating = np.random.normal(4.3, 0.7)
                else:
                    rating = np.random.normal(3.0, 1.1)
            else:  # General users
                rating = np.random.normal(3.5, 1.0)
            
            # Clamp ratings between 1 and 5
            rating = np.clip(rating, 1.0, 5.0)
            
            ratings_data.append({
                "user_id": user_id,
                "movie_id": int(movie_id),
                "rating": round(rating, 1),
                "timestamp": np.random.randint(1000000000, 1600000000)
            })
    
    ratings_df = pd.DataFrame(ratings_data)
    
    return movies_df, ratings_df

def create_user_movie_matrix(ratings_df: pd.DataFrame) -> pd.DataFrame:
    """Create a user-movie rating matrix."""
    return ratings_df.pivot(index='user_id', columns='movie_id', values='rating').fillna(0)

def save_sample_data():
    """Save sample data to CSV files."""
    movies_df, ratings_df = generate_sample_data()
    movies_df.to_csv('movies.csv', index=False)
    ratings_df.to_csv('ratings.csv', index=False)
    return movies_df, ratings_df

if __name__ == "__main__":
    movies_df, ratings_df = save_sample_data()
    print(f"Generated {len(movies_df)} movies and {len(ratings_df)} ratings")
    print("\nMovies sample:")
    print(movies_df.head())
    print("\nRatings sample:")
    print(ratings_df.head())