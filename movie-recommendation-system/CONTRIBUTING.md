# Contributing to Movie Recommendation System

Thank you for your interest in contributing to our movie recommendation system! 🎬

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Git
- Basic knowledge of FastAPI and machine learning

### Setup Development Environment

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/your-username/movie-recommendation-system.git
   cd movie-recommendation-system
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Test the web interface**
   ```
   http://localhost:8000
   ```

## 🎯 How to Contribute

### 🐛 Bug Reports
- Use the issue tracker to report bugs
- Include steps to reproduce the issue
- Provide system information (OS, Python version)
- Include screenshots if relevant

### ✨ Feature Requests
- Check existing issues to avoid duplicates
- Clearly describe the proposed feature
- Explain the use case and benefits
- Consider backward compatibility

### 🔧 Code Contributions

#### 1. **Choose an Issue**
- Look for issues labeled `good first issue` or `help wanted`
- Comment on the issue to let others know you're working on it

#### 2. **Create a Branch**
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

#### 3. **Make Your Changes**
- Follow the existing code style
- Add type hints for all functions
- Include docstrings for new functions
- Update tests if applicable

#### 4. **Test Your Changes**
```bash
# Run the application
python app.py

# Test the web interface
# Test API endpoints
python demo_new_ui.py
```

#### 5. **Commit Your Changes**
```bash
git add .
git commit -m "feat: add new recommendation algorithm"
# or
git commit -m "fix: resolve genre filtering issue"
```

#### 6. **Push and Create Pull Request**
```bash
git push origin your-branch-name
```

Then create a pull request on GitHub.

## 📝 Code Style Guidelines

### Python Code Style
- Follow PEP 8
- Use type hints for all function parameters and return values
- Maximum line length: 100 characters
- Use meaningful variable and function names

### Example:
```python
def get_movie_recommendations(
    movie_name: str, 
    num_recommendations: int = 10
) -> List[MovieRecommendation]:
    """
    Get movie recommendations based on movie name.
    
    Args:
        movie_name: Name of the movie to find similar movies
        num_recommendations: Number of recommendations to return
        
    Returns:
        List of MovieRecommendation objects
    """
    # Implementation here
    pass
```

### HTML/CSS Style
- Use semantic HTML elements
- Follow responsive design principles
- Use consistent class naming (BEM methodology preferred)
- Comment complex CSS rules

## 🧪 Testing Guidelines

### Manual Testing
- Test all input types (movie, genre, actor)
- Test different algorithms (Smart, Advanced, Popular)
- Test error scenarios (invalid inputs, server errors)
- Test responsive design on different screen sizes

### API Testing
```bash
# Test movie-based recommendations
curl -X POST "http://localhost:8000/recommend" \
  -H "Content-Type: application/json" \
  -d '{"movie_name": "The Matrix", "num_recommendations": 5}'

# Test genre-based recommendations
curl -X POST "http://localhost:8000/recommend" \
  -H "Content-Type: application/json" \
  -d '{"genre": "Action", "num_recommendations": 5}'
```

## 📂 Project Structure

```
movie-recommendation-system/
├── app.py                    # Main FastAPI application
├── recommendation_engine.py  # ML algorithms
├── models.py                 # Pydantic data models
├── data_generator.py         # Sample data generation
├── static/
│   └── index.html           # Web interface
├── movies.csv               # Sample movie data
├── ratings.csv              # Sample rating data
├── requirements.txt         # Dependencies
└── README.md               # Documentation
```

## 🎨 Adding New Features

### Adding a New Recommendation Algorithm

1. **Create the algorithm class** in `recommendation_engine.py`
2. **Add it to the main engine** in the `get_recommendations` method
3. **Update the models** in `models.py` if needed
4. **Add UI support** in `static/index.html`
5. **Update documentation** in `README.md`

### Adding a New Input Type

1. **Update the request model** in `models.py`
2. **Add processing logic** in `recommendation_engine.py`
3. **Update the API endpoint** in `app.py`
4. **Add UI controls** in `static/index.html`
5. **Test thoroughly** with various inputs

## 🔍 Code Review Process

### For Contributors
- Ensure your code follows the style guidelines
- Add appropriate comments and docstrings
- Test your changes thoroughly
- Update documentation if needed

### For Reviewers
- Check code quality and style
- Verify functionality works as expected
- Ensure backward compatibility
- Review security implications

## 📋 Commit Message Guidelines

Use conventional commit format:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

Examples:
```
feat: add actor-based recommendation algorithm
fix: resolve genre filtering case sensitivity issue
docs: update API documentation with new endpoints
style: format code according to PEP 8
refactor: extract similarity calculation into separate class
```

## 🎉 Recognition

Contributors will be recognized in:
- README.md contributors section
- GitHub contributors page
- Release notes for significant contributions

## 💬 Getting Help

- Create an issue for questions
- Join our discussions on GitHub
- Check existing issues and documentation first

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for helping make this movie recommendation system better! 🎬✨