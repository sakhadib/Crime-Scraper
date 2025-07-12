# Crime Data Scraper

An AI-powered web scraper that extracts crime-related news articles from news websites, processes them using Natural Language Processing (NLP), and stores structured data in CSV format.

## Features

- **Web Scraping**: Automatically scrapes news websites for crime-related articles
- **NLP Processing**: Uses spaCy to extract key information (who, what, when, where, how, why)
- **Data Storage**: Saves structured data in CSV format with deduplication
- **Automation**: Schedule scraping at regular intervals
- **Error Handling**: Robust error handling with logging and retry mechanisms
- **Scalable**: Modular design allows easy expansion to more websites and features

## Installation

1. **Clone or download the project files**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download spaCy language model**:
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Project Structure

```
CrimeData/
├── main.py              # Main application entry point
├── config.py            # Configuration settings
├── scraper.py           # Web scraping functionality
├── nlp_processor.py     # NLP processing and data extraction
├── utils.py             # Utility functions
├── scheduler.py         # Automation and scheduling
├── example_websites.py  # Example website configurations
├── requirements.txt     # Python dependencies
├── data/               # Directory for CSV files
├── logs/               # Directory for log files
└── README.md           # This file
```

## Usage

### Basic Usage

1. **Configure websites** in `config.py`:
   ```python
   NEWS_WEBSITES = [
       {
           "name": "Example News",
           "url": "https://example.com/news",
           "article_selector": "article h2 a",
           "headline_selector": "h1",
           "content_selector": "div.content"
       }
   ]
   ```

2. **Run the scraper**:
   ```bash
   python main.py
   ```

### Command Line Options

- **Full scrape** (all websites):
  ```bash
  python main.py --mode full
  ```

- **Single website scrape**:
  ```bash
  python main.py --mode single --website "Example News"
  ```

- **Test configuration**:
  ```bash
  python main.py --mode test
  ```

- **View statistics**:
  ```bash
  python main.py --mode stats
  ```

### Automation

1. **Schedule daily scraping at 9 AM**:
   ```bash
   python scheduler.py --schedule daily --time 09:00
   ```

2. **Schedule hourly scraping**:
   ```bash
   python scheduler.py --schedule hourly
   ```

3. **Schedule every 6 hours**:
   ```bash
   python scheduler.py --schedule custom --hours 6
   ```

## Configuration

### Website Configuration

Each website requires the following configuration in `config.py`:

- `name`: Unique identifier for the website
- `url`: Main page URL to scrape
- `article_selector`: CSS selector for article links
- `headline_selector`: CSS selector for article headlines
- `content_selector`: CSS selector for article content

### Crime Keywords

Modify `CRIME_KEYWORDS` in `config.py` to add or remove crime-related terms:

```python
CRIME_KEYWORDS = [
    "robbery", "theft", "murder", "assault", 
    "vandalism", "shooting", "arrest", ...
]
```

## Data Output

The scraper saves data to `data/crime_articles.csv` with the following columns:

- `date_scraped`: When the article was scraped
- `article_url`: Original article URL
- `headline`: Article headline
- `publication_date`: When the article was published
- `who`: People involved (extracted using NER)
- `what`: Type of crime
- `where`: Location (extracted using NER)
- `when`: Date/time of incident
- `how`: Method or description
- `why`: Motivation (if available)
- `economic_loss`: Monetary loss (if mentioned)
- `injuries`: Number of injuries
- `fatalities`: Number of fatalities
- `arrests`: Number of arrests
- `full_text`: Complete article text

## Automation Setup

### Windows Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (daily/weekly/monthly)
4. Set action to start a program:
   - Program: `python.exe`
   - Arguments: `path\\to\\main.py --mode full`
   - Start in: `path\\to\\CrimeData`

### Linux/macOS Cron

Add to crontab (`crontab -e`):

```bash
# Run daily at 9 AM
0 9 * * * cd /path/to/CrimeData && python main.py --mode full

# Run every 6 hours
0 */6 * * * cd /path/to/CrimeData && python main.py --mode full
```

## Ethical Considerations

### Important Guidelines

1. **Respect robots.txt**: Always check website robots.txt files
2. **Rate limiting**: Built-in delays between requests (configurable)
3. **Terms of service**: Respect website terms of service
4. **Data accuracy**: Verify extracted data accuracy
5. **Privacy**: Be mindful of personal information in articles
6. **Bias detection**: Monitor for potential bias in crime reporting

### Data Quality

- Implement validation checks for extracted data
- Regular manual verification of NLP accuracy
- Monitor for false positives in crime classification
- Consider demographic bias in crime reporting

## Error Handling

The scraper includes comprehensive error handling:

- **Network errors**: Automatic retries with exponential backoff
- **Parse errors**: Graceful handling of malformed HTML
- **Missing data**: Default values for missing fields
- **Logging**: Detailed logs in `logs/scraper.log`

## Future Enhancements

### Vector Database Migration

When the dataset grows large (100k+ articles), consider migrating to a vector database:

1. **FAISS Integration**:
   ```python
   import faiss
   from sentence_transformers import SentenceTransformer
   
   # Create embeddings
   model = SentenceTransformer('all-MiniLM-L6-v2')
   embeddings = model.encode(articles)
   
   # Build FAISS index
   index = faiss.IndexFlatIP(embeddings.shape[1])
   index.add(embeddings)
   ```

2. **Similarity Search**:
   ```python
   # Search for similar crimes
   query_embedding = model.encode([query])
   distances, indices = index.search(query_embedding, k=10)
   ```

### Advanced Features

- **Image processing**: Extract images from articles
- **Sentiment analysis**: Analyze tone and sentiment
- **Trend analysis**: Identify crime patterns over time
- **Geospatial analysis**: Map crime locations
- **Real-time alerts**: Notify on specific crime types

## Troubleshooting

### Common Issues

1. **spaCy model not found**:
   ```bash
   python -m spacy download en_core_web_sm
   ```

2. **Network timeouts**:
   - Increase `REQUEST_TIMEOUT` in config.py
   - Check internet connection
   - Verify website accessibility

3. **No articles found**:
   - Check CSS selectors for target websites
   - Verify crime keywords are appropriate
   - Test individual website configurations

4. **CSV encoding issues**:
   - Ensure UTF-8 encoding
   - Check for special characters in text

### Performance Optimization

- Adjust `DELAY_BETWEEN_REQUESTS` for faster/slower scraping
- Use multiple processes for large-scale scraping
- Implement caching for frequently accessed data

## Contributing

1. Add new website configurations to `example_websites.py`
2. Enhance NLP patterns in `nlp_processor.py`
3. Improve error handling and logging
4. Add new data extraction features

## License

This project is for educational and research purposes. Ensure compliance with website terms of service and local laws when scraping data.

## Support

For issues and questions:

1. Check the logs in `logs/scraper.log`
2. Run configuration test: `python main.py --mode test`
3. Verify website accessibility
4. Review error messages in console output
