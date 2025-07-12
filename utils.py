"""
Utility functions for the Crime Data Scraper
Contains helper functions for logging, file operations, and data processing
"""

import logging
import os
import time
import re
import hashlib
import json
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

def generate_content_hash(title: str, content: str, source: Optional[str] = None) -> str:
    """
    Generate a hash for article content to detect duplicates
    
    Args:
        title (str): Article title
        content (str): Article content
        source (str, optional): Source website name
    
    Returns:
        str: SHA-256 hash of the normalized content
    """
    # Normalize content for comparison
    normalized_title = clean_text(title).lower().strip()
    normalized_content = clean_text(content).lower().strip()
    
    # Create content string for hashing
    if source:
        # Include source for exact duplicate detection (same source + same content)
        content_string = f"{source}||{normalized_title}||{normalized_content}"
    else:
        # Content-only hash for cross-source duplicate detection
        content_string = f"{normalized_title}||{normalized_content}"
    
    # Generate SHA-256 hash
    return hashlib.sha256(content_string.encode('utf-8')).hexdigest()

def generate_similarity_hash(title: str, content: str) -> str:
    """
    Generate a similarity hash for detecting similar articles across sources
    Uses key content indicators for loose matching
    
    Args:
        title (str): Article title
        content (str): Article content
    
    Returns:
        str: Hash for similarity detection
    """
    # Extract key phrases and normalize
    title_words = set(clean_text(title).lower().split())
    content_words = set(clean_text(content).lower().split())
    
    # Focus on crime-related keywords and entities
    crime_keywords = {
        'murder', 'robbery', 'assault', 'theft', 'burglary', 'shooting', 
        'stabbing', 'arrest', 'police', 'victim', 'suspect', 'charged',
        'court', 'jail', 'prison', 'crime', 'criminal', 'felony'
    }
    
    # Extract crime-related words from title and content
    crime_words_title = title_words.intersection(crime_keywords)
    crime_words_content = content_words.intersection(crime_keywords)
    
    # Create similarity signature
    signature_parts = sorted(list(crime_words_title.union(crime_words_content)))
    signature = '||'.join(signature_parts[:10])  # Use top 10 crime-related words
    
    return hashlib.md5(signature.encode('utf-8')).hexdigest()

def check_duplicate_article(article_data: Dict, existing_hashes: set, 
                          similarity_hashes: set, source: str) -> Dict:
    """
    Check if an article is a duplicate and determine the type of duplicate
    
    Args:
        article_data (Dict): Article data with title, content, etc.
        existing_hashes (set): Set of existing exact content hashes
        similarity_hashes (set): Set of existing similarity hashes
        source (str): Source website name
    
    Returns:
        Dict: Duplicate detection results
    """
    title = article_data.get('headline', '')
    content = article_data.get('full_text', article_data.get('content', ''))
    
    if not title or not content:
        return {'is_duplicate': False, 'duplicate_type': None}
    
    # Generate hashes
    exact_hash = generate_content_hash(title, content, source)
    content_only_hash = generate_content_hash(title, content)
    similarity_hash = generate_similarity_hash(title, content)
    
    # Check for exact duplicate (same source + same content)
    if exact_hash in existing_hashes:
        return {
            'is_duplicate': True,
            'duplicate_type': 'exact_same_source',
            'hash': exact_hash,
            'reason': f'Exact duplicate from same source: {source}'
        }
    
    # Check for content similarity across sources
    if similarity_hash in similarity_hashes:
        return {
            'is_duplicate': True,
            'duplicate_type': 'similar_cross_source',
            'hash': similarity_hash,
            'reason': f'Similar content detected across sources (keeping both)',
            'allow_duplicate': True  # Allow similar content from different sources
        }
    
    return {
        'is_duplicate': False,
        'duplicate_type': None,
        'exact_hash': exact_hash,
        'content_hash': content_only_hash,
        'similarity_hash': similarity_hash
    }

def load_existing_hashes(csv_file_path: str) -> tuple:
    """
    Load existing article hashes from CSV file to detect duplicates
    
    Args:
        csv_file_path (str): Path to the CSV file
    
    Returns:
        tuple: (exact_hashes, similarity_hashes) sets
    """
    exact_hashes = set()
    similarity_hashes = set()
    
    try:
        import pandas as pd
        if os.path.exists(csv_file_path):
            df = pd.read_csv(csv_file_path)
            
            # Extract hashes if they exist in the CSV
            if 'content_hash' in df.columns:
                exact_hashes = set(df['content_hash'].dropna().values)
            
            if 'similarity_hash' in df.columns:
                similarity_hashes = set(df['similarity_hash'].dropna().values)
            
            # If no hash columns exist, generate them from existing data
            if not exact_hashes and 'headline' in df.columns and 'full_text' in df.columns:
                for _, row in df.iterrows():
                    if pd.notna(row['headline']) and pd.notna(row['full_text']):
                        source = row.get('source', '') if 'source' in row else ''
                        exact_hash = generate_content_hash(row['headline'], row['full_text'], source)
                        similarity_hash = generate_similarity_hash(row['headline'], row['full_text'])
                        exact_hashes.add(exact_hash)
                        similarity_hashes.add(similarity_hash)
                        
    except Exception as e:
        print(f"Warning: Could not load existing hashes: {e}")
    
    return exact_hashes, similarity_hashes

def append_to_csv_with_dedup(article_data: Dict, csv_file_path: Optional[str] = None) -> Dict:
    """
    Append article to CSV with duplicate detection
    
    Args:
        article_data (Dict): Article data to append
        csv_file_path (str, optional): Path to CSV file
    
    Returns:
        Dict: Result with success status and duplicate information
    """
    from config import CSV_FILE_PATH
    
    if csv_file_path is None:
        csv_file_path = CSV_FILE_PATH
    
    # Load existing hashes
    existing_hashes, similarity_hashes = load_existing_hashes(csv_file_path)
    
    # Check for duplicates
    source = article_data.get('source', '')
    duplicate_result = check_duplicate_article(
        article_data, existing_hashes, similarity_hashes, source
    )
    
    # If it's an exact duplicate from the same source, skip it
    if duplicate_result['is_duplicate'] and duplicate_result['duplicate_type'] == 'exact_same_source':
        return {
            'success': False,
            'skipped': True,
            'reason': duplicate_result['reason'],
            'duplicate_type': duplicate_result['duplicate_type']
        }
    
    # Add hash information to article data
    if not duplicate_result['is_duplicate']:
        article_data['content_hash'] = duplicate_result.get('exact_hash', '')
        article_data['similarity_hash'] = duplicate_result.get('similarity_hash', '')
    else:
        # Similar content from different source - add hash and note
        article_data['content_hash'] = duplicate_result.get('hash', duplicate_result.get('exact_hash', ''))
        article_data['similarity_hash'] = duplicate_result.get('hash', duplicate_result.get('similarity_hash', ''))
        article_data['duplicate_note'] = duplicate_result.get('reason', '')
    
    # Append to CSV
    success = append_to_csv(article_data)
    
    return {
        'success': success,
        'skipped': False,
        'duplicate_info': duplicate_result if duplicate_result['is_duplicate'] else None
    }
