"""
Utility functions for the Crime Data Scraper
Contains helper functions for logging, file operations, and data processing
"""

import logging
import os
import time
import re
from datetime import datetime
from typing import List, Dict, Optional
from fake_useragent import UserAgent
import pandas as pd
from config import LOG_FILE_PATH, CSV_FILE_PATH, CSV_COLUMNS

def setup_logging() -> logging.Logger:
    """
    Set up logging configuration for the scraper
    
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logger
    logger = logging.getLogger('crime_scraper')
    logger.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # File handler
    file_handler = logging.FileHandler(LOG_FILE_PATH)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger

def get_random_user_agent() -> str:
    """
    Get a random user agent string to avoid detection
    
    Returns:
        str: Random user agent string
    """
    try:
        ua = UserAgent()
        return ua.random
    except Exception:
        # Fallback user agent if fake-useragent fails
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

def clean_text(text: str) -> str:
    """
    Clean and normalize text content
    
    Args:
        text (str): Raw text to clean
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters that might cause CSV issues
    text = re.sub(r'["\n\r\t]', ' ', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text

def extract_date_from_text(text: str) -> Optional[str]:
    """
    Extract date from text using regex patterns
    
    Args:
        text (str): Text to extract date from
        
    Returns:
        Optional[str]: Extracted date string or None
    """
    date_patterns = [
        r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b',  # MM/DD/YYYY or MM-DD-YYYY
        r'\b(\d{4}[/-]\d{1,2}[/-]\d{1,2})\b',    # YYYY/MM/DD or YYYY-MM-DD
        r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',  # Month DD, YYYY
        r'\b\d{1,2}\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b'   # DD Month YYYY
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0)
    
    return None

def extract_numbers_from_text(text: str) -> List[int]:
    """
    Extract numbers from text (useful for injuries, fatalities, economic loss)
    
    Args:
        text (str): Text to extract numbers from
        
    Returns:
        List[int]: List of extracted numbers
    """
    numbers = re.findall(r'\b\d+\b', text)
    return [int(num) for num in numbers]

def extract_money_from_text(text: str) -> Optional[str]:
    """
    Extract monetary amounts from text
    
    Args:
        text (str): Text to extract money from
        
    Returns:
        Optional[str]: Extracted monetary amount or None
    """
    money_patterns = [
        r'\$[\d,]+(?:\.\d{2})?',  # $1,000.00
        r'\b\d+\s*(?:dollars?|bucks?)\b',  # 100 dollars
        r'\b(?:USD|usd)\s*\d+\b'  # USD 100
    ]
    
    for pattern in money_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0)
    
    return None

def ensure_csv_exists():
    """
    Ensure the CSV file exists with proper headers
    """
    if not os.path.exists(CSV_FILE_PATH):
        df = pd.DataFrame(columns=CSV_COLUMNS)
        df.to_csv(CSV_FILE_PATH, index=False)

def append_to_csv(data: Dict) -> bool:
    """
    Append data to the CSV file
    
    Args:
        data (Dict): Data dictionary to append
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        ensure_csv_exists()
        
        # Create DataFrame from the data
        df = pd.DataFrame([data])
        
        # Append to CSV
        df.to_csv(CSV_FILE_PATH, mode='a', header=False, index=False)
        
        return True
    except Exception as e:
        logger = setup_logging()
        logger.error(f"Error appending to CSV: {str(e)}")
        return False

def url_is_duplicate(url: str) -> bool:
    """
    Check if URL already exists in the CSV file
    
    Args:
        url (str): URL to check
        
    Returns:
        bool: True if duplicate, False otherwise
    """
    try:
        if not os.path.exists(CSV_FILE_PATH):
            return False
        
        df = pd.read_csv(CSV_FILE_PATH)
        return url in df['article_url'].values
    except Exception:
        return False

def rate_limit_delay(delay_seconds: int = 1):
    """
    Add delay between requests to be respectful to servers
    
    Args:
        delay_seconds (int): Number of seconds to delay
    """
    time.sleep(delay_seconds)

def is_crime_related(text: str, keywords: List[str]) -> bool:
    """
    Check if text contains crime-related keywords
    
    Args:
        text (str): Text to check
        keywords (List[str]): List of crime keywords
        
    Returns:
        bool: True if crime-related, False otherwise
    """
    text_lower = text.lower()
    return any(keyword.lower() in text_lower for keyword in keywords)

def get_current_timestamp() -> str:
    """
    Get current timestamp as string
    
    Returns:
        str: Current timestamp in YYYY-MM-DD HH:MM:SS format
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
