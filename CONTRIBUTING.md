# Contributing to Jukeyman Autonomous Media Station (JAMS)

Thank you for your interest in contributing to JAMS! This document provides guidelines and instructions for contributing.

## 🎯 Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Follow professional standards

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Git
- NVIDIA GPU (for AI generation features)

### Development Setup

```bash
# 1. Fork the repository
# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/jams.git
cd jams

# 3. Create a branch
git checkout -b feature/your-feature-name

# 4. Set up development environment
python3.11 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt

# 5. Copy environment file
cp .env.example .env
# Edit .env with your configuration

# 6. Start services
docker-compose up -d postgres redis
./scripts/start_all_services.sh
```

## 📝 Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions/updates

### 2. Make Your Changes

- Write clean, readable code
- Follow PEP 8 (Python) and ESLint (JavaScript) standards
- Add comments for complex logic
- Update documentation as needed

### 3. Write Tests

```bash
# Run tests
cd backend
pytest

# Run with coverage
pytest --cov=app --cov-report=html
```

### 4. Commit Your Changes

```bash
git add .
git commit -m "feat: add new image generation endpoint"
```

Commit message format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `style:` - Code style changes
- `refactor:` - Code refactoring
- `test:` - Tests
- `chore:` - Maintenance

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## 🧪 Testing Guidelines

### Backend Tests

```python
# Example test structure
def test_image_generation():
    # Arrange
    prompt = "test prompt"
    
    # Act
    result = generate_image(prompt)
    
    # Assert
    assert result.status == "completed"
    assert result.output_url is not None
```

### API Tests

```python
def test_api_endpoint(client):
    response = client.post(
        "/api/v1/generate/image",
        json={"prompt": "test"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
```

## 📚 Documentation

### Code Documentation

- Use docstrings for all functions and classes
- Follow Google-style docstrings
- Include type hints

```python
def generate_image(
    prompt: str,
    width: int = 1024,
    height: int = 1024
) -> Dict[str, Any]:
    """
    Generate an image using ComfyUI.
    
    Args:
        prompt: Text description of the image
        width: Image width in pixels
        height: Image height in pixels
        
    Returns:
        Dictionary containing generation result with output_url
        
    Raises:
        ValueError: If prompt is empty
        ConnectionError: If ComfyUI is unavailable
    """
    pass
```

### README Updates

- Update README.md for significant changes
- Add examples for new features
- Update installation instructions if needed

## 🎨 Code Style

### Python

- Follow PEP 8
- Use Black for formatting
- Maximum line length: 100 characters
- Use type hints

```bash
# Format code
black backend/app/

# Check style
flake8 backend/app/
```

### TypeScript/JavaScript

- Follow ESLint rules
- Use Prettier for formatting
- Use TypeScript for type safety

## 🐛 Reporting Bugs

### Bug Report Template

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
- OS: [e.g., Ubuntu 22.04]
- Python version: [e.g., 3.11]
- GPU: [e.g., RTX 4090]

**Additional context**
Add any other context about the problem.
```

## 💡 Feature Requests

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
A clear description of the problem.

**Describe the solution you'd like**
What you want to happen.

**Describe alternatives you've considered**
Alternative solutions or features.

**Additional context**
Any other context or screenshots.
```

## 🔍 Review Process

1. **Automated Checks** - CI/CD will run tests and linting
2. **Code Review** - Maintainers will review your PR
3. **Feedback** - Address any requested changes
4. **Merge** - Once approved, your PR will be merged

### Review Checklist

- [ ] Code follows style guidelines
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
- [ ] Security considerations addressed

## 🏗️ Architecture Guidelines

### Adding New AI Engines

1. Create service in `backend/app/services/`
2. Add configuration in `backend/app/core/config.py`
3. Create API endpoint in `backend/app/api/v1/`
4. Add Celery task in `backend/app/tasks/`
5. Update documentation

### Adding New Agents

1. Add agent config in `backend/app/agents/swarm_config.py`
2. Update orchestrator if needed
3. Add tests
4. Update documentation

## 📦 Release Process

Releases are managed by maintainers. Version numbers follow [Semantic Versioning](https://semver.org/).

- **MAJOR** - Breaking changes
- **MINOR** - New features (backward compatible)
- **PATCH** - Bug fixes

## 🤝 Community

- **GitHub Discussions** - For questions and discussions
- **GitHub Issues** - For bugs and feature requests
- **Email** - support@rjbusinesssolutions.org

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to JAMS!** 🚀

*Built by [RJ Business Solutions](https://rjbusinesssolutions.org/) | Architect: Rick Jefferson*

