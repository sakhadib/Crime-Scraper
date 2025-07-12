# Contributing to Global Crime Data Scraper

Thank you for your interest in contributing to this project! This guide will help you get started.

## 🤝 How to Contribute

### Reporting Issues
- **Search existing issues** before creating new ones
- **Use clear, descriptive titles** for bug reports and feature requests
- **Include system information** (OS, Python version, dependencies)
- **Provide reproduction steps** for bugs
- **Include error logs** when reporting issues

### Suggesting Enhancements
- **Check the roadmap** in README.md to avoid duplicate suggestions
- **Explain the use case** and potential impact
- **Consider implementation complexity** and maintenance burden
- **Provide examples** or mockups when possible

### Contributing Code

#### Setting Up Development Environment
```bash
# Fork and clone the repository
git clone https://github.com/yourusername/crime-data-scraper.git
cd crime-data-scraper

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Test the setup
python main.py --mode test
```

#### Development Workflow
1. **Create feature branch**: `git checkout -b feature/your-feature-name`
2. **Make your changes** following code standards below
3. **Test thoroughly** including edge cases
4. **Update documentation** if needed
5. **Commit with clear messages**: `git commit -m "Add: Feature description"`
6. **Push and create pull request**

## 📝 Code Standards

### Python Style Guide
- **Follow PEP 8** for code formatting
- **Use meaningful variable names** and clear function documentation
- **Add type hints** where applicable
- **Include docstrings** for all functions and classes
- **Keep functions focused** and under 50 lines when possible

### Adding News Sources
When adding new news sources to `verified_sources_config.py`:

```python
{
    "name": "News Source Name",
    "url": "https://example.com/crime-section",
    "article_selector": "CSS_SELECTOR_FOR_ARTICLE_LINKS",
    "headline_selector": "CSS_SELECTOR_FOR_HEADLINES", 
    "content_selector": "CSS_SELECTOR_FOR_CONTENT",
    "response_time": 0.0,  # Will be updated during testing
    "verified_date": "YYYY-MM-DD"
}
```

**Requirements for new sources:**
- Must have clear crime/legal section
- Must be accessible without login/paywall
- Must respect robots.txt
- Must have consistent HTML structure
- Should be from reputable news organization

### Testing Guidelines
- **Test all new sources** thoroughly before submission
- **Verify CSS selectors** work consistently
- **Check data extraction quality** manually
- **Test error handling** with invalid inputs
- **Document any limitations** or special requirements

## 🌍 Priority Contribution Areas

### High Priority
1. **New International Sources**: Especially from underrepresented regions
2. **NLP Improvements**: Better entity extraction and crime classification
3. **Error Handling**: More robust error recovery and reporting
4. **Performance Optimization**: Faster processing and lower memory usage

### Medium Priority
1. **Data Quality**: Enhanced validation and cleaning
2. **Documentation**: Additional examples and tutorials
3. **Testing**: Unit tests and integration tests
4. **Monitoring**: Health checks and performance metrics

### Future Features
1. **Real-time Processing**: Live news monitoring
2. **API Development**: REST API for data access
3. **Dashboard**: Web interface for monitoring
4. **Machine Learning**: Predictive analytics and trend detection

## 📚 Resources

### Helpful Links
- **spaCy Documentation**: https://spacy.io/usage
- **BeautifulSoup Guide**: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- **CSS Selectors Reference**: https://www.w3schools.com/cssref/css_selectors.asp
- **Web Scraping Ethics**: https://blog.apify.com/web-scraping-ethics/

### Project Resources
- **Issue Tracker**: GitHub Issues
- **Documentation**: README.md
- **Changelog**: CHANGELOG.md
- **Code Examples**: example_websites.py

## ✅ Pull Request Checklist

Before submitting your pull request:

- [ ] Code follows PEP 8 style guidelines
- [ ] All tests pass (including new sources)
- [ ] Documentation updated if needed
- [ ] Changelog updated with your changes
- [ ] No sensitive data (API keys, passwords) included
- [ ] Commit messages are clear and descriptive
- [ ] PR description explains changes and motivation

## 🏆 Recognition

Contributors will be recognized in:
- **Project README**: Contributors section
- **Release Notes**: Major contribution acknowledgments
- **Code Comments**: Attribution for significant algorithms or features

## 📞 Getting Help

If you need help with contributing:
- **Check existing documentation** first
- **Search closed issues** for similar questions
- **Create a GitHub issue** with "question" label
- **Be specific** about what you're trying to achieve

Thank you for helping make this project better! 🎉
