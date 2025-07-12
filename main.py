"""
Main application file for the Crime Data Scraper
Orchestrates web scraping, NLP processing, and data storage
"""

import argparse
import sys
from datetime import datetime
from typing import List, Dict
from scraper import WebScraper
from nlp_processor import CrimeNLPProcessor
from utils import setup_logging, append_to_csv, ensure_csv_exists, get_current_timestamp, append_to_csv_with_dedup
from config import NEWS_WEBSITES

class CrimeDataScraper:
    """
    Main class that orchestrates the entire crime data scraping process
    """
    
    def __init__(self):
        self.logger = setup_logging()
        self.scraper = WebScraper()
        self.nlp_processor = CrimeNLPProcessor()
        self.logger.info("Crime Data Scraper initialized")
    
    def run_full_scrape(self) -> int:
        """
        Run the complete scraping process for all configured websites
        
        Returns:
            int: Number of articles successfully processed and saved
        """
        self.logger.info("Starting full scrape process")
        
        try:
            # Ensure CSV file exists
            ensure_csv_exists()
            
            # Scrape articles from all websites
            self.logger.info("Scraping articles from all configured websites")
            raw_articles = self.scraper.scrape_all_websites()
            
            if not raw_articles:
                self.logger.warning("No articles found")
                return 0
            
            # Process articles with NLP
            self.logger.info(f"Processing {len(raw_articles)} articles with NLP")
            processed_articles = self.nlp_processor.process_multiple_articles(raw_articles)
            
            # Save to CSV with duplicate detection
            saved_count = 0
            skipped_count = 0
            duplicate_info = []
            
            for article in processed_articles:
                result = append_to_csv_with_dedup(article)
                
                if result['success']:
                    saved_count += 1
                    if result.get('duplicate_info'):
                        duplicate_info.append({
                            'title': article.get('headline', 'Unknown'),
                            'type': result['duplicate_info']['duplicate_type'],
                            'reason': result['duplicate_info']['reason']
                        })
                elif result.get('skipped'):
                    skipped_count += 1
                    self.logger.info(f"Skipped duplicate: {article.get('headline', 'Unknown')} - {result['reason']}")
                else:
                    self.logger.error(f"Failed to save article: {article.get('headline', 'Unknown')}")
            
            # Log summary
            self.logger.info(f"Successfully processed and saved {saved_count} articles")
            if skipped_count > 0:
                self.logger.info(f"Skipped {skipped_count} duplicate articles")
            if duplicate_info:
                self.logger.info(f"Found {len(duplicate_info)} similar articles from different sources (kept both)")
            
            return saved_count
            
        except Exception as e:
            self.logger.error(f"Error in full scrape process: {str(e)}")
            return 0
    
    def run_single_website_scrape(self, website_name: str) -> int:
        """
        Run scraping for a single website
        
        Args:
            website_name (str): Name of the website to scrape
            
        Returns:
            int: Number of articles successfully processed and saved
        """
        self.logger.info(f"Starting scrape for website: {website_name}")
        
        try:
            # Ensure CSV file exists
            ensure_csv_exists()
            
            # Find the website configuration
            website_config = None
            for config in NEWS_WEBSITES:
                if config['name'].lower() == website_name.lower():
                    website_config = config
                    break
            
            if not website_config:
                self.logger.error(f"Website '{website_name}' not found in configuration")
                return 0
            
            # Scrape articles from the specified website
            raw_articles = self.scraper.extract_article_links(website_config)
            
            # Get full content for each article
            full_articles = []
            for article in raw_articles:
                content = self.scraper.extract_article_content(article['url'], website_config)
                if content:
                    article['content'] = content
                    full_articles.append(article)
            
            if not full_articles:
                self.logger.warning(f"No articles found for {website_name}")
                return 0
            
            # Process articles with NLP
            processed_articles = self.nlp_processor.process_multiple_articles(full_articles)
            
            # Save to CSV with duplicate detection
            saved_count = 0
            skipped_count = 0
            
            for article in processed_articles:
                result = append_to_csv_with_dedup(article)
                
                if result['success']:
                    saved_count += 1
                elif result.get('skipped'):
                    skipped_count += 1
                    self.logger.info(f"Skipped duplicate from {website_name}: {article.get('headline', 'Unknown')}")
            
            if skipped_count > 0:
                self.logger.info(f"Successfully processed and saved {saved_count} articles from {website_name} (skipped {skipped_count} duplicates)")
            else:
                self.logger.info(f"Successfully processed and saved {saved_count} articles from {website_name}")
            
            return saved_count
            
        except Exception as e:
            self.logger.error(f"Error scraping {website_name}: {str(e)}")
            return 0
    
    def test_configuration(self) -> bool:
        """
        Test the scraper configuration and connectivity
        
        Returns:
            bool: True if configuration is valid, False otherwise
        """
        self.logger.info("Testing scraper configuration")
        
        try:
            # Test spaCy model
            test_text = "This is a test sentence."
            self.nlp_processor.extract_entities(test_text)
            self.logger.info("✓ spaCy model loaded successfully")
            
            # Test CSV functionality
            ensure_csv_exists()
            self.logger.info("✓ CSV file functionality working")
            
            # Test website connectivity
            working_sites = 0
            for website_config in NEWS_WEBSITES:
                try:
                    soup = self.scraper.get_page_content(website_config['url'])
                    if soup:
                        working_sites += 1
                        self.logger.info(f"✓ Successfully connected to {website_config['name']}")
                    else:
                        self.logger.warning(f"✗ Failed to connect to {website_config['name']}")
                except Exception as e:
                    self.logger.warning(f"✗ Error connecting to {website_config['name']}: {str(e)}")
            
            self.logger.info(f"Configuration test complete. {working_sites}/{len(NEWS_WEBSITES)} websites accessible")
            return working_sites > 0
            
        except Exception as e:
            self.logger.error(f"Configuration test failed: {str(e)}")
            return False
    
    def get_statistics(self) -> Dict:
        """
        Get statistics about the scraped data
        
        Returns:
            Dict: Statistics about the scraped articles
        """
        try:
            import pandas as pd
            from config import CSV_FILE_PATH
            
            df = pd.read_csv(CSV_FILE_PATH)
            
            stats = {
                'total_articles': len(df),
                'date_range': {
                    'earliest': df['date_scraped'].min(),
                    'latest': df['date_scraped'].max()
                },
                'crime_types': df['what'].value_counts().to_dict() if 'what' in df.columns else {},
                'locations': df['where'].value_counts().head(10).to_dict() if 'where' in df.columns else {},
                'articles_with_injuries': len(df[df['injuries'] != '']) if 'injuries' in df.columns else 0,
                'articles_with_fatalities': len(df[df['fatalities'] != '']) if 'fatalities' in df.columns else 0,
                'articles_with_arrests': len(df[df['arrests'] != '']) if 'arrests' in df.columns else 0,
                'duplicate_stats': {
                    'total_with_hashes': len(df[df['content_hash'].notna()]) if 'content_hash' in df.columns else 0,
                    'articles_marked_similar': len(df[df['duplicate_note'].notna()]) if 'duplicate_note' in df.columns else 0,
                    'unique_content_hashes': len(df['content_hash'].dropna().unique()) if 'content_hash' in df.columns else 0,
                    'unique_similarity_hashes': len(df['similarity_hash'].dropna().unique()) if 'similarity_hash' in df.columns else 0
                }
            }
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error getting statistics: {str(e)}")
            return {}

