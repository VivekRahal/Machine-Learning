"""
Demo script for the new Movie Recommendation System
Shows recommendations based on Movie Names, Genres, and Actors
"""

import requests
import json
import time

API_BASE = "http://localhost:8000"

def print_separator():
    print("🎬" + "="*78 + "🎬")

def print_header(title):
    print_separator()
    print(f"🎭 {title.center(76)} 🎭")
    print_separator()

def test_movie_recommendations():
    print_header("MOVIE-BASED RECOMMENDATIONS")
    
    movies_to_test = ["The Matrix", "Forrest Gump", "Inception"]
    
    for movie in movies_to_test:
        print(f"\n🎬 Finding movies similar to '{movie}'...")
        try:
            response = requests.post(f"{API_BASE}/recommend", json={
                "movie_name": movie,
                "num_recommendations": 5,
                "algorithm": "collaborative"
            })
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Found {len(data['recommendations'])} recommendations:")
                for i, rec in enumerate(data['recommendations'], 1):
                    genres = " | ".join(rec['genres'])
                    print(f"  {i}. {rec['title']} ({rec['year']}) - {genres}")
                    print(f"     ⭐ Rating: {rec['predicted_rating']}/5.0 | Confidence: {rec['confidence_score']*100:.1f}%")
            else:
                print(f"❌ Error: {response.status_code}")
        except Exception as e:
            print(f"❌ Connection error: {e}")
        
        time.sleep(1)

def test_genre_recommendations():
    print_header("GENRE-BASED RECOMMENDATIONS")
    
    genres_to_test = ["Action", "Comedy", "Drama", "Sci-Fi"]
    
    for genre in genres_to_test:
        print(f"\n🎪 Top {genre} movies...")
        try:
            response = requests.post(f"{API_BASE}/recommend", json={
                "genre": genre,
                "num_recommendations": 4,
                "algorithm": "collaborative"
            })
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Found {len(data['recommendations'])} {genre} movies:")
                for i, rec in enumerate(data['recommendations'], 1):
                    print(f"  {i}. {rec['title']} ({rec['year']})")
                    print(f"     ⭐ Rating: {rec['predicted_rating']}/5.0 | Confidence: {rec['confidence_score']*100:.1f}%")
            else:
                print(f"❌ Error: {response.status_code}")
        except Exception as e:
            print(f"❌ Connection error: {e}")
        
        time.sleep(1)

def test_actor_recommendations():
    print_header("ACTOR-BASED RECOMMENDATIONS (DEMO)")
    
    actors_to_test = ["Tom Hanks", "Leonardo DiCaprio", "Meryl Streep"]
    
    for actor in actors_to_test:
        print(f"\n🎭 Movies featuring '{actor}'...")
        try:
            response = requests.post(f"{API_BASE}/recommend", json={
                "actor_name": actor,
                "num_recommendations": 4,
                "algorithm": "collaborative"
            })
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Found {len(data['recommendations'])} popular movies (simulated for {actor}):")
                for i, rec in enumerate(data['recommendations'], 1):
                    genres = " | ".join(rec['genres'])
                    print(f"  {i}. {rec['title']} ({rec['year']}) - {genres}")
                    print(f"     ⭐ Rating: {rec['predicted_rating']}/5.0")
            else:
                print(f"❌ Error: {response.status_code}")
        except Exception as e:
            print(f"❌ Connection error: {e}")
        
        time.sleep(1)

def main():
    print_header("NEW MOVIE RECOMMENDATION SYSTEM DEMO")
    print("🌟 Now supports recommendations based on:")
    print("   📽️  Movie Names - Find similar movies")
    print("   🎪 Genres - Get top movies by genre")
    print("   🎭 Actors - Movies featuring specific actors")
    print()
    
    # Check if API is running
    try:
        response = requests.get(f"{API_BASE}/health")
        if response.status_code != 200:
            print("❌ API is not running! Please start the server first.")
            return
        print("✅ API is running successfully!")
    except:
        print("❌ Cannot connect to API! Please make sure the server is running on http://localhost:8000")
        return
    
    # Test different recommendation types
    test_movie_recommendations()
    test_genre_recommendations() 
    test_actor_recommendations()
    
    print_header("DEMO COMPLETED")
    print("🌟 Visit http://localhost:8000 for the beautiful web interface! 🌟")
    print("🎬 Try different movies, genres, and actors to see personalized recommendations!")
    print_separator()

if __name__ == "__main__":
    main()