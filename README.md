*# Global Crime Data Scraper

An advanced AI-powered web scraper that extracts crime-related news articles from **40 verified international news sources**, processes them using Natural Language Processing (NLP), and stores structured data with intelligent duplicate detection. Features comprehensive global coverage across 6 continents with hash-based deduplication system.

## 🚀 Key Features

### 🌐 Global News Coverage
- **40 Verified Sources** across 6 continents (North America, Europe, Asia, Latin America, Africa, Australia)
- **International Scope** with sources in multiple languages (English, Spanish, French, Italian, etc.)
- **Real-time Verification** ensures all sources are accessible and working

### 🔍 Advanced Duplicate Detection
- **SHA-256 Content Hashing** for exact duplicate prevention
- **MD5 Similarity Hashing** for cross-source similar content detection
- **Smart Logic**: Blocks same-source exact replicas, keeps cross-source similar content
- **Persistent Storage** of hash information for long-term deduplication

### 🧠 AI-Powered Data Extraction
- **spaCy NLP Processing** extracts key information (who, what, when, where, how, why)
- **Named Entity Recognition** identifies people, locations, organizations
- **Crime Classification** categorizes crime types automatically
- **Economic Impact Detection** extracts financial loss information

### 📊 Professional Data Output
- **Structured CSV Format** with 18 standardized columns
- **Complete Metadata** including source, dates, hashes
- **Data Integrity** with validation and error handling
- **Excel/Pandas Compatible** for professional analysis

## 🌍 Global News Sources

### Regional Coverage (40 Verified Sources)

| Region | Sources | Examples |
|--------|---------|----------|
| **North America** | 16 | AP News, CNN, Fox News, Washington Post, NBC, CBS |
| **Europe** | 6 | Sky News UK, Euronews, Deutsche Welle, Le Monde |
| **Asia** | 5 | Japan Times, Times of India, NDTV, Nikkei Asia |
| **Latin America** | 2 | El Universal Mexico, La Jornada Mexico |
| **Africa** | 1 | Daily Maverick South Africa |
| **Australia/Oceania** | 4 | ABC Australia, Sky News Australia, Nine News |

### Fastest Response Sources
1. **Washington Post Crime** - 0.38s
2. **Times of India Crime** - 0.40s  
3. **Sky News UK Crime** - 0.60s
4. **Fox News Crime** - 0.78s
5. **Chicago Tribune Crime** - 0.78s

## 📁 Project Structure

```
CrimeData/
├── main.py                    # Main application entry point
├── config.py                  # Configuration with 40 global sources
├── verified_sources_config.py # Verified international news sources
├── scraper.py                 # Web scraping functionality
├── nlp_processor.py           # NLP processing and data extraction
├── utils.py                   # Utility functions + duplicate detection
├── scheduler.py               # Automation and scheduling
├── example_websites.py        # Example website configurations
├── requirements.txt           # Python dependencies
├── .gitignore                 # Git ignore file
├── data/                      # Directory for CSV files
│   └── crime_articles.csv     # Main data output with headers
├── logs/                      # Directory for log files
│   └── scraper.log           # Application logs
└── README.md                  # This documentation
```

## 🔧 Installation

### Prerequisites
- Python 3.8+ 
- Internet connection for news scraping
- Minimum 1GB RAM for NLP processing

### Setup Steps

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd CrimeData
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download spaCy language model**:
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. **Test installation**:
   ```bash
   python main.py --mode test
   ```

## 🎯 Usage

### Quick Start

**Test the system** (recommended first run):
```bash
python main.py --mode test
```

**Full global scrape** (all 40 sources):
```bash
python main.py --mode full
```

**Quick sample** (limit articles for testing):
```bash
python main.py --mode full --max-articles 10
```

### Command Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `--mode test` | Test all source connectivity | `python main.py --mode test` |
| `--mode full` | Scrape all verified sources | `python main.py --mode full` |
| `--mode single` | Scrape single source | `python main.py --mode single --website "AP News Crime"` |
| `--mode stats` | Show data statistics | `python main.py --mode stats` |
| `--max-articles N` | Limit articles per source | `python main.py --mode full --max-articles 5` |

### Configuration

