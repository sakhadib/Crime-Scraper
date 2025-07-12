"""
Test script for duplicate detection functionality
"""

import sys
import os
from utils import (
    generate_content_hash, 
    generate_similarity_hash, 
    check_duplicate_article,
    append_to_csv_with_dedup
)

def test_duplicate_detection():
    """Test the duplicate detection system"""
    
    print("Testing Crime Data Scraper Duplicate Detection System")
    print("=" * 60)
    
    # Test data - same article from different sources
    article1 = {
        'headline': 'Local Man Arrested for Armed Robbery at Downtown Bank',
        'content': 'Police arrested a 25-year-old man yesterday for armed robbery at First National Bank downtown. The suspect fled the scene but was apprehended two blocks away. No injuries were reported.',
        'source': 'Local News 1'
    }
    
    # Exact duplicate from same source
    article2 = {
        'headline': 'Local Man Arrested for Armed Robbery at Downtown Bank',
        'content': 'Police arrested a 25-year-old man yesterday for armed robbery at First National Bank downtown. The suspect fled the scene but was apprehended two blocks away. No injuries were reported.',
        'source': 'Local News 1'
    }
    
    # Same story, different source (should be kept)
    article3 = {
        'headline': 'Bank Robbery Suspect Arrested Downtown',
        'content': 'A 25-year-old male was taken into custody yesterday following an armed robbery at First National Bank in the downtown area. The perpetrator escaped initially but was caught nearby. There were no reported injuries.',
        'source': 'City Tribune'
    }
    
    # Completely different article
    article4 = {
        'headline': 'Traffic Accident on Highway 101 Results in Two Injuries',
        'content': 'Two people were hospitalized following a three-car collision on Highway 101 during rush hour. Emergency responders arrived quickly at the scene.',
        'source': 'Traffic News'
    }
    
    print("1. Testing hash generation:")
    hash1 = generate_content_hash(article1['headline'], article1['content'], article1['source'])
    hash2 = generate_content_hash(article2['headline'], article2['content'], article2['source'])
    hash3 = generate_content_hash(article3['headline'], article3['content'], article3['source'])
    
    print(f"   Article 1 hash: {hash1[:16]}...")
    print(f"   Article 2 hash: {hash2[:16]}...")
    print(f"   Article 3 hash: {hash3[:16]}...")
    print(f"   Articles 1&2 same hash: {hash1 == hash2}")
    print(f"   Articles 1&3 same hash: {hash1 == hash3}")
    
    print("\n2. Testing similarity detection:")
    sim1 = generate_similarity_hash(article1['headline'], article1['content'])
    sim3 = generate_similarity_hash(article3['headline'], article3['content'])
    sim4 = generate_similarity_hash(article4['headline'], article4['content'])
    
    print(f"   Article 1 similarity: {sim1}")
    print(f"   Article 3 similarity: {sim3}")
    print(f"   Article 4 similarity: {sim4}")
    print(f"   Articles 1&3 similar: {sim1 == sim3}")
    print(f"   Articles 1&4 similar: {sim1 == sim4}")
    
    print("\n3. Testing duplicate detection logic:")
    
    # Track hashes
    existing_hashes = set()
    similarity_hashes = set()
    
    # Process first article
    result1 = check_duplicate_article(article1, existing_hashes, similarity_hashes, article1['source'])
    print(f"   Article 1: {result1}")
    if not result1['is_duplicate']:
        existing_hashes.add(result1['exact_hash'])
        similarity_hashes.add(result1['similarity_hash'])
    
    # Process exact duplicate
    result2 = check_duplicate_article(article2, existing_hashes, similarity_hashes, article2['source'])
    print(f"   Article 2 (exact duplicate): {result2}")
    
    # Process similar article from different source
    result3 = check_duplicate_article(article3, existing_hashes, similarity_hashes, article3['source'])
    print(f"   Article 3 (similar, diff source): {result3}")
    if not result3['is_duplicate'] or result3.get('allow_duplicate'):
        existing_hashes.add(result3.get('exact_hash', ''))
        similarity_hashes.add(result3.get('similarity_hash', ''))
    
    # Process different article
    result4 = check_duplicate_article(article4, existing_hashes, similarity_hashes, article4['source'])
    print(f"   Article 4 (different): {result4}")
    
    print("\n4. Expected behavior:")
    print("   ✓ Article 1: Should be saved (new)")
    print("   ✗ Article 2: Should be skipped (exact duplicate, same source)")
    print("   ✓ Article 3: Should be saved (similar content, different source)")
    print("   ✓ Article 4: Should be saved (different content)")
    
    print("\n5. Results summary:")
    if not result1['is_duplicate']:
        print("   ✓ Article 1: SAVED")
    else:
        print("   ✗ Article 1: ERROR - should not be duplicate")
    
    if result2['is_duplicate'] and result2['duplicate_type'] == 'exact_same_source':
        print("   ✓ Article 2: SKIPPED (correct - exact duplicate)")
    else:
        print("   ✗ Article 2: ERROR - should be detected as exact duplicate")
    
    if not result3['is_duplicate'] or result3.get('allow_duplicate'):
        print("   ✓ Article 3: SAVED (correct - different source)")
    else:
        print("   ✗ Article 3: ERROR - should be kept despite similarity")
    
    if not result4['is_duplicate']:
        print("   ✓ Article 4: SAVED (correct - different content)")
    else:
        print("   ✗ Article 4: ERROR - should not be duplicate")
    
    print("\n" + "=" * 60)
    print("Duplicate detection test completed!")
    
    return True

if __name__ == "__main__":
    test_duplicate_detection()
