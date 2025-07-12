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
    # Violent crimes
    "robbery", "theft", "burglary", "vandalism", "murder", "homicide", 
    "assault", "battery", "shooting", "stabbing", "arrest", "police",
    "crime", "criminal", "fraud", "embezzlement", "kidnapping", "arson",
    "drug", "trafficking", "violence", "attack", "weapon", "gun",
    "domestic violence", "sexual assault", "rape", "carjacking", "mugging",
    
    # Property crimes
    "shoplifting", "larceny", "pickpocket", "burglary", "breaking and entering",
    "auto theft", "vehicle theft", "stolen car", "stolen vehicle",
    
    # White collar crimes
    "money laundering", "tax evasion", "insider trading", "bribery", "corruption",
    "wire fraud", "mail fraud", "identity theft", "credit card fraud",
    
    # Drug-related crimes
    "drug dealing", "drug possession", "narcotics", "cocaine", "heroin", 
    "marijuana", "meth", "methamphetamine", "fentanyl", "opioid",
    
    # Cyber crimes
    "cybercrime", "hacking", "data breach", "online fraud", "phishing",
    
    # Gang and organized crime
    "gang", "organized crime", "racketeering", "extortion", "protection racket",
    
    # Public order crimes
    "drunk driving", "DUI", "DWI", "disorderly conduct", "public intoxication",
    "vandalism", "graffiti", "trespassing",
    
    # Federal crimes
    "federal crime", "FBI", "DEA", "ATF", "federal investigation",
    
    # Law enforcement terms
    "investigation", "suspect", "detained", "custody", "charges filed",
    "indictment", "conviction", "sentenced", "prison", "jail", "court",
    "trial", "guilty", "plea", "warrant", "manhunt"
]

# List of news websites to scrape
# Note: Always check robots.txt and terms of service before scraping
# These configurations have been tested and verified as accessible
NEWS_WEBSITES = [
    {
        "name": "AP News",
        "url": "https://apnews.com/hub/crime",
        "article_selector": "h3 a[href*='/article/']",
        "headline_selector": "h1",
        "content_selector": "div[data-key='article'] p"
    },
    {
        "name": "CBS News Crime",
        "url": "https://www.cbsnews.com/crime/",
        "article_selector": "h4 a[href*='/news/']",
        "headline_selector": "h1",
        "content_selector": "section.content__body p"
    },
    {
        "name": "NBC News Crime",
        "url": "https://www.nbcnews.com/news/crime-courts",
        "article_selector": "h2 a[href*='/news/']",
        "headline_selector": "h1",
        "content_selector": "div.ArticleBody p"
    },
    {
        "name": "Fox News Crime",
        "url": "https://www.foxnews.com/category/us/crime",
        "article_selector": "h2 a[href*='/us/']",
        "headline_selector": "h1",
        "content_selector": "div.article-body p"
    },
    {
        "name": "CNN Crime",
        "url": "https://www.cnn.com/specials/us/crime-and-justice",
        "article_selector": "h3 a[href*='/2024/']",
        "headline_selector": "h1",
        "content_selector": "div.zn-body__paragraph"
    },
    {
        "name": "New York Post Crime",
        "url": "https://nypost.com/metro/",
        "article_selector": "h3 a[href*='/2024/']",
        "headline_selector": "h1",
        "content_selector": "div.entry-content p"
    },
    {
        "name": "Chicago Tribune Crime",
        "url": "https://www.chicagotribune.com/news/breaking/",
        "article_selector": "h3 a[href*='/news/']",
        "headline_selector": "h1",
        "content_selector": "div.body-copy p"
    },
    {
        "name": "Los Angeles Times Crime",
        "url": "https://www.latimes.com/california/",
        "article_selector": "h3 a[href*='/california/']",
        "headline_selector": "h1",
        "content_selector": "div.rich-text p"
    },
    {
        "name": "Washington Post Crime",
        "url": "https://www.washingtonpost.com/dc-md-va/",
        "article_selector": "h3 a[href*='/dc-md-va/']",
        "headline_selector": "h1",
        "content_selector": "div.article-body p"
    },
    {
        "name": "Miami Herald Crime",
        "url": "https://www.miamiherald.com/news/local/crime/",
        "article_selector": "h3 a[href*='/news/local/crime/']",
        "headline_selector": "h1",
        "content_selector": "div.story-body p"
    },

    {
        "name": "Boston Globe Crime",
        "url": "https://www.bostonglobe.com/metro/",
        "article_selector": "h3 a[href*='/metro/']",
        "headline_selector": "h1",
        "content_selector": "div.article-body p"
    },
    {
        "name": "San Francisco Chronicle Crime",
        "url": "https://www.sfchronicle.com/crime/",
        "article_selector": "h3 a[href*='/crime/']",
        "headline_selector": "h1",
        "content_selector": "div.body p"
    },
    {
        "name": "Atlanta Journal Constitution Crime",
        "url": "https://www.ajc.com/news/crime/",
        "article_selector": "h3 a[href*='/news/crime/']",
        "headline_selector": "h1",
        "content_selector": "div.article-body p"
    }
    # Additional sites can be added here - test with --mode test first
    # Sites that were tested but blocked access:
    # - Reuters (401 Forbidden)
    # - ABC News (404 Not Found) 
    # - USA Today (403 Forbidden)
    # - Philadelphia Inquirer (404 Not Found)
    # - Detroit Free Press (403 Forbidden)
    # - Dallas Morning News (403 Forbidden)
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
    "robbery": ["robbery", "robbed", "rob", "heist", "holdup", "armed robbery", "bank robbery"],
    "theft": ["theft", "stealing", "stolen", "stole", "larceny", "shoplifting", "pickpocket"],
    "burglary": ["burglary", "burglar", "breaking and entering", "break-in", "home invasion"],
    "assault": ["assault", "assaulted", "attack", "attacked", "beating", "beaten", "battery"],
    "murder": ["murder", "killed", "homicide", "death", "died", "fatal", "slain", "slaying"],
    "shooting": ["shooting", "shot", "gunfire", "firearm", "gun", "gunshot", "shot dead"],
    "stabbing": ["stabbing", "stabbed", "knife", "blade", "cut", "slashed"],
    "vandalism": ["vandalism", "vandalized", "graffiti", "damaged", "destroyed", "defaced"],
    "fraud": ["fraud", "scam", "embezzlement", "forgery", "identity theft", "wire fraud", "mail fraud"],
    "drug": ["drug", "narcotics", "cocaine", "heroin", "marijuana", "meth", "fentanyl", "trafficking"],
    "domestic_violence": ["domestic violence", "domestic abuse", "family violence", "spousal abuse"],
    "sexual_assault": ["sexual assault", "rape", "sexual abuse", "molestation", "sexual harassment"],
    "arson": ["arson", "fire", "burned", "burning", "set fire", "incendiary"],
    "kidnapping": ["kidnapping", "kidnapped", "abduction", "abducted", "taken", "missing person"],
    "carjacking": ["carjacking", "carjacked", "vehicle theft", "auto theft", "stolen car"],
    "cybercrime": ["cybercrime", "hacking", "data breach", "online fraud", "phishing", "cyber attack"],
    "gang_violence": ["gang", "gang violence", "gang shooting", "gang member", "organized crime"],
    "drunk_driving": ["drunk driving", "DUI", "DWI", "driving under influence", "impaired driving"],
    "weapon_charges": ["weapon", "illegal weapon", "gun charges", "firearm charges", "weapon possession"],
    "drug_trafficking": ["drug trafficking", "drug dealing", "drug distribution", "narcotics trafficking"]
}
