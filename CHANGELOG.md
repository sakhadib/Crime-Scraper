# Changelog

All notable changes to the Global Crime Data Scraper project will be documented in this file.

## [2.0.0] - 2025-07-13

### 🌍 Major Global Expansion
- **ADDED**: 40 verified international news sources across 6 continents
- **ADDED**: Regional coverage including North America (16), Europe (6), Asia (5), Latin America (2), Africa (1), Australia/Oceania (4)
- **ADDED**: Comprehensive source testing infrastructure with accessibility verification
- **ADDED**: Response time tracking for performance optimization

### 🔒 Advanced Duplicate Detection
- **ADDED**: SHA-256 content hashing for exact duplicate prevention
- **ADDED**: MD5 similarity hashing for cross-source content detection
- **ADDED**: Smart duplicate logic: blocks same-source exact replicas, keeps cross-source similar content
- **ADDED**: Persistent hash storage in CSV for long-term deduplication

### 📊 Enhanced Data Quality
- **ADDED**: Proper CSV headers with 18 standardized columns
- **ADDED**: Professional data structure compatible with Excel/Pandas
- **ADDED**: Enhanced metadata including source verification dates and response times
- **ADDED**: Improved error handling and data validation

### 🔧 Technical Improvements
- **UPDATED**: Configuration system with verified sources separation
- **UPDATED**: Utils.py with comprehensive duplicate detection functions
- **UPDATED**: NLP processing with enhanced entity extraction
- **ADDED**: .gitignore file for clean repository management
- **ADDED**: Comprehensive documentation and troubleshooting guides

### 🧹 Repository Cleanup
- **REMOVED**: Unnecessary test files and temporary documentation
- **REMOVED**: Old source arrays replaced with verified configurations
- **REMOVED**: Development artifacts and cache files
- **ORGANIZED**: Clean project structure ready for public release

### 📚 Documentation Overhaul
- **REWRITTEN**: Complete README.md with comprehensive usage guide
- **ADDED**: Installation instructions, configuration details, and examples
- **ADDED**: Ethical guidelines and legal compliance section
- **ADDED**: Technical architecture overview and performance metrics
- **ADDED**: Troubleshooting guide and contribution guidelines

## [1.0.0] - 2025-07-12

### Initial Release
- **ADDED**: Basic web scraping functionality for crime news
- **ADDED**: spaCy NLP processing for data extraction
- **ADDED**: CSV output with basic crime data fields
- **ADDED**: Simple configuration system for news sources
- **ADDED**: Basic error handling and logging
- **ADDED**: Command-line interface with multiple modes
- **ADDED**: Scheduling capability for automated scraping

---

## Version Numbering

This project follows [Semantic Versioning](https://semver.org/):
- **MAJOR**: Incompatible API changes or major feature overhauls
- **MINOR**: Backward-compatible functionality additions
- **PATCH**: Backward-compatible bug fixes

## Contributing

When contributing, please:
1. Update this changelog with your changes
2. Follow the established categorization (ADDED, CHANGED, DEPRECATED, REMOVED, FIXED, SECURITY)
3. Include relevant details and impact assessment
4. Reference issue numbers where applicable
