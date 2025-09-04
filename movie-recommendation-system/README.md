# 🎬 Movie Recommendation System







A modern, user-friendly movie recommendation system that accepts **movie names**, **genres**, and **actor names** as input instead of confusing user IDs. Built with FastAPI and clean OOP principles.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)

## ✨ Features

### 🎭 **Natural Input Methods**
- **🎬 Movie-based**: "Find movies similar to The Matrix"
- **🎪 Genre-based**: "Show me top Action movies" 
- **🎭 Actor-based**: "Movies featuring Tom Hanks"

### 🤖 **Advanced ML Algorithms**
- **Smart Algorithm**: Collaborative filtering for personalized recommendations
- **Advanced Algorithm**: SVD matrix factorization for complex patterns
- **Popular Algorithm**: KMeans clustering for trending movies

### 🎨 **Beautiful Web Interface**
- **Glass morphism design** with gradient backgrounds
- **Responsive layout** that works on all devices
- **Real-time recommendations** with loading animations
- **Interactive controls** for algorithm selection

### 🏗️ **Clean Architecture**
- **SOLID principles** throughout the codebase
- **Type safety** with Pydantic validation
- **Separation of concerns** with dependency injection
- **Production-ready** error handling and logging

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone/Download the project**
   ```bash
   cd movie-recommender
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the server**
   ```bash
   python app.py
   ```

4. **Open your browser**
   ```
   http://localhost:8000
   ```

## 🎯 How to Use

### 🌐 Web Interface (Recommended)

1. **Visit** `http://localhost:8000`
2. **Choose input type**: Movie, Genre, or Actor
3. **Enter your preference**:
   - Movie: "The Matrix", "Inception", "Forrest Gump"
   - Genre: Action, Comedy, Drama, Sci-Fi
   - Actor: "Tom Hanks", "Leonardo DiCaprio"
4. **Select algorithm**: Smart, Advanced, or Popular
5. **Click "Get Movies"** for instant recommendations!

### 📡 API Usage

#### Movie-based Recommendations
```bash
curl -X POST "http://localhost:8000/recommend" \
  -H "Content-Type: application/json" \
  -d '{
    "movie_name": "The Matrix",
    "num_recommendations": 5,
    "algorithm": "collaborative"
  }'
```

#### Genre-based Recommendations
```bash
curl -X POST "http://localhost:8000/recommend" \
  -H "Content-Type: application/json" \
  -d '{
    "genre": "Action",
    "num_recommendations": 10,
    "algorithm": "collaborative"
  }'
```

#### Actor-based Recommendations
```bash
curl -X POST "http://localhost:8000/recommend" \
  -H "Content-Type: application/json" \
  -d '{
    "actor_name": "Tom Hanks",
    "num_recommendations": 8,
    "algorithm": "collaborative"
  }'
```

### 📊 Sample Response
```json
{
  "input_type": "movie",
  "input_value": "The Matrix",
  "recommendations": [
    {
      "movie_id": 7,
      "title": "The Dark Knight",
      "genres": ["Action", "Crime", "Drama"],
      "year": 2008,
      "predicted_rating": 4.5,
      "confidence_score": 0.89
    }
  ],
  "algorithm_used": "collaborative",
  "total_recommendations": 5,
  "accuracy_score": 0.85,
  "execution_time_ms": 45.2
}
```

## 📁 Project Structure

```
movie-recommender/
├── 🎬 app.py                    # Main FastAPI application
├── 🤖 recommendation_engine.py  # ML algorithms & recommendation logic
├── 📋 models.py                 # Pydantic data models with validation
├── 🎨 static/index.html         # Beautiful web interface
├── 📊 data_generator.py         # Sample data generation
├── 🎯 demo_new_ui.py           # Command-line demo script
├── 📦 requirements.txt          # Python dependencies
├── 🎭 movies.csv               # Sample movie data
├── ⭐ ratings.csv              # Sample rating data
└── 📖 README.md                # This file
```

## 🎮 Interactive Demo

Run the command-line demo to see all features:

```bash
python demo_new_ui.py
```

This will demonstrate:
- Movie-based recommendations for "The Matrix", "Forrest Gump", "Inception"
- Genre-based recommendations for Action, Comedy, Drama, Sci-Fi
- Actor-based recommendations for "Tom Hanks", "Leonardo DiCaprio", "Meryl Streep"

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Beautiful web interface |
| `/recommend` | POST | Get personalized recommendations |
| `/movies` | GET | List all available movies |
| `/stats` | GET | System statistics |
| `/health` | GET | Health check |