def main():
    """
    Main function to run the crime data scraper with command line interface
    """
    parser = argparse.ArgumentParser(description='Crime Data Scraper')
    parser.add_argument('--mode', choices=['full', 'single', 'test', 'stats', 'dedup-test'], 
                       default='full', help='Scraping mode')
    parser.add_argument('--website', type=str, help='Website name for single mode')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Initialize the scraper
    scraper = CrimeDataScraper()
    
    if args.mode == 'test':
        print("Testing configuration...")
        success = scraper.test_configuration()
        if success:
            print("✓ Configuration test passed")
            sys.exit(0)
        else:
            print("✗ Configuration test failed")
            sys.exit(1)
    
    elif args.mode == 'dedup-test':
        print("Testing duplicate detection system...")
        try:
            from test_duplicate_detection import test_duplicate_detection
            success = test_duplicate_detection()
            if success:
                print("✓ Duplicate detection test completed successfully")
            else:
                print("✗ Duplicate detection test failed")
        except ImportError:
            print("Error: test_duplicate_detection.py not found")
        except Exception as e:
            print(f"Error running duplicate detection test: {e}")
    
    elif args.mode == 'stats':
        print("Generating statistics...")
        stats = scraper.get_statistics()
        if stats:
            print("\n=== Crime Data Statistics ===")
            print(f"Total Articles: {stats.get('total_articles', 0)}")
            print(f"Date Range: {stats.get('date_range', {}).get('earliest', 'N/A')} to {stats.get('date_range', {}).get('latest', 'N/A')}")
            print(f"Articles with Injuries: {stats.get('articles_with_injuries', 0)}")
            print(f"Articles with Fatalities: {stats.get('articles_with_fatalities', 0)}")
            print(f"Articles with Arrests: {stats.get('articles_with_arrests', 0)}")
            
            # Duplicate detection stats
            dup_stats = stats.get('duplicate_stats', {})
            if dup_stats:
                print(f"\n=== Duplicate Detection Stats ===")
                print(f"Articles with Hash Data: {dup_stats.get('total_with_hashes', 0)}")
                print(f"Similar Articles (Different Sources): {dup_stats.get('articles_marked_similar', 0)}")
                print(f"Unique Content Signatures: {dup_stats.get('unique_content_hashes', 0)}")
                print(f"Unique Similarity Signatures: {dup_stats.get('unique_similarity_hashes', 0)}")
            
            print("\nTop Crime Types:")
            for crime_type, count in list(stats.get('crime_types', {}).items())[:5]:
                if crime_type:
                    print(f"  {crime_type}: {count}")
            
            print("\nTop Locations:")
            for location, count in list(stats.get('locations', {}).items())[:5]:
                if location:
                    print(f"  {location}: {count}")
        else:
            print("No statistics available")
    
    elif args.mode == 'single':
        if not args.website:
            print("Error: --website argument required for single mode")
            sys.exit(1)
        
        print(f"Scraping website: {args.website}")
        count = scraper.run_single_website_scrape(args.website)
        print(f"Processed {count} articles")
    
    else:  # full mode
        print("Starting full scrape...")
        start_time = datetime.now()
        count = scraper.run_full_scrape()
        end_time = datetime.now()
        duration = end_time - start_time
        
        print(f"Scraping completed in {duration}")
        print(f"Processed {count} articles")

if __name__ == "__main__":
    main()