The system uses **verified_sources_config.py** with 40 pre-tested international sources. No manual configuration needed for basic usage.

**Custom sources** can be added to `config.py`:
```python
NEWS_WEBSITES = [
    {
        "name": "Custom News Source",
        "url": "https://example.com/crime",
        "article_selector": "article h2 a",
        "headline_selector": "h1",
        "content_selector": "div.content",
        "response_time": 0.0,
        "verified_date": "2025-07-13"
    }
]
```

## ⚙️ Automation

### Scheduling Options

1. **Daily scraping at 9 AM**:
   ```bash
   python scheduler.py --schedule daily --time 09:00
   ```

2. **Hourly scraping**:
   ```bash
   python scheduler.py --schedule hourly
   ```

3. **Custom interval (every 6 hours)**:
   ```bash
   python scheduler.py --schedule custom --hours 6
   ```

### Production Deployment

#### Windows Task Scheduler
1. Open Task Scheduler → Create Basic Task
2. Set trigger (daily/weekly/monthly)
3. Action: Start a program
   - **Program**: `python.exe`
   - **Arguments**: `"C:\path\to\main.py" --mode full`
   - **Start in**: `C:\path\to\CrimeData`

#### Linux/macOS Cron
Add to crontab (`crontab -e`):
```bash
# Daily at 9 AM
0 9 * * * cd /path/to/CrimeData && python main.py --mode full

# Every 6 hours
0 */6 * * * cd /path/to/CrimeData && python main.py --mode full
```

#### Docker Deployment
```bash
# Build image
docker build -t crime-scraper .

# Run with volume for data persistence
docker run -v $(pwd)/data:/app/data crime-scraper
```

## 📊 Data Output

### CSV Structure

The scraper saves data to `data/crime_articles.csv` with **18 standardized columns**:

| Column | Description | Example |
|--------|-------------|---------|
| `date_scraped` | When article was collected | `2025-07-13 02:57:06` |
| `article_url` | Source URL | `https://apnews.com/article/...` |
| `headline` | Article title | `"Colorado dentist accused of poisoning..."` |
| `publication_date` | Original publication date | `"July 23, 2012"` |
| `who` | People/entities (NLP extracted) | `"James Craig; Angela Craig; DENVER"` |
| `what` | Crime types identified | `"murder; fraud; arson; assault"` |
| `where` | Locations mentioned | `"Colorado; Centennial; Aurora"` |
| `when` | Time references | `"2025; July 23, 2012; Monday"` |
| `how` | Methods/descriptions | `"dentist accused of poisoning wife's"` |
| `why` | Motivations (if found) | `""` |
| `economic_loss` | Financial impact | `"$20,000"` |
| `injuries` | Number of injuries | `""` |
| `fatalities` | Number of deaths | `""` |
| `arrests` | Number of arrests | `""` |
| `full_text` | Complete article content | `"Colorado dentist accused..."` |
| `content_hash` | SHA-256 for exact duplicates | `1cf043c3585faa0703230bd4...` |
| `similarity_hash` | MD5 for similar content | `73bcab23a9c6c18b009510fa...` |
| `duplicate_note` | Duplicate detection info | `""` |

### Sample Data
```csv
date_scraped,article_url,headline,publication_date,who,what,where...
2025-07-13 02:57:06,https://apnews.com/article/...,Colorado dentist accused...,July 23 2012,James Craig; Angela Craig,murder; fraud,Colorado; Denver,...
```

### Duplicate Detection Logic

1. **Exact Same Source Duplicates**: ❌ **BLOCKED** (same URL, same content hash)
2. **Cross-Source Similar Content**: ✅ **ALLOWED** (different sources, similar content)
3. **Unique Content**: ✅ **ALLOWED** (new content, new hash)

### Data Quality Features

- **UTF-8 Encoding** for international character support
- **Automatic Header Generation** for CSV compatibility
- **Error Handling** with graceful fallbacks
- **Validation Checks** for data integrity

## 🔒 Ethical Guidelines & Legal Compliance

### Responsible Scraping Practices

✅ **What We Do Right**:
- **Rate Limiting**: Built-in delays between requests (1-2 seconds)
- **Robots.txt Compliance**: Respects website crawling guidelines  
- **Fair Use**: Educational/research purpose data collection
- **Error Handling**: Graceful failures without overwhelming servers
- **Attribution**: Preserves source URLs and publication dates