## 🎪 Available Genres

- Action
- Adventure  
- Animation
- Comedy
- Crime
- Drama
- Fantasy
- Horror
- Romance
- Sci-Fi
- Thriller

## 🤖 Machine Learning Algorithms

### 1. **Smart (Collaborative Filtering)**
- **Best for**: Personalized recommendations based on similar users
- **How it works**: Finds users with similar preferences and recommends movies they liked
- **Use case**: "Users who liked The Matrix also enjoyed..."

### 2. **Advanced (SVD Matrix Factorization)**
- **Best for**: Complex pattern recognition and sparse data
- **How it works**: Decomposes user-movie matrix to find latent factors
- **Use case**: Discovering hidden preferences and niche recommendations

### 3. **Popular (KMeans Clustering)**
- **Best for**: Trending movies and group preferences
- **How it works**: Clusters users into groups and recommends popular movies within clusters
- **Use case**: "Movies trending among users with similar tastes"

## 🎨 UI Features

### 🌟 Modern Design
- **Glass morphism** effects with backdrop blur
- **Gradient backgrounds** for visual appeal
- **Smooth animations** and transitions
- **Responsive design** for all screen sizes

### 🎮 Interactive Elements
- **Tab-based input selection** (Movie/Genre/Actor)
- **Real-time validation** and error messages
- **Loading animations** during processing
- **Star ratings** and confidence indicators
- **Movie cards** with hover effects

### 📱 Mobile Friendly
- **Touch-optimized** interface
- **Responsive breakpoints** for tablets and phones
- **Fast loading** with optimized assets

## 📊 Performance

- **Startup Time**: ~2-3 seconds
- **Recommendation Speed**: 50-200ms
- **Memory Usage**: ~50MB for sample dataset
- **Concurrent Users**: Supports multiple simultaneous requests

## 🔍 Example Queries

### 🎬 Movie-based
- "Matrix" → Returns sci-fi action movies
- "Forrest Gump" → Returns drama/comedy movies
- "Inception" → Returns mind-bending thrillers

### 🎪 Genre-based
- "Action" → Top-rated action movies by popularity
- "Comedy" → Highest-rated comedies
- "Drama" → Award-winning dramatic films

### 🎭 Actor-based (Demo)
- "Tom Hanks" → Popular movies (simulated)
- "Leonardo DiCaprio" → Trending films (simulated)
- "Meryl Streep" → Classic performances (simulated)

## 🛠️ Development

### Adding New Features

1. **New Algorithm**: Implement in `recommendation_engine.py`
2. **New Input Type**: Add to `models.py` and update API
3. **UI Changes**: Modify `static/index.html`
4. **API Endpoints**: Add to `app.py`

### Code Quality
- **Type hints** throughout the codebase
- **Pydantic validation** for all inputs
- **Error handling** with proper HTTP status codes
- **Logging** for debugging and monitoring

## 🧪 Testing

### Manual Testing
```bash
# Test the web interface
start http://localhost:8000

# Test API endpoints
python demo_new_ui.py
```

### API Testing
```bash
# Health check
curl http://localhost:8000/health

# Get movie list
curl http://localhost:8000/movies

# Get system stats
curl http://localhost:8000/stats
```

## 🎯 Use Cases

### 🏠 Personal Use
- **Movie nights**: Find similar movies to ones you enjoyed
- **Genre exploration**: Discover top movies in new genres
- **Actor filmography**: Explore an actor's best works

### 🏢 Business Applications
- **Streaming platforms**: Personalized content recommendations
- **Movie databases**: Enhanced search and discovery
- **Entertainment apps**: User engagement features

### 🎓 Educational
- **ML learning**: Study recommendation algorithms
- **API development**: Example of clean FastAPI architecture
- **UI/UX**: Modern web interface patterns

## 🔧 Configuration

The system works out-of-the-box with sample data, but you can customize:

- **Port**: Change in `app.py` (default: 8000)
- **Algorithm parameters**: Modify in `recommendation_engine.py`
- **UI styling**: Update `static/index.html`
- **Sample data**: Replace `movies.csv` and `ratings.csv`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes following the existing code style
4. Test your changes thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🎬 Screenshots

### Main Interface
![Main Interface](screenshot-main.png)

### Movie Recommendations
![Movie Recommendations](screenshot-movies.png)

### Genre Selection
![Genre Selection](screenshot-genres.png)

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

---

**Built with ❤️ using FastAPI, Pandas, Scikit-learn, and modern web technologies.**

*No more confusing user IDs - just natural, intuitive movie discovery!* 🎬✨
