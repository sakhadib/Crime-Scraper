"""
Configuration file for the Crime Data Scraper
Contains settings for websites, keywords, file paths, and other constants
"""

import os
from typing import List, Dict

# Import verified sources
from verified_sources_config import VERIFIED_NEWS_WEBSITES

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

# Use verified sources from comprehensive testing
NEWS_WEBSITES = VERIFIED_NEWS_WEBSITES

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
    "full_text",
    "content_hash",
    "similarity_hash",
    "duplicate_note"
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
