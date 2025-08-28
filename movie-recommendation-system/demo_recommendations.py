"""
Demo script to showcase the Movie Recommendation System
Shows recommendations for different users and algorithms
"""

import requests
import json
import time

API_BASE = "http://localhost:8000"

def print_separator():
    print("=" * 80)

def print_header(title):
    print_separator()
    print(f"🎬 {title.center(76)} 🎬")
    print_separator()

def get_recommendations(user_id, algorithm, num_recommendations=5):
    """Get recommendations from the API"""
    try:
        response = requests.post(f"{API_BASE}/recommend", json={
            "user_id": user_id,
            "num_recommendations": num_recommendations,
            "algorithm": algorithm
        })
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return None

def display_recommendations(data):
    """Display recommendations in a nice format"""
    if not data:
        return
    
    print(f"👤 User ID: {data['user_id']}")
    print(f"🤖 Algorithm: {data['algorithm_used'].upper()}")
    print(f"🎯 Accuracy: {data['accuracy_score']*100:.1f}%")
    print(f"⏱️  Execution Time: {data['execution_time_ms']:.1f}ms")
    print(f"🎬 Total Recommendations: {data['total_recommendations']}")
    print()
    
    for i, movie in enumerate(data['recommendations'], 1):
        stars = "⭐" * int(movie['predicted_rating'])
        genres = " | ".join(movie['genres'])
        print(f"{i:2d}. 🎭 {movie['title']} ({movie['year'] or 'Unknown'})")
        print(f"     📊 Rating: {movie['predicted_rating']}/5.0 {stars}")
        print(f"     🎪 Genres: {genres}")
        print(f"     📈 Confidence: {movie['confidence_score']*100:.1f}%")
        print()

def get_system_stats():
    """Get and display system statistics"""
    try:
        response = requests.get(f"{API_BASE}/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"🎬 Movies in Database: {stats['total_movies']}")
            print(f"⭐ Total Ratings: {stats['total_ratings']}")
            print(f"👥 Total Users: {stats['total_users']}")
            print(f"📊 Average Rating: {stats['average_rating']}/5.0")
            print(f"📏 Rating Scale: {stats['rating_scale']}")
            print(f"💚 System Health: {stats['system_health'].upper()}")
            print()
            print("🏆 Most Popular Genres:")
            for genre in stats['most_popular_genres'][:5]:
                print(f"   • {genre['genre']}: {genre['count']} movies")
        else:
            print(f"❌ Error getting stats: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection error: {e}")

def main():
    print_header("MOVIE RECOMMENDATION SYSTEM DEMO")
    
    # Check if API is running
    try:
        response = requests.get(f"{API_BASE}/health")
        if response.status_code != 200:
            print("❌ API is not running! Please start the server first.")
            return
    except:
        print("❌ Cannot connect to API! Please make sure the server is running on http://localhost:8000")
        return
    
    # Display system stats
    print("📊 SYSTEM STATISTICS")
    print("-" * 40)
    get_system_stats()
    
    # Demo different algorithms for different users
    algorithms = ["collaborative", "svd", "kmeans"]
    users = [1, 5, 10]
    
    for user_id in users:
        for algorithm in algorithms:
            print_header(f"RECOMMENDATIONS FOR USER {user_id} - {algorithm.upper()} ALGORITHM")
            
            data = get_recommendations(user_id, algorithm, 6)
            if data:
                display_recommendations(data)
            
            time.sleep(0.5)  # Small delay between requests
    
    print_header("DEMO COMPLETED")
    print("🌟 Visit http://localhost:8000 for the interactive web interface! 🌟")
    print_separator()

if __name__ == "__main__":
    main()