⚠️ **Important Considerations**:
- **Check Terms of Service** for each news source before commercial use
- **Respect Copyright**: Articles remain property of original publishers
- **Monitor Usage**: Avoid excessive requests that could impact website performance
- **Data Accuracy**: Verify extracted information for critical applications
- **Privacy**: Be mindful of personal information in crime articles

### Data Quality & Bias Awareness

- **Cross-Reference Sources**: Multiple international sources reduce bias
- **Geographic Diversity**: Global coverage prevents regional bias
- **Manual Verification**: Regularly check NLP extraction accuracy
- **Demographic Considerations**: Monitor for potential bias in crime reporting
- **Temporal Validation**: Verify dates and timeline accuracy

### Compliance Checklist

- [ ] Verify robots.txt compliance for new sources
- [ ] Review terms of service for commercial usage
- [ ] Implement additional rate limiting if needed
- [ ] Set up monitoring for extraction accuracy
- [ ] Establish data retention policies
- [ ] Document usage for transparency

## 🛠️ Technical Details

### System Requirements
- **Python**: 3.8+ (tested on 3.9+)
- **Memory**: 1GB+ RAM for NLP processing
- **Storage**: 100MB+ for dependencies, 10MB+ for data
- **Network**: Stable internet connection for scraping

### Dependencies
```
requests>=2.28.0        # HTTP requests for scraping
beautifulsoup4>=4.11.0  # HTML parsing
spacy>=3.4.0           # NLP processing
pandas>=1.5.0          # Data manipulation
schedule>=1.2.0        # Task scheduling
colorama>=0.4.5        # Colored terminal output
python-dateutil>=2.8.0 # Date parsing
```

### Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   main.py       │───▶│   scraper.py     │───▶│  utils.py       │
│ Entry Point     │    │ Web Scraping     │    │ Duplicate Det.  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   config.py     │    │ nlp_processor.py │    │ crime_articles  │
│ Configuration   │    │ NLP Extraction   │    │     .csv        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Performance Metrics
- **Source Testing**: 62.5% global accessibility rate (40/64 sources)
- **Processing Speed**: ~2-5 articles per second per source
- **Memory Usage**: ~200-500MB during operation
- **Network Usage**: ~1-10MB per source depending on article count
- **Response Times**: 0.38s to 3.13s per source (average: 1.2s)

### Error Handling
- **Network Timeouts**: 30s timeout with 3 retries
- **HTML Parsing Errors**: Graceful fallbacks with logging
- **NLP Processing Failures**: Continue with partial data
- **CSV Write Errors**: Atomic operations with rollback
- **Duplicate Detection**: Hash collision handling

## 🚀 Future Enhancements

### Planned Features

#### Vector Database Migration
For large datasets (100k+ articles):
```python
# FAISS Integration Example
import faiss
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(articles)
index = faiss.IndexFlatIP(embeddings.shape[1])
index.add(embeddings)

# Similarity search
query_embedding = model.encode([query])
distances, indices = index.search(query_embedding, k=10)
```

#### Advanced Analytics
- **Sentiment Analysis**: Analyze tone and public sentiment
- **Trend Analysis**: Identify crime patterns over time  
- **Geospatial Mapping**: Interactive crime location mapping
- **Real-time Alerts**: Notifications for specific crime types
- **Language Translation**: Multi-language source support

#### Infrastructure Improvements
- **Containerization**: Docker/Kubernetes deployment
- **Cloud Integration**: AWS/GCP/Azure cloud storage
- **API Development**: REST API for data access
- **Dashboard Creation**: Web-based monitoring interface
- **Machine Learning**: Predictive crime analytics

### Scalability Roadmap

1. **Phase 1**: Current (40 sources, local CSV) ✅
2. **Phase 2**: 100+ sources, database integration
3. **Phase 3**: Real-time processing, API development
4. **Phase 4**: ML analytics, predictive modeling
5. **Phase 5**: Enterprise deployment, commercial licensing

## 🐛 Troubleshooting

### Common Issues & Solutions

