"""
Configuration file for the Crime Data Scraper
Contains settings for websites, keywords, file paths, and other constants
"""

import os
from typing import List, Dict

# Base directory for the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

# Create directories if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# CSV file path
CSV_FILE_PATH = os.path.join(DATA_DIR, "crime_articles.csv")

# Log file path
LOG_FILE_PATH = os.path.join(LOGS_DIR, "scraper.log")

# Crime-related keywords for filtering articles
CRIME_KEYWORDS = [
    "robbery", "theft", "burglary", "vandalism", "murder", "homicide", 
    "assault", "battery", "shooting", "stabbing", "arrest", "police",
    "crime", "criminal", "fraud", "embezzlement", "kidnapping", "arson",
    "drug", "trafficking", "violence", "attack", "weapon", "gun",
    "domestic violence", "sexual assault", "rape", "carjacking", "mugging"
]

# List of news websites to scrape
# Note: These are example websites. In production, check robots.txt and terms of service
# Replace with actual local news websites and their correct CSS selectors
NEWS_WEBSITES = [
    {
        "name": "Test Website",
        "url": "https://httpbin.org/html",  # Simple test page
        "article_selector": "h1",  # CSS selector for article links
        "headline_selector": "h1",  # CSS selector for headlines
        "content_selector": "p"  # CSS selector for article content
    }
    # Example configurations (uncomment and modify as needed):
    # {
    #     "name": "BBC News",
    #     "url": "https://www.bbc.com/news",
    #     "article_selector": "h3 a[href*='/news/']",
    #     "headline_selector": "h1",
    #     "content_selector": "div[data-component='text-block']"
    # },
    # {
    #     "name": "Local News Example",
    #     "url": "https://your-local-news.com/crime",
    #     "article_selector": "article h2 a",
    #     "headline_selector": "h1.article-title",
    #     "content_selector": "div.article-content p"
    # }
]

# HTTP request settings
REQUEST_TIMEOUT = 30
MAX_RETRIES = 3
DELAY_BETWEEN_REQUESTS = 1  # seconds

# spaCy model name
SPACY_MODEL = "en_core_web_sm"

# CSV column headers
CSV_COLUMNS = [
    "date_scraped",
    "article_url",
    "headline", 
    "publication_date",
    "who",
    "what",
    "where",
    "when",
    "how",
    "why",
    "economic_loss",
    "injuries",
    "fatalities", 
    "arrests",
    "full_text"
]

# Entity types for spaCy NER
ENTITY_TYPES = {
    "PERSON": "who",
    "GPE": "where",  # Geopolitical entities (cities, countries)
    "LOC": "where",  # Locations
    "DATE": "when",
    "TIME": "when",
    "MONEY": "economic_loss",
    "CARDINAL": "injuries"  # Numbers that could indicate injuries/fatalities
}

# Crime type patterns for classification
CRIME_TYPE_PATTERNS = {
    "robbery": ["robbery", "robbed", "rob", "heist"],
    "theft": ["theft", "stealing", "stolen", "stole", "burglary", "burglar"],
    "assault": ["assault", "assaulted", "attack", "attacked", "beating", "beaten"],
    "murder": ["murder", "killed", "homicide", "death", "died", "fatal"],
    "shooting": ["shooting", "shot", "gunfire", "firearm", "gun"],
    "vandalism": ["vandalism", "vandalized", "graffiti", "damaged", "destroyed"],
    "fraud": ["fraud", "scam", "embezzlement", "forgery", "identity theft"],
    "drug": ["drug", "narcotics", "cocaine", "heroin", "marijuana", "meth"],
    "domestic_violence": ["domestic violence", "domestic abuse", "family violence"],
    "sexual_assault": ["sexual assault", "rape", "sexual abuse"]
}
