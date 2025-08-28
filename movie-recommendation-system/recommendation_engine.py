"""
Movie Recommendation Engine with clean OOP design.
Simple, working implementation of recommendation algorithms.
"""

import numpy as np
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Tuple
import warnings
import time
import ast

from models import MovieRecommendation, SimilarMovieItem

warnings.filterwarnings('ignore')


class MovieRecommendationEngine:
    """
    Main recommendation engine implementing multiple algorithms.
    """
    
    def __init__(self, movies_df: pd.DataFrame, ratings_df: pd.DataFrame):
        self.movies_df = movies_df
        self.ratings_df = ratings_df
        self.user_movie_matrix = self._create_user_movie_matrix()
        
        # Initialize algorithms
        self.item_similarity_matrix = None
        self.svd_model = None
        self.kmeans_model = None
        
        # Precompute matrices
        self._compute_similarities()
        self._fit_svd()
        self._fit_kmeans()
        
        print("✅ Movie Recommendation Engine initialized")
    
    def _create_user_movie_matrix(self) -> pd.DataFrame:
        """Create user-movie rating matrix."""
        return self.ratings_df.pivot(
            index='user_id', 
            columns='movie_id', 
            values='rating'
        ).fillna(0)
    
    def _compute_similarities(self):
        """Compute item-item similarity matrix."""
        self.item_similarity_matrix = cosine_similarity(self.user_movie_matrix.T)
    
    def _fit_svd(self):
        """Fit SVD model."""
        self.svd_model = TruncatedSVD(n_components=20, random_state=42)
        self.user_factors = self.svd_model.fit_transform(self.user_movie_matrix)
        self.item_factors = self.svd_model.components_
    
    def _fit_kmeans(self):
        """Fit KMeans model."""
        self.kmeans_model = KMeans(n_clusters=5, random_state=42, n_init=10)
        self.user_clusters = self.kmeans_model.fit_predict(self.user_movie_matrix)
    
    def _get_popular_movies(self, num_movies: int) -> List[Tuple[int, float]]:
        """Get popular movies for new users."""
        movie_stats = self.ratings_df.groupby('movie_id').agg({
            'rating': ['mean', 'count']
        })
        movie_stats.columns = ['avg_rating', 'count']
        movie_stats['score'] = movie_stats['avg_rating'] * np.log1p(movie_stats['count'])
        
        top_movies = movie_stats.nlargest(num_movies, 'score')
        return [(int(movie_id), float(score)) for movie_id, score in 
                zip(top_movies.index, top_movies['score'])]
    
    def get_recommendations_by_movie(
        self, 
        movie_name: str, 
        num_recommendations: int = 10
    ) -> Tuple[List[MovieRecommendation], float, str]:
        """Get recommendations based on a movie name."""
        start_time = time.time()
        
        # Find the movie in the database
        movie_matches = self.movies_df[
            self.movies_df['title'].str.contains(movie_name, case=False, na=False)
        ]
        
        if movie_matches.empty:
            # Return empty recommendations if movie not found
            execution_time = (time.time() - start_time) * 1000
            return [], execution_time, f"Movie '{movie_name}' not found"
        
        # Use the first match
        movie_id = movie_matches.iloc[0]['movie_id']
        similar_movies = self.get_similar_movies(movie_id, num_recommendations)
        
        # Convert to MovieRecommendation objects
        recommendations = []
        for similar_movie in similar_movies:
            recommendations.append(MovieRecommendation(
                movie_id=similar_movie.movie_id,
                title=similar_movie.title,
                genres=similar_movie.genres,
                year=similar_movie.year,
                predicted_rating=4.0 + similar_movie.similarity_score,  # Scale similarity to rating
                confidence_score=max(0.0, min(1.0, similar_movie.similarity_score))
            ))
        
        execution_time = (time.time() - start_time) * 1000
        return recommendations, execution_time, f"Based on similarity to '{movie_matches.iloc[0]['title']}'"
    
    def get_recommendations_by_genre(
        self, 
        genre: str, 
        num_recommendations: int = 10
    ) -> Tuple[List[MovieRecommendation], float, str]:
        """Get recommendations based on genre preference."""
        start_time = time.time()
        
        # Find movies with the specified genre
        genre_movies = []
        for _, movie in self.movies_df.iterrows():
            movie_genres = movie['genres']
            if isinstance(movie_genres, str) and movie_genres.startswith('['):
                try:
                    movie_genres = ast.literal_eval(movie_genres)
                except (ValueError, SyntaxError):
                    movie_genres = [movie_genres]
            elif not isinstance(movie_genres, list):
                movie_genres = [str(movie_genres)]
            
            # Check if requested genre matches any movie genre (case insensitive)
            if any(genre.lower() in g.lower() for g in movie_genres):
                genre_movies.append(movie)
        
        if not genre_movies:
            execution_time = (time.time() - start_time) * 1000
            return [], execution_time, f"No movies found for genre '{genre}'"
        
        # Sort by average rating and popularity
        genre_df = pd.DataFrame(genre_movies)
        
        # Get rating statistics for these movies
        movie_ratings = []
        for _, movie in genre_df.iterrows():
            movie_id = movie['movie_id']
            ratings = self.ratings_df[self.ratings_df['movie_id'] == movie_id]
            if not ratings.empty:
                avg_rating = ratings['rating'].mean()
                rating_count = len(ratings)
                # Score combines rating and popularity
                score = avg_rating + (0.1 * np.log1p(rating_count))
            else:
                score = 3.0  # Default score for unrated movies
            
            movie_ratings.append({
                'movie_id': movie_id,
                'title': movie['title'],
                'genres': movie['genres'],
                'year': movie.get('year'),
                'score': score,
                'avg_rating': avg_rating if not ratings.empty else 3.0
            })
        
        # Sort by score and take top recommendations
        movie_ratings.sort(key=lambda x: x['score'], reverse=True)
        top_movies = movie_ratings[:num_recommendations]
        
        recommendations = []
        for movie_data in top_movies:
            genres = movie_data['genres']
            if isinstance(genres, str) and genres.startswith('['):
                try:
                    genres = ast.literal_eval(genres)
                except (ValueError, SyntaxError):
                    genres = [genres]
            elif not isinstance(genres, list):
                genres = [str(genres)]
            
            recommendations.append(MovieRecommendation(
                movie_id=movie_data['movie_id'],
                title=movie_data['title'],
                genres=genres,
                year=movie_data['year'],
                predicted_rating=round(movie_data['avg_rating'], 2),
                confidence_score=max(0.0, min(1.0, movie_data['score'] / 5.0))
            ))
        
        execution_time = (time.time() - start_time) * 1000
        return recommendations, execution_time, f"Top {genre} movies by rating and popularity"
    
    def get_recommendations_by_actor(
        self, 
        actor_name: str, 
        num_recommendations: int = 10
    ) -> Tuple[List[MovieRecommendation], float, str]:
        """Get recommendations based on actor name (simulated for demo)."""
        start_time = time.time()
        
        # For this demo, we'll simulate actor-based recommendations
        # by finding movies with similar patterns in titles or using collaborative filtering
        
        # Use collaborative filtering with a simulated user preference
        # We'll create a virtual user who likes movies with certain patterns
        popular_movies = self._get_popular_movies(num_recommendations * 2)
        
        recommendations = []
        for movie_id, score in popular_movies[:num_recommendations]:
            movie_info = self.movies_df[self.movies_df['movie_id'] == movie_id]
            if not movie_info.empty:
                movie = movie_info.iloc[0]
                
                genres = movie['genres']
                if isinstance(genres, str) and genres.startswith('['):
                    try:
                        genres = ast.literal_eval(genres)
                    except (ValueError, SyntaxError):
                        genres = [genres]
                elif not isinstance(genres, list):
                    genres = [str(genres)]
                
                recommendations.append(MovieRecommendation(
                    movie_id=int(movie_id),
                    title=movie['title'],
                    genres=genres,
                    year=int(movie['year']) if pd.notna(movie.get('year')) else None,
                    predicted_rating=4.0,  # Simulated rating
                    confidence_score=max(0.0, min(1.0, score / 10.0))
                ))
        
        execution_time = (time.time() - start_time) * 1000
        return recommendations, execution_time, f"Popular movies (simulated for actor '{actor_name}')"
    
    def get_recommendations(
        self, 
        movie_name: str = None,
        genre: str = None,
        actor_name: str = None,
        num_recommendations: int = 10, 
        algorithm: str = "collaborative"
    ) -> Tuple[List[MovieRecommendation], float, str, str]:
        """Get recommendations based on input type."""
        if movie_name:
            recommendations, execution_time, description = self.get_recommendations_by_movie(
                movie_name, num_recommendations
            )
            return recommendations, execution_time, "movie", movie_name
        elif genre:
            recommendations, execution_time, description = self.get_recommendations_by_genre(
                genre, num_recommendations
            )
            return recommendations, execution_time, "genre", genre
        elif actor_name:
            recommendations, execution_time, description = self.get_recommendations_by_actor(
                actor_name, num_recommendations
            )
            return recommendations, execution_time, "actor", actor_name
        else:
            raise ValueError("At least one of movie_name, genre, or actor_name must be provided")
    
    def get_similar_movies(
        self, 
        movie_id: int, 
        num_similar: int = 10
    ) -> List[SimilarMovieItem]:
        """Get movies similar to the given movie."""
        if movie_id not in self.user_movie_matrix.columns:
            return []
        
        movie_idx = list(self.user_movie_matrix.columns).index(movie_id)
        similarities = self.item_similarity_matrix[movie_idx]
        
        similar_indices = np.argsort(similarities)[::-1][1:num_similar+1]
        
        similar_movies = []
        movie_ids = list(self.user_movie_matrix.columns)
        
        for idx in similar_indices:
            if idx < len(movie_ids):
                similar_movie_id = movie_ids[idx]
                similarity_score = similarities[idx]
                
                movie_info = self.movies_df[self.movies_df['movie_id'] == similar_movie_id]
                if not movie_info.empty:
                    movie = movie_info.iloc[0]
                    
                    genres = movie['genres']
                    if isinstance(genres, str) and genres.startswith('['):
                        try:
                            genres = ast.literal_eval(genres)
                        except (ValueError, SyntaxError):
                            genres = [genres]
                    elif not isinstance(genres, list):
                        genres = [str(genres)]
                    
                    similar_movies.append(SimilarMovieItem(
                        movie_id=int(similar_movie_id),
                        title=movie['title'],
                        genres=genres,
                        year=int(movie['year']) if pd.notna(movie.get('year')) else None,
                        similarity_score=round(float(similarity_score), 3)
                    ))
        
        return similar_movies
    
    def calculate_accuracy_score(self, user_id: int, recommended_movie_ids: List[int]) -> float:
        """Calculate accuracy score for recommendations."""
        if user_id not in self.user_movie_matrix.index:
            return 0.0
        
        user_ratings = self.user_movie_matrix.loc[user_id]
        liked_movies = user_ratings[user_ratings >= 3.0].index.tolist()
        
        if not liked_movies or not recommended_movie_ids:
            return 0.0
        
        overlap = len(set(liked_movies) & set(recommended_movie_ids))
        max_possible = min(len(liked_movies), len(recommended_movie_ids))
        
        return overlap / max_possible if max_possible > 0 else 0.0
    
    def get_system_stats(self) -> dict:
        """Get system statistics."""
        total_movies = len(self.movies_df)
        total_ratings = len(self.ratings_df)
        total_users = self.ratings_df['user_id'].nunique()
        avg_rating = self.ratings_df['rating'].mean()
        
        # Genre statistics
        all_genres = []
        for genres_list in self.movies_df['genres']:
            if isinstance(genres_list, list):
                all_genres.extend(genres_list)
            elif isinstance(genres_list, str):
                try:
                    parsed_genres = ast.literal_eval(genres_list) if genres_list.startswith('[') else [genres_list]
                    all_genres.extend(parsed_genres)
                except (ValueError, SyntaxError):
                    all_genres.append(genres_list)
        
        genre_counts = pd.Series(all_genres).value_counts().head(10)
        most_popular_genres = [
            {"genre": genre, "count": int(count)} 
            for genre, count in genre_counts.items()
        ]
        
        return {
            "total_movies": total_movies,
            "total_ratings": total_ratings,
            "total_users": total_users,
            "average_rating": round(avg_rating, 2),
            "rating_scale": f"{self.ratings_df['rating'].min():.1f}-{self.ratings_df['rating'].max():.1f}",
            "most_popular_genres": most_popular_genres,
            "system_health": "healthy" if total_ratings > 0 else "warning"
        }