#### Installation Problems
```bash
# spaCy model not found
python -m spacy download en_core_web_sm

# Permission errors (Windows)
pip install --user -r requirements.txt

# SSL certificate errors
pip install --trusted-host pypi.org --trusted-host pypi.python.org requests
```

#### Runtime Issues

| Problem | Symptoms | Solution |
|---------|----------|----------|
| **No articles found** | Empty CSV output | Check CSS selectors, verify crime keywords |
| **Network timeouts** | Connection errors | Increase `REQUEST_TIMEOUT` in config.py |
| **Memory errors** | System slowdown | Reduce `--max-articles`, close other applications |
| **CSV encoding** | Special characters broken | Ensure UTF-8 encoding, check locale settings |
| **Duplicate detection** | Hash errors | Clear/regenerate hash columns in CSV |

#### Performance Optimization

```python
# Faster scraping (use with caution)
DELAY_BETWEEN_REQUESTS = 0.5  # Default: 1.0

# Reduce memory usage
MAX_ARTICLES_PER_SOURCE = 10  # Default: unlimited

# Parallel processing (advanced)
from concurrent.futures import ThreadPoolExecutor
```

#### Debugging Steps

1. **Test single source**:
   ```bash
   python main.py --mode single --website "AP News Crime"
   ```

2. **Check logs**:
   ```bash
   cat logs/scraper.log | tail -50
   ```

3. **Verify connectivity**:
   ```bash
   python main.py --mode test
   ```

4. **Reset data** (if needed):
   ```bash
   mv data/crime_articles.csv data/crime_articles_backup.csv
   ```

### Support & Contributing

#### Getting Help
- **Check logs** in `logs/scraper.log` for detailed error information
- **Run tests** with `python main.py --mode test` to verify setup
- **Review error messages** in console output for specific issues

#### Contributing
1. **Fork the repository** and create a feature branch
2. **Add new sources** to `verified_sources_config.py` with proper testing
3. **Enhance NLP patterns** in `nlp_processor.py` for better extraction
4. **Improve error handling** and add comprehensive logging
5. **Submit pull requests** with clear descriptions and test results

#### Development Setup
```bash
# Clone for development
git clone <repository-url>
cd CrimeData

# Install in development mode
pip install -e .

# Run tests
python -m pytest tests/

# Code formatting
black *.py
flake8 *.py
```

## 📄 License & Legal

### License
This project is released under the **MIT License** for educational and research purposes. 

### Legal Disclaimer
- **Educational Use**: Designed for research, journalism, and academic purposes
- **Website Compliance**: Users must verify compliance with individual website terms of service
- **Copyright Respect**: All scraped content remains property of original publishers
- **No Warranty**: Software provided "as-is" without warranty of any kind
- **User Responsibility**: Users are responsible for legal compliance in their jurisdiction

### Attribution
When using data from this scraper:
- **Cite Original Sources**: Always attribute articles to original publishers
- **Preserve URLs**: Maintain source links for transparency
- **Academic Citation**: Include this project in academic references if used for research

## 📊 Project Status

### Current Version: 2.0.0
- ✅ **Global Coverage**: 40 verified international sources
- ✅ **Duplicate Detection**: Advanced hash-based system
- ✅ **Production Ready**: Comprehensive error handling and logging
- ✅ **Data Quality**: Professional CSV output with headers
- ✅ **Documentation**: Complete setup and usage guides

### Statistics
- **🌍 Global Sources**: 40 verified across 6 continents
- **📈 Success Rate**: 62.5% source accessibility 
- **🔍 Data Points**: 18 standardized CSV columns
- **⚡ Performance**: 0.38s - 3.13s response times
- **🛡️ Reliability**: Advanced duplicate detection with SHA-256/MD5 hashing

### Repository Health
- **📝 Documentation**: Comprehensive README and inline comments
- **🧪 Testing**: Source verification and connectivity testing
- **🔧 Maintenance**: Active development and updates
- **🌐 Community**: Open source with contribution guidelines
- **📦 Dependencies**: Well-maintained, regularly updated libraries

---

**⭐ Star this repository if you find it useful!**  
**🐛 Report issues or suggest enhancements via GitHub Issues**  
**🤝 Contributions welcome - see Contributing section above**

Built with ❤️ for the global journalism and research community.
*