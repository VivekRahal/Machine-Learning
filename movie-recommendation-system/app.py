"""
Simple Movie Recommendation API - Working Version
Clean implementation with proper OOP design.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import pandas as pd
from typing import List
import logging

from models import (
    RecommendationRequest, 
    RecommendationResponse, 
    Movie,
    AlgorithmType
)
from recommendation_engine import MovieRecommendationEngine
from data_generator import generate_sample_data

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Movie Recommendation System",
    description="A clean, maintainable movie recommendation API",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Global variables
movies_df = None
ratings_df = None
recommendation_engine = None


@app.on_event("startup")
async def startup_event():
    """Initialize the recommendation engine on startup."""
    global recommendation_engine, movies_df, ratings_df
    
    logger.info("🚀 Starting Movie Recommendation System...")
    
    try:
        # Try to load existing data
        movies_df = pd.read_csv('movies.csv')
        ratings_df = pd.read_csv('ratings.csv')
        logger.info(f"✅ Loaded existing data: {len(movies_df)} movies, {len(ratings_df)} ratings")
    except:
        # Generate sample data
        logger.info("📝 Generating sample data...")
        movies_df, ratings_df = generate_sample_data()
        movies_df.to_csv('movies.csv', index=False)
        ratings_df.to_csv('ratings.csv', index=False)
        logger.info(f"✅ Generated {len(movies_df)} movies and {len(ratings_df)} ratings")
    
    # Initialize recommendation engine
    recommendation_engine = MovieRecommendationEngine(movies_df, ratings_df)
    logger.info("✅ Recommendation system initialized successfully!")


@app.get("/")
async def root():
    """Serve the main UI page."""
    return FileResponse('static/index.html')

@app.get("/api")
async def api_info():
    """API information endpoint."""
    return {
        "message": "Welcome to Movie Recommendation System",
        "description": "A clean, maintainable movie recommendation API",
        "version": "2.0.0",
        "algorithms": [algo.value for algo in AlgorithmType],
        "endpoints": {
            "GET /movies": "List all available movies",
            "POST /recommend": "Get movie recommendations",
            "GET /health": "Health check"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "movies_count": len(movies_df) if movies_df is not None else 0,
        "ratings_count": len(ratings_df) if ratings_df is not None else 0,
        "engine_ready": recommendation_engine is not None
    }


@app.get("/movies", response_model=List[Movie])
async def get_movies():
    """Get list of all available movies."""
    if movies_df is None:
        raise HTTPException(status_code=500, detail="Movies data not initialized")
    
    try:
        movies_list = []
        for _, row in movies_df.iterrows():
            genres = row['genres']
            if isinstance(genres, str) and genres.startswith('['):
                import ast
                try:
                    genres = ast.literal_eval(genres)
                except:
                    genres = [genres]
            elif not isinstance(genres, list):
                genres = [str(genres)]
            
            movies_list.append(Movie(
                movie_id=int(row['movie_id']),
                title=row['title'],
                genres=genres,
                year=int(row['year']) if pd.notna(row.get('year')) else None
            ))
        
        return movies_list
        
    except Exception as e:
        logger.error(f"Error retrieving movies: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving movies")


@app.post("/recommend", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    """Get movie recommendations based on movie name, genre, or actor."""
    if recommendation_engine is None:
        raise HTTPException(status_code=500, detail="Recommendation engine not initialized")
    
    try:
        # Get recommendations from engine
        recommendations, execution_time, input_type, input_value = recommendation_engine.get_recommendations(
            movie_name=request.movie_name,
            genre=request.genre,
            actor_name=request.actor_name,
            num_recommendations=request.num_recommendations,
            algorithm=request.algorithm.value
        )
        
        # Calculate a simple accuracy score based on confidence
        if recommendations:
            accuracy_score = sum(rec.confidence_score for rec in recommendations) / len(recommendations)
        else:
            accuracy_score = 0.0
        
        return RecommendationResponse(
            input_type=input_type,
            input_value=input_value,
            recommendations=recommendations,
            algorithm_used=request.algorithm,
            total_recommendations=len(recommendations),
            accuracy_score=round(accuracy_score, 3),
            execution_time_ms=round(execution_time, 2)
        )
        
    except Exception as e:
        logger.error(f"Error generating recommendations: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")


@app.get("/stats")
async def get_system_stats():
    """Get system statistics."""
    if recommendation_engine is None:
        raise HTTPException(status_code=500, detail="Recommendation engine not initialized")
    
    try:
        stats = recommendation_engine.get_system_stats()
        return stats
        
    except Exception as e:
        logger.error(f"Error retrieving system stats: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving system statistics")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")