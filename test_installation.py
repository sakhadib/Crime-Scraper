"""
Test script to validate the Crime Data Scraper installation and configuration
"""

import os
import sys
import importlib
from datetime import datetime

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    required_modules = [
        'requests', 'beautifulsoup4', 'spacy', 'pandas', 
        'fake_useragent', 'schedule', 'dateutil'
    ]
    
    for module in required_modules:
        try:
            if module == 'beautifulsoup4':
                import bs4
                print(f"✓ {module} (bs4) imported successfully")
            elif module == 'dateutil':
                import dateutil
                print(f"✓ {module} imported successfully")
            else:
                importlib.import_module(module)
                print(f"✓ {module} imported successfully")
        except ImportError as e:
            print(f"✗ Failed to import {module}: {e}")
            return False
    
    return True

def test_spacy_model():
    """Test that spaCy model is available"""
    print("\nTesting spaCy model...")
    
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        
        # Test with sample text
        doc = nlp("John Smith was arrested in New York yesterday.")
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        
        print(f"✓ spaCy model loaded successfully")
        print(f"  Sample entities: {entities}")
        return True
        
    except Exception as e:
        print(f"✗ spaCy model test failed: {e}")
        print("  Try running: python -m spacy download en_core_web_sm")
        return False

def test_project_modules():
    """Test that project modules can be imported"""
    print("\nTesting project modules...")
    
    project_modules = ['config', 'utils', 'scraper', 'nlp_processor', 'main']
    
    for module in project_modules:
        try:
            importlib.import_module(module)
            print(f"✓ {module}.py imported successfully")
        except ImportError as e:
            print(f"✗ Failed to import {module}: {e}")
            return False
    
    return True

def test_directories():
    """Test that required directories exist or can be created"""
    print("\nTesting directories...")
    
    required_dirs = ['data', 'logs']
    
    for dir_name in required_dirs:
        try:
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
                print(f"✓ Created directory: {dir_name}")
            else:
                print(f"✓ Directory exists: {dir_name}")
        except Exception as e:
            print(f"✗ Failed to create directory {dir_name}: {e}")
            return False
    
    return True

def test_csv_functionality():
    """Test CSV file creation and writing"""
    print("\nTesting CSV functionality...")
    
    try:
        from utils import ensure_csv_exists, append_to_csv
        
        # Test CSV creation
        ensure_csv_exists()
        print("✓ CSV file creation successful")
        
        # Test data appending
        test_data = {
            'date_scraped': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'article_url': 'http://test.com/article1',
            'headline': 'Test Article',
            'publication_date': '2024-01-01',
            'who': 'Test Person',
            'what': 'test crime',
            'where': 'Test City',
            'when': '2024-01-01',
            'how': 'test method',
            'why': 'test reason',
            'economic_loss': '$100',
            'injuries': '0',
            'fatalities': '0',
            'arrests': '1',
            'full_text': 'This is a test article.'
        }
        
        success = append_to_csv(test_data)
        if success:
            print("✓ CSV data writing successful")
        else:
            print("✗ CSV data writing failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ CSV functionality test failed: {e}")
        return False

def test_nlp_processor():
    """Test NLP processor functionality"""
    print("\nTesting NLP processor...")
    
    try:
        from nlp_processor import CrimeNLPProcessor
        
        processor = CrimeNLPProcessor()
        
        # Test with sample article
        sample_article = {
            'headline': 'Bank Robbery in Downtown',
            'content': 'Two suspects robbed First National Bank on Main Street yesterday. John Doe was injured during the incident. Police arrested one suspect.',
            'url': 'http://test.com/article'
        }
        
        result = processor.process_article(sample_article)
        
        if result and 'headline' in result:
            print("✓ NLP processor working successfully")
            print(f"  Extracted crime type: {result.get('what', 'None')}")
            print(f"  Extracted location: {result.get('where', 'None')}")
            print(f"  Extracted person: {result.get('who', 'None')}")
            return True
        else:
            print("✗ NLP processor failed to process article")
            return False
            
    except Exception as e:
        print(f"✗ NLP processor test failed: {e}")
        return False

def test_web_scraper():
    """Test web scraper basic functionality"""
    print("\nTesting web scraper...")
    
    try:
        from scraper import WebScraper
        
        scraper = WebScraper()
        
        # Test with a simple webpage
        test_url = "https://httpbin.org/html"
        soup = scraper.get_page_content(test_url)
        
        if soup:
            print("✓ Web scraper can fetch web pages")
            return True
        else:
            print("✗ Web scraper failed to fetch test page")
            return False
            
    except Exception as e:
        print(f"✗ Web scraper test failed: {e}")
        return False

def run_all_tests():
    """Run all tests and provide summary"""
    print("=" * 50)
    print("Crime Data Scraper Installation Test")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("spaCy Model", test_spacy_model),
        ("Project Modules", test_project_modules),
        ("Directories", test_directories),
        ("CSV Functionality", test_csv_functionality),
        ("NLP Processor", test_nlp_processor),
        ("Web Scraper", test_web_scraper)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All tests passed! The Crime Data Scraper is ready to use.")
        print("\nNext steps:")
        print("1. Configure websites in config.py")
        print("2. Run: python main.py --mode test")
        print("3. Run: python main.py --mode full")
    else:
        print(f"\n✗ {total - passed} tests failed. Please address the issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
