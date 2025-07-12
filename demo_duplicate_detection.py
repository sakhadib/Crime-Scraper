"""
Demonstration script for duplicate detection in action
"""

import sys
import os
from datetime import datetime
from main import CrimeDataScraper

def demo_duplicate_detection():
    """Demonstrate duplicate detection with sample data"""
    
    print("Crime Data Scraper - Duplicate Detection Demo")
    print("=" * 50)
    
    # Initialize scraper
    scraper = CrimeDataScraper()
    
    # Create some test articles to demonstrate duplicate detection
    from utils import append_to_csv_with_dedup
    
    test_articles = [
        {
            'headline': 'Local Bank Robbery Leads to Arrest',
            'source': 'City News',
            'url': 'https://example.com/article1',
            'date_scraped': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'full_text': 'Police arrested a suspect yesterday after a robbery at First National Bank downtown. The 30-year-old male fled but was caught nearby.',
            'who': 'Police, Suspect (30-year-old male)',
            'what': 'Bank robbery, Arrest',
            'where': 'First National Bank downtown',
            'when': 'Yesterday',
            'how': 'Armed robbery, fled on foot',
            'why': '',
            'economic_loss': '',
            'injuries': '',
            'fatalities': '',
            'arrests': '1 suspect arrested'
        },
        {
            # Exact duplicate from same source (should be skipped)
            'headline': 'Local Bank Robbery Leads to Arrest',
            'source': 'City News',
            'url': 'https://example.com/article1',
            'date_scraped': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'full_text': 'Police arrested a suspect yesterday after a robbery at First National Bank downtown. The 30-year-old male fled but was caught nearby.',
            'who': 'Police, Suspect (30-year-old male)',
            'what': 'Bank robbery, Arrest',
            'where': 'First National Bank downtown',
            'when': 'Yesterday',
            'how': 'Armed robbery, fled on foot',
            'why': '',
            'economic_loss': '',
            'injuries': '',
            'fatalities': '',
            'arrests': '1 suspect arrested'
        },
        {
            # Similar story from different source (should be kept)
            'headline': 'Bank Robber Apprehended After Downtown Crime',
            'source': 'Metro Tribune',
            'url': 'https://tribune.com/article2',
            'date_scraped': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'full_text': 'A 30-year-old man was arrested following an armed robbery at First National Bank in the downtown area. The perpetrator attempted to escape but was captured.',
            'who': 'Police, Perpetrator (30-year-old man)',
            'what': 'Armed robbery, Arrest',
            'where': 'First National Bank, downtown area',
            'when': 'Recently',
            'how': 'Armed robbery, attempted escape',
            'why': '',
            'economic_loss': '',
            'injuries': '',
            'fatalities': '',
            'arrests': '1 man arrested'
        },
        {
            # Completely different story (should be kept)
            'headline': 'Highway Accident Causes Traffic Delays',
            'source': 'Traffic News',
            'url': 'https://traffic.com/accident',
            'date_scraped': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'full_text': 'A three-car collision on Highway 101 during rush hour resulted in significant traffic delays and two minor injuries.',
            'who': 'Drivers involved',
            'what': 'Traffic accident',
            'where': 'Highway 101',
            'when': 'Rush hour',
            'how': 'Three-car collision',
            'why': '',
            'economic_loss': '',
            'injuries': '2 minor injuries',
            'fatalities': '',
            'arrests': ''
        }
    ]
    
    print(f"Processing {len(test_articles)} test articles...")
    print()
    
    # Track hashes manually for demonstration
    tracked_hashes = set()
    tracked_similarity = set()
    
    results = []
    for i, article in enumerate(test_articles, 1):
        print(f"Article {i}: {article['headline'][:50]}...")
        print(f"  Source: {article['source']}")
        
        # Manually check for demonstration purposes
        from utils import check_duplicate_article
        
        duplicate_check = check_duplicate_article(
            article, tracked_hashes, tracked_similarity, article['source']
        )
        
        print(f"  Duplicate Check: {duplicate_check}")
        
        # Now save with the system
        result = append_to_csv_with_dedup(article)
        results.append(result)
        
        # Update our tracking sets
        if not duplicate_check['is_duplicate']:
            tracked_hashes.add(duplicate_check.get('exact_hash', ''))
            tracked_similarity.add(duplicate_check.get('similarity_hash', ''))
        elif duplicate_check.get('allow_duplicate'):
            tracked_hashes.add(duplicate_check.get('hash', ''))
            tracked_similarity.add(duplicate_check.get('hash', ''))
        
        if result['success']:
            status = "✓ SAVED"
            if result.get('duplicate_info'):
                status += f" (noted as similar to different source)"
        elif result.get('skipped'):
            status = "✗ SKIPPED"
        else:
            status = "✗ ERROR"
        
        print(f"  Result: {status}")
        if result.get('reason'):
            print(f"  Reason: {result['reason']}")
        print()
    
    # Summary
    saved = sum(1 for r in results if r['success'])
    skipped = sum(1 for r in results if r.get('skipped'))
    failed = sum(1 for r in results if not r['success'] and not r.get('skipped'))
    
    print("=" * 50)
    print("DUPLICATE DETECTION SUMMARY:")
    print(f"✓ Articles Saved: {saved}")
    print(f"✗ Duplicates Skipped: {skipped}")
    print(f"✗ Failed: {failed}")
    print()
    print("Expected behavior:")
    print("- Article 1: Saved (new)")
    print("- Article 2: Skipped (exact duplicate, same source)")
    print("- Article 3: Saved (similar content, different source)")
    print("- Article 4: Saved (different content)")
    print()
    
    if saved == 3 and skipped == 1:
        print("🎉 DUPLICATE DETECTION WORKING PERFECTLY!")
    else:
        print("⚠️  Unexpected results - check configuration")
    
    return True

if __name__ == "__main__":
    demo_duplicate_detection()
