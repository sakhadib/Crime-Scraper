"""
NLP processor module for extracting structured information from crime articles
Uses spaCy for named entity recognition and custom patterns for crime classification
"""

import spacy
from spacy.matcher import Matcher
from spacy.language import Language
from typing import Dict, List, Optional, Tuple, Union
import re
from datetime import datetime
from utils import (
    setup_logging, clean_text, extract_date_from_text, 
    extract_numbers_from_text, extract_money_from_text
)
from config import SPACY_MODEL, ENTITY_TYPES, CRIME_TYPE_PATTERNS

class CrimeNLPProcessor:
    """
    NLP processor for extracting structured information from crime articles
    """
    
    def __init__(self):
        self.logger = setup_logging()
        self.nlp: Optional[Language] = None
        self.matcher: Optional[Matcher] = None
        self._load_model()
        self._setup_matcher()
    
    def _load_model(self):
        """
        Load the spaCy model
        """
        try:
            self.nlp = spacy.load(SPACY_MODEL)
            self.logger.info(f"Successfully loaded spaCy model: {SPACY_MODEL}")
        except Exception as e:
            self.logger.error(f"Failed to load spaCy model: {str(e)}")
            raise
    
    def _setup_matcher(self):
        """
        Set up pattern matcher for crime types and specific entities
        """
        if self.nlp is None:
            raise RuntimeError("spaCy model must be loaded before setting up matcher")
            
        self.matcher = Matcher(self.nlp.vocab)
        
        # Add patterns for different crime types
        for crime_type, patterns in CRIME_TYPE_PATTERNS.items():
            pattern_list = []
            for pattern in patterns:
                # Create token patterns for each crime keyword
                tokens = pattern.split()
                token_pattern = [{"LOWER": token} for token in tokens]
                pattern_list.append(token_pattern)
            
            if pattern_list:
                self.matcher.add(f"CRIME_{crime_type.upper()}", pattern_list)
        
        # Add patterns for specific crime-related phrases
        injury_patterns = [
            [{"LOWER": "injured"}, {"IS_DIGIT": True}],
            [{"IS_DIGIT": True}, {"LOWER": "injured"}],
            [{"IS_DIGIT": True}, {"LOWER": "victims"}],
            [{"IS_DIGIT": True}, {"LOWER": "people"}, {"LOWER": "hurt"}]
        ]
        self.matcher.add("INJURIES", injury_patterns)
        
        fatality_patterns = [
            [{"LOWER": "killed"}, {"IS_DIGIT": True}],
            [{"IS_DIGIT": True}, {"LOWER": "killed"}],
            [{"IS_DIGIT": True}, {"LOWER": "dead"}],
            [{"IS_DIGIT": True}, {"LOWER": "deaths"}],
            [{"IS_DIGIT": True}, {"LOWER": "fatalities"}]
        ]
        self.matcher.add("FATALITIES", fatality_patterns)
        
        arrest_patterns = [
            [{"LOWER": "arrested"}, {"IS_DIGIT": True}],
            [{"IS_DIGIT": True}, {"LOWER": "arrested"}],
            [{"IS_DIGIT": True}, {"LOWER": "suspects"}],
            [{"LOWER": "suspect"}, {"LOWER": "in"}, {"LOWER": "custody"}]
        ]
        self.matcher.add("ARRESTS", arrest_patterns)
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract named entities from text using spaCy NER
        
        Args:
            text (str): Text to process
            
        Returns:
            Dict[str, List[str]]: Dictionary of entity types and their values
        """
        if self.nlp is None:
            raise RuntimeError("spaCy model not loaded")
            
        doc = self.nlp(text)
        entities = {}
        
        for ent in doc.ents:
            entity_type = ENTITY_TYPES.get(ent.label_, ent.label_)
            if entity_type not in entities:
                entities[entity_type] = []
            
            entity_text = clean_text(ent.text)
            if entity_text and entity_text not in entities[entity_type]:
                entities[entity_type].append(entity_text)
        
        return entities
    
    def classify_crime_type(self, text: str) -> List[str]:
        """
        Classify the type of crime mentioned in the text
        
        Args:
            text (str): Text to analyze
            
        Returns:
            List[str]: List of detected crime types
        """
        if self.nlp is None or self.matcher is None:
            raise RuntimeError("spaCy model and matcher not loaded")
            
        doc = self.nlp(text)
        matches = self.matcher(doc)
        
        crime_types = []
        for match_id, start, end in matches:
            label = self.nlp.vocab.strings[match_id]
            if label.startswith("CRIME_"):
                crime_type = label.replace("CRIME_", "").lower()
                if crime_type not in crime_types:
                    crime_types.append(crime_type)
        
        return crime_types
    
    def extract_injury_info(self, text: str) -> Dict[str, Optional[int]]:
        """
        Extract information about injuries, fatalities, and arrests
        
        Args:
            text (str): Text to analyze
            
        Returns:
            Dict[str, Optional[int]]: Dictionary with injury, fatality, and arrest counts
        """
        if self.nlp is None or self.matcher is None:
            raise RuntimeError("spaCy model and matcher not loaded")
            
        doc = self.nlp(text)
        matches = self.matcher(doc)
        
        info: Dict[str, Optional[int]] = {
            "injuries": None,
            "fatalities": None,
            "arrests": None
        }
        
        # Use matcher patterns
        for match_id, start, end in matches:
            label = self.nlp.vocab.strings[match_id]
            span = doc[start:end]
            
            # Extract numbers from the matched span
            numbers = extract_numbers_from_text(span.text)
            if numbers:
                if label == "INJURIES":
                    info["injuries"] = max(numbers)
                elif label == "FATALITIES":
                    info["fatalities"] = max(numbers)
                elif label == "ARRESTS":
                    info["arrests"] = max(numbers)
        
        # Additional regex-based extraction as backup
        text_lower = text.lower()
        
        # Injuries
        injury_patterns = [
            r'(\d+)\s+(?:people\s+)?(?:were\s+)?injured',
            r'injured\s+(\d+)',
            r'(\d+)\s+victims?',
            r'(\d+)\s+people\s+hurt'
        ]
        
        for pattern in injury_patterns:
            match = re.search(pattern, text_lower)
            if match and info["injuries"] is None:
                info["injuries"] = int(match.group(1))
                break
        
        # Fatalities
        fatality_patterns = [
            r'(\d+)\s+(?:people\s+)?(?:were\s+)?killed',
            r'killed\s+(\d+)',
            r'(\d+)\s+(?:people\s+)?died',
            r'(\d+)\s+deaths?',
            r'(\d+)\s+fatalities'
        ]
        
        for pattern in fatality_patterns:
            match = re.search(pattern, text_lower)
            if match and info["fatalities"] is None:
                info["fatalities"] = int(match.group(1))
                break
        
        # Arrests
        arrest_patterns = [
            r'(\d+)\s+(?:people\s+)?(?:were\s+)?arrested',
            r'arrested\s+(\d+)',
            r'(\d+)\s+suspects?',
            r'(\d+)\s+in\s+custody'
        ]
        
        for pattern in arrest_patterns:
            match = re.search(pattern, text_lower)
            if match and info["arrests"] is None:
                info["arrests"] = int(match.group(1))
                break
        
        return info
    
    def extract_method_and_motivation(self, text: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Extract method (how) and motivation (why) from the text
        
        Args:
            text (str): Text to analyze
            
        Returns:
            Tuple[Optional[str], Optional[str]]: Method and motivation
        """
        if self.nlp is None:
            raise RuntimeError("spaCy model not loaded")
            
        doc = self.nlp(text)
        
        # Method extraction patterns
        method_keywords = [
            "weapon", "gun", "knife", "shooting", "stabbing", "beating",
            "strangling", "poisoning", "bombing", "arson", "breaking",
            "entering", "forced entry", "climbing", "jumping"
        ]
        
        method = None
        for token in doc:
            if token.text.lower() in method_keywords:
                # Get surrounding context
                start = max(0, token.i - 3)
                end = min(len(doc), token.i + 4)
                method = clean_text(doc[start:end].text)
                break
        
        # Motivation extraction patterns
        motivation_patterns = [
            r'(?:because|due to|motivated by|reason|motive)[\s\w]*?(?:money|drugs?|revenge|jealousy|anger|dispute|robbery|theft)',
            r'(?:over|about|regarding)[\s\w]*?(?:money|drugs?|relationship|property|debt)',
            r'(?:domestic|family|personal)[\s\w]*?(?:dispute|violence|conflict)'
        ]
        
        motivation = None
        text_lower = text.lower()
        for pattern in motivation_patterns:
            match = re.search(pattern, text_lower)
            if match:
                motivation = clean_text(match.group(0))
                break
        
        return method, motivation
    
    def process_article(self, article_data: Dict) -> Dict:
        """
        Process a complete article and extract all relevant information
        
        Args:
            article_data (Dict): Article data with headline, content, etc.
            
        Returns:
            Dict: Processed article data with extracted information
        """
        try:
            headline = article_data.get('headline', '')
            content = article_data.get('content', '')
            full_text = f"{headline} {content}"
            
            # Extract entities
            entities = self.extract_entities(full_text)
            
            # Classify crime type
            crime_types = self.classify_crime_type(full_text)
            
            # Extract injury information
            injury_info = self.extract_injury_info(full_text)
            
            # Extract method and motivation
            method, motivation = self.extract_method_and_motivation(full_text)
            
            # Extract economic loss
            economic_loss = extract_money_from_text(full_text)
            
            # Extract publication date from content
            publication_date = extract_date_from_text(full_text)
            
            # Compile processed data
            processed_data = {
                'date_scraped': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'article_url': article_data.get('url', ''),
                'headline': clean_text(headline),
                'publication_date': publication_date or '',
                'who': '; '.join(entities.get('who', [])),
                'what': '; '.join(crime_types) if crime_types else '',
                'where': '; '.join(entities.get('where', [])),
                'when': '; '.join(entities.get('when', [])),
                'how': method or '',
                'why': motivation or '',
                'economic_loss': economic_loss or '',
                'injuries': injury_info.get('injuries', ''),
                'fatalities': injury_info.get('fatalities', ''),
                'arrests': injury_info.get('arrests', ''),
                'full_text': clean_text(full_text)
            }
            
            self.logger.info(f"Successfully processed article: {headline}")
            return processed_data
            
        except Exception as e:
            self.logger.error(f"Error processing article: {str(e)}")
            return {}
    
    def process_multiple_articles(self, articles: List[Dict]) -> List[Dict]:
        """
        Process multiple articles
        
        Args:
            articles (List[Dict]): List of article data
            
        Returns:
            List[Dict]: List of processed article data
        """
        processed_articles = []
        
        for article in articles:
            processed = self.process_article(article)
            if processed:
                processed_articles.append(processed)
        
        self.logger.info(f"Processed {len(processed_articles)} out of {len(articles)} articles")
        return processed_articles

# Test function
def test_nlp_processor():
    """
    Test the NLP processor with sample text
    """
    processor = CrimeNLPProcessor()
    
    sample_text = """
    Police arrested two suspects after a robbery at Main Street Bank yesterday. 
    John Smith, 25, was injured during the incident when the suspects used a gun 
    to threaten customers. The robbers stole $5,000 before fleeing the scene. 
    The incident happened at 3 PM on January 15th, 2024 in downtown Chicago.
    """
    
    sample_article = {
        'headline': 'Bank Robbery Leaves One Injured',
        'content': sample_text,
        'url': 'http://example.com/article1'
    }
    
    result = processor.process_article(sample_article)
    
    print("Processed Article Data:")
    for key, value in result.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    test_nlp_processor()
