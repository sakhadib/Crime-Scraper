"""
Simple duplicate detection test without CSV dependencies
"""

def test_duplicate_logic():
    """Test just the duplicate detection logic"""
    
    from utils import generate_content_hash, generate_similarity_hash, check_duplicate_article
    
    print("Crime Data Scraper - Duplicate Detection Core Logic Test")
    print("=" * 60)
    
    # Test articles
    article1 = {
        'headline': 'Local Bank Robbery Leads to Arrest',
        'full_text': 'Police arrested a suspect yesterday after a robbery at First National Bank downtown. The 30-year-old male fled but was caught nearby.',
        'source': 'City News'
    }
    
    # Exact duplicate from same source
    article2 = {
        'headline': 'Local Bank Robbery Leads to Arrest',
        'full_text': 'Police arrested a suspect yesterday after a robbery at First National Bank downtown. The 30-year-old male fled but was caught nearby.',
        'source': 'City News'
    }
    
    # Similar story from different source
    article3 = {
        'headline': 'Bank Robber Apprehended After Downtown Crime',
        'full_text': 'A 30-year-old man was arrested following an armed robbery at First National Bank in the downtown area. The perpetrator attempted to escape but was captured.',
        'source': 'Metro Tribune'
    }
    
    # Different story
    article4 = {
        'headline': 'Highway Accident Causes Traffic Delays',
        'full_text': 'A three-car collision on Highway 101 during rush hour resulted in significant traffic delays and two minor injuries.',
        'source': 'Traffic News'
    }
    
    # Track hashes
    existing_hashes = set()
    similarity_hashes = set()
    
    articles = [article1, article2, article3, article4]
    results = []
    
    print("Processing articles:")
    print()
    
    for i, article in enumerate(articles, 1):
        print(f"Article {i}: {article['headline'][:40]}...")
        print(f"  Source: {article['source']}")
        
        # Check for duplicate
        result = check_duplicate_article(article, existing_hashes, similarity_hashes, article['source'])
        results.append(result)
        
        # Print result
        if result['is_duplicate']:
            if result['duplicate_type'] == 'exact_same_source':
                print(f"  Status: ✗ DUPLICATE (exact, same source)")
                print(f"  Action: SKIP")
            elif result['duplicate_type'] == 'similar_cross_source':
                print(f"  Status: ⚠ SIMILAR (different source)")
                print(f"  Action: KEEP BOTH")
                # Add to tracking sets
                existing_hashes.add(result.get('hash', ''))
                similarity_hashes.add(result.get('hash', ''))
        else:
            print(f"  Status: ✓ NEW")
            print(f"  Action: SAVE")
            # Add to tracking sets
            existing_hashes.add(result['exact_hash'])
            similarity_hashes.add(result['similarity_hash'])
        
        print()
    
    # Summary
    print("=" * 60)
    print("RESULTS SUMMARY:")
    print(f"Article 1: {'SAVED' if not results[0]['is_duplicate'] else 'SKIPPED'} (expected: SAVED)")
    print(f"Article 2: {'SAVED' if not results[1]['is_duplicate'] else 'SKIPPED'} (expected: SKIPPED)")
    print(f"Article 3: {'SAVED' if not results[2]['is_duplicate'] or results[2].get('allow_duplicate') else 'SKIPPED'} (expected: SAVED)")
    print(f"Article 4: {'SAVED' if not results[3]['is_duplicate'] else 'SKIPPED'} (expected: SAVED)")
    
    # Check if results match expectations
    expected = [False, True, True, False]  # is_duplicate flags
    actual = [r['is_duplicate'] for r in results]
    
    print()
    if expected[0] == actual[0] and expected[1] == actual[1] and expected[3] == actual[3]:
        # Special case for article 3 - similar but different source should be allowed
        if results[2]['is_duplicate'] and results[2].get('allow_duplicate'):
            print("🎉 DUPLICATE DETECTION WORKING PERFECTLY!")
        elif not results[2]['is_duplicate']:
            print("🎉 DUPLICATE DETECTION WORKING PERFECTLY!")
        else:
            print("⚠️ Article 3 handling needs adjustment")
    else:
        print("⚠️ Some results don't match expectations")
    
    print()
    print("Hash examples:")
    for i, result in enumerate(results, 1):
        hash_val = result.get('exact_hash', result.get('hash', 'N/A'))
        print(f"Article {i}: {hash_val[:16]}...")

if __name__ == "__main__":
    test_duplicate_logic()
