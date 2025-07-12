"""
Web scraper module for crime data extraction
Handles scraping news websites for crime-related articles
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import time
from urllib.parse import urljoin, urlparse
from utils import (
    setup_logging, get_random_user_agent, clean_text, 
    rate_limit_delay, is_crime_related, url_is_duplicate
)
from config import (
    NEWS_WEBSITES, CRIME_KEYWORDS, REQUEST_TIMEOUT, 
    MAX_RETRIES, DELAY_BETWEEN_REQUESTS
)

class WebScraper:
    """
    Web scraper class for extracting crime-related news articles
    """
    
    def __init__(self):
        self.logger = setup_logging()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': get_random_user_agent()
        })
    
    def get_page_content(self, url: str) -> Optional[BeautifulSoup]:
        """
        Get page content with error handling and retries
        
        Args:
            url (str): URL to scrape
            
        Returns:
            Optional[BeautifulSoup]: Parsed HTML content or None if failed
        """
        for attempt in range(MAX_RETRIES):
            try:
                self.logger.info(f"Fetching URL: {url} (Attempt {attempt + 1})")
                
                response = self.session.get(
                    url, 
                    timeout=REQUEST_TIMEOUT,
                    headers={'User-Agent': get_random_user_agent()}
                )
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                return soup
                
            except requests.exceptions.RequestException as e:
                self.logger.warning(f"Request failed (attempt {attempt + 1}): {str(e)}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    self.logger.error(f"Failed to fetch {url} after {MAX_RETRIES} attempts")
        
        return None
    
    def extract_article_links(self, website_config: Dict) -> List[Dict]:
        """
        Extract article links from a news website's main page
        
        Args:
            website_config (Dict): Website configuration
            
        Returns:
            List[Dict]: List of article information dictionaries
        """
        soup = self.get_page_content(website_config['url'])
        if not soup:
            return []
        
        articles = []
        
        try:
            # Find article links using the CSS selector
            article_elements = soup.select(website_config['article_selector'])
            
            for element in article_elements:
                try:
                    # Extract headline and URL
                    headline = clean_text(element.get_text())
                    article_url = element.get('href')
                    
                    if not article_url or not isinstance(article_url, str):
                        continue
                    
                    # Convert relative URLs to absolute
                    article_url = urljoin(website_config['url'], article_url)
                    
                    # Check if it's crime-related and not a duplicate
                    if (is_crime_related(headline, CRIME_KEYWORDS) and 
                        not url_is_duplicate(article_url)):
                        
                        articles.append({
                            'headline': headline,
                            'url': article_url,
                            'source': website_config['name']
                        })
                        
                        self.logger.info(f"Found crime-related article: {headline}")
                    
                except Exception as e:
                    self.logger.warning(f"Error processing article element: {str(e)}")
                    continue
        
        except Exception as e:
            self.logger.error(f"Error extracting articles from {website_config['name']}: {str(e)}")
        
        return articles
    
    def extract_article_content(self, article_url: str, website_config: Dict) -> Optional[str]:
        """
        Extract full content from an article URL
        
        Args:
            article_url (str): URL of the article
            website_config (Dict): Website configuration
            
        Returns:
            Optional[str]: Article content or None if failed
        """
        soup = self.get_page_content(article_url)
        if not soup:
            return None
        
        try:
            # Try to find content using the configured selector
            content_elements = soup.select(website_config.get('content_selector', 'p'))
            
            if content_elements:
                content = ' '.join([clean_text(elem.get_text()) for elem in content_elements])
            else:
                # Fallback: try common content selectors
                fallback_selectors = [
                    'div.article-content', 'div.content', 'article', 
                    'div.story-body', 'div.post-content', 'p'
                ]
                
                content = ""
                for selector in fallback_selectors:
                    elements = soup.select(selector)
                    if elements:
                        content = ' '.join([clean_text(elem.get_text()) for elem in elements])
                        break
            
            return content if content else None
            
        except Exception as e:
            self.logger.error(f"Error extracting content from {article_url}: {str(e)}")
            return None
    
    def scrape_all_websites(self) -> List[Dict]:
        """
        Scrape all configured websites for crime-related articles
        
        Returns:
            List[Dict]: List of all found articles with content
        """
        all_articles = []
        
        for website_config in NEWS_WEBSITES:
            self.logger.info(f"Scraping website: {website_config['name']}")
            
            try:
                # Get article links
                articles = self.extract_article_links(website_config)
                
                # Get full content for each article
                for article in articles:
                    rate_limit_delay(DELAY_BETWEEN_REQUESTS)
                    
                    content = self.extract_article_content(article['url'], website_config)
                    if content:
                        article['content'] = content
                        all_articles.append(article)
                        self.logger.info(f"Successfully scraped: {article['headline']}")
                    else:
                        self.logger.warning(f"Failed to get content for: {article['headline']}")
                
            except Exception as e:
                self.logger.error(f"Error scraping {website_config['name']}: {str(e)}")
                continue
        
        self.logger.info(f"Total articles scraped: {len(all_articles)}")
        return all_articles
    
    def scrape_single_website(self, website_name: str) -> List[Dict]:
        """
        Scrape a single website by name
        
        Args:
            website_name (str): Name of the website to scrape
            
        Returns:
            List[Dict]: List of articles from the specified website
        """
        website_config = None
        for config in NEWS_WEBSITES:
            if config['name'] == website_name:
                website_config = config
                break
        
        if not website_config:
            self.logger.error(f"Website '{website_name}' not found in configuration")
            return []
        
        return self.extract_article_links(website_config)

# Example usage and testing function
def test_scraper():
    """
    Test function for the scraper (useful for development)
    """
    # Add a real news website for testing
    test_website = {
        "name": "BBC News",
        "url": "https://www.bbc.com/news",
        "article_selector": "h3 a",
        "headline_selector": "h1",
        "content_selector": "div[data-component='text-block']"
    }
    
    scraper = WebScraper()
    
    # Test getting page content
    soup = scraper.get_page_content(test_website['url'])
    if soup:
        print("Successfully connected to test website")
    else:
        print("Failed to connect to test website")

if __name__ == "__main__":
    test_scraper()
