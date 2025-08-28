"""
Data models for the Movie Recommendation System.
Implements clean OOP design with proper validation and type safety.
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Literal
from enum import Enum
from datetime import datetime


class GenreEnum(str, Enum):
    """Enumeration of valid movie genres."""
    ACTION = "Action"
    ADVENTURE = "Adventure"
    ANIMATION = "Animation"
    CHILDREN = "Children"
    COMEDY = "Comedy"
    CRIME = "Crime"
    DOCUMENTARY = "Documentary"
    DRAMA = "Drama"
    FANTASY = "Fantasy"
    FILM_NOIR = "Film-Noir"
    HORROR = "Horror"
    MUSICAL = "Musical"
    MYSTERY = "Mystery"
    ROMANCE = "Romance"
    SCI_FI = "Sci-Fi"
    THRILLER = "Thriller"
    WAR = "War"
    WESTERN = "Western"


class AlgorithmType(str, Enum):
    """Enumeration of available recommendation algorithms."""
    COLLABORATIVE = "collaborative"
    SVD = "svd"
    KMEANS = "kmeans"


class SimilarityType(str, Enum):
    """Enumeration of similarity calculation methods."""
    COSINE = "cosine"
    JACCARD = "jaccard"


class Movie(BaseModel):
    """
    Movie entity with validation and business logic.
    Represents a single movie in the recommendation system.
    """
    movie_id: int = Field(..., ge=1, description="Unique movie identifier")
    title: str = Field(..., min_length=1, max_length=200, description="Movie title")
    genres: List[str] = Field(..., min_items=1, description="List of movie genres")
    year: Optional[int] = Field(None, ge=1900, le=2030, description="Release year")
    
    @validator('title')
    @classmethod
    def validate_title(cls, v):
        """Validate and clean movie title."""
        if not v or v.isspace():
            raise ValueError("Title cannot be empty or whitespace")
        return v.strip()
    
    @validator('genres')
    @classmethod
    def validate_genres(cls, v):
        """Validate genre list."""
        if not v:
            raise ValueError("Movie must have at least one genre")
        return [genre.strip() for genre in v if genre.strip()]
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "movie_id": 1,
                "title": "Toy Story",
                "genres": ["Animation", "Children", "Comedy"],
                "year": 1995
            }
        }


class Rating(BaseModel):
    """
    Rating entity representing user ratings for movies.
    Implements validation for rating values and relationships.
    """
    user_id: int = Field(..., ge=1, description="User identifier")
    movie_id: int = Field(..., ge=1, description="Movie identifier")
    rating: float = Field(..., ge=0.5, le=5.0, description="Rating value (0.5-5.0)")
    timestamp: Optional[datetime] = Field(None, description="Rating timestamp")
    
    @validator('rating')
    @classmethod
    def validate_rating(cls, v):
        """Validate rating is in 0.5 increments."""
        if v % 0.5 != 0:
            raise ValueError("Rating must be in 0.5 increments")
        return v
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "user_id": 1,
                "movie_id": 1,
                "rating": 4.5,
                "timestamp": "2023-01-01T12:00:00"
            }
        }


class User(BaseModel):
    """
    User entity with preference management.
    Represents a user in the recommendation system.
    """
    user_id: int = Field(..., ge=1, description="Unique user identifier")
    preferences: Optional[List[str]] = Field(None, description="User's preferred genres")
    
    @validator('preferences')
    @classmethod
    def validate_preferences(cls, v):
        """Validate user preferences."""
        if v is not None:
            return [pref.strip() for pref in v if pref.strip()]
        return v
    
    def has_preference_for_genre(self, genre: str) -> bool:
        """Check if user has preference for a specific genre."""
        if not self.preferences:
            return False
        preferences = self.preferences or []
        return genre.lower() in [pref.lower() for pref in preferences]


class RecommendationRequest(BaseModel):
    """
    Request model for movie recommendations.
    Supports multiple input types: movie name, genre, or actor.
    """
    # Input options (at least one must be provided)
    movie_name: Optional[str] = Field(None, description="Movie name to find similar movies")
    genre: Optional[str] = Field(None, description="Genre preference (e.g., Action, Comedy)")
    actor_name: Optional[str] = Field(None, description="Actor name for movies they appeared in")
    
    # Request parameters
    num_recommendations: int = Field(10, ge=1, le=20, description="Number of recommendations")
    algorithm: AlgorithmType = Field(AlgorithmType.COLLABORATIVE, description="Algorithm to use")
    min_rating_threshold: Optional[float] = Field(3.0, ge=0.5, le=5.0, description="Minimum rating threshold")
    
    @validator('movie_name', 'genre', 'actor_name')
    @classmethod
    def validate_at_least_one_input(cls, v, values):
        """Ensure at least one input method is provided."""
        movie_name = values.get('movie_name') or v if 'movie_name' not in values else values.get('movie_name')
        genre = values.get('genre') or v if 'genre' not in values else values.get('genre')
        actor_name = values.get('actor_name') or v if 'actor_name' not in values else values.get('actor_name')
        
        if not any([movie_name, genre, actor_name]):
            raise ValueError("At least one of movie_name, genre, or actor_name must be provided")
        return v
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "user_id": 1,
                "num_recommendations": 10,
                "algorithm": "collaborative",
                "min_rating_threshold": 3.0
            }
        }


class MovieRecommendation(BaseModel):
    """
    Single movie recommendation with prediction details.
    Represents a recommended movie with its predicted rating.
    """
    movie_id: int = Field(..., description="Recommended movie ID")
    title: str = Field(..., description="Movie title")
    genres: List[str] = Field(..., description="Movie genres")
    year: Optional[int] = Field(None, description="Release year")
    predicted_rating: float = Field(..., ge=0.0, le=5.0, description="Predicted rating")
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Prediction confidence")
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "movie_id": 1,
                "title": "Toy Story",
                "genres": ["Animation", "Children", "Comedy"],
                "year": 1995,
                "predicted_rating": 4.2,
                "confidence_score": 0.85
            }
        }


class RecommendationResponse(BaseModel):
    """
    Response model for movie recommendations.
    Contains recommended movies and metadata about the recommendation.
    """
    input_type: str = Field(..., description="Type of input used (movie, genre, actor)")
    input_value: str = Field(..., description="The actual input value provided")
    recommendations: List[MovieRecommendation] = Field(..., description="List of recommended movies")
    algorithm_used: AlgorithmType = Field(..., description="Algorithm used for recommendations")
    total_recommendations: int = Field(..., description="Total number of recommendations")
    accuracy_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Recommendation accuracy")
    execution_time_ms: Optional[float] = Field(None, description="Execution time in milliseconds")
    
    @validator('total_recommendations')
    @classmethod
    def validate_total_matches_list(cls, v, values):
        """Validate total_recommendations matches the actual list length."""
        if 'recommendations' in values and len(values['recommendations']) != v:
            raise ValueError("Total recommendations must match the length of recommendations list")
        return v
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "user_id": 1,
                "recommendations": [],
                "algorithm_used": "collaborative",
                "total_recommendations": 0,
                "accuracy_score": 0.75,
                "execution_time_ms": 245.6
            }
        }


class SimilarityRequest(BaseModel):
    """
    Request model for movie similarity calculations.
    Used to find movies similar to a given movie.
    """
    movie_id: int = Field(..., ge=1, description="Movie to find similar movies for")
    similarity_type: SimilarityType = Field(SimilarityType.COSINE, description="Similarity calculation method")
    num_similar: int = Field(10, ge=1, le=50, description="Number of similar movies to return")
    min_similarity_threshold: Optional[float] = Field(0.1, ge=0.0, le=1.0, description="Minimum similarity threshold")
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "movie_id": 1,
                "similarity_type": "cosine",
                "num_similar": 10,
                "min_similarity_threshold": 0.1
            }
        }


class SimilarMovieItem(BaseModel):
    """
    Single similar movie item with similarity score.
    Represents a movie similar to the query movie.
    """
    movie_id: int = Field(..., description="Similar movie ID")
    title: str = Field(..., description="Movie title")
    genres: List[str] = Field(..., description="Movie genres")
    year: Optional[int] = Field(None, description="Release year")
    similarity_score: float = Field(..., ge=0.0, le=1.0, description="Similarity score")


class SimilarityResponse(BaseModel):
    """
    Response model for movie similarity requests.
    Contains similar movies and similarity metadata.
    """
    movie_id: int = Field(..., description="Original movie ID")
    similar_movies: List[SimilarMovieItem] = Field(..., description="List of similar movies")
    similarity_type: SimilarityType = Field(..., description="Similarity method used")
    total_similar: int = Field(..., description="Total number of similar movies found")
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "movie_id": 1,
                "similar_movies": [],
                "similarity_type": "cosine",
                "total_similar": 0
            }
        }


class SystemStats(BaseModel):
    """
    System statistics and health information.
    Provides insights into the recommendation system's data and performance.
    """
    total_movies: int = Field(..., ge=0, description="Total number of movies")
    total_ratings: int = Field(..., ge=0, description="Total number of ratings")
    total_users: int = Field(..., ge=0, description="Total number of users")
    average_rating: float = Field(..., ge=0.0, le=5.0, description="Average rating across all movies")
    rating_scale: str = Field(..., description="Rating scale (e.g., '0.5-5.0')")
    most_popular_genres: List[dict] = Field(..., description="Most popular genres with counts")
    system_health: Literal["healthy", "warning", "error"] = Field("healthy", description="System health status")
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "total_movies": 100,
                "total_ratings": 1000,
                "total_users": 50,
                "average_rating": 3.5,
                "rating_scale": "0.5-5.0",
                "most_popular_genres": [{"genre": "Drama", "count": 25}],
                "system_health": "healthy"
            }
        }