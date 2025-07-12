"""
Comprehensive source testing and filtering script
Tests all sources from source_array.py and creates a verified accessible list
"""

import sys
import time
from typing import List, Dict
from main import CrimeDataScraper
from scraper import WebScraper
from config import ALL_NEWS_SOURCES

def test_all_sources() -> Dict:
    """
    Test all sources and categorize them by accessibility
    
    Returns:
        Dict: Results with accessible, blocked, and failed sources
    """
    
    print("🌐 Crime Data Scraper - Comprehensive Source Testing")
    print("=" * 70)
    print(f"Testing {len(ALL_NEWS_SOURCES)} news sources from around the world...")
    print()
    
    scraper = WebScraper()
    
    accessible_sources = []
    blocked_sources = []
    failed_sources = []
    timeout_sources = []
    
    total_sources = len(ALL_NEWS_SOURCES)
    
    for i, source in enumerate(ALL_NEWS_SOURCES, 1):
        source_name = source['name']
        source_url = source['url']
        
        print(f"[{i:3d}/{total_sources}] Testing: {source_name[:50]:<50}", end=" ")
        
        try:
            # Test connectivity with timeout
            start_time = time.time()
            soup = scraper.get_page_content(source_url)
            response_time = time.time() - start_time
            
            if soup:
                accessible_sources.append({
                    **source,
                    'response_time': round(response_time, 2),
                    'status': 'accessible'
                })
                print(f"✅ OK ({response_time:.1f}s)")
            else:
                blocked_sources.append({
                    **source,
                    'status': 'blocked',
                    'error': 'No content returned'
                })
                print("❌ BLOCKED")
                
        except Exception as e:
            error_msg = str(e).lower()
            
            if 'timeout' in error_msg or 'timed out' in error_msg:
                timeout_sources.append({
                    **source,
                    'status': 'timeout',
                    'error': str(e)
                })
                print("⏱️  TIMEOUT")
            elif '403' in error_msg or 'forbidden' in error_msg:
                blocked_sources.append({
                    **source,
                    'status': 'forbidden',
                    'error': str(e)
                })
                print("🚫 FORBIDDEN")
            elif '404' in error_msg or 'not found' in error_msg:
                failed_sources.append({
                    **source,
                    'status': 'not_found',
                    'error': str(e)
                })
                print("❓ NOT FOUND")
            elif '401' in error_msg or 'unauthorized' in error_msg:
                blocked_sources.append({
                    **source,
                    'status': 'unauthorized',
                    'error': str(e)
                })
                print("🔒 UNAUTHORIZED")
            else:
                failed_sources.append({
                    **source,
                    'status': 'error',
                    'error': str(e)
                })
                print(f"❌ ERROR: {str(e)[:30]}...")
        
        # Small delay to be respectful
        time.sleep(0.5)
    
    return {
        'accessible': accessible_sources,
        'blocked': blocked_sources,
        'failed': failed_sources,
        'timeout': timeout_sources,
        'total_tested': total_sources
    }

def generate_accessible_config(accessible_sources: List[Dict]) -> str:
    """
    Generate Python config code for accessible sources
    
    Args:
        accessible_sources: List of accessible source dictionaries
        
    Returns:
        str: Python code for the configuration
    """
    
    config_code = "# Verified accessible news sources\n"
    config_code += "# Generated automatically by source tester\n"
    config_code += f"# Tested on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    config_code += "VERIFIED_NEWS_WEBSITES = [\n"
    
    for source in accessible_sources:
        config_code += "    {\n"
        config_code += f"        \"name\": \"{source['name']}\",\n"
        config_code += f"        \"url\": \"{source['url']}\",\n"
        config_code += f"        \"article_selector\": \"{source['article_selector']}\",\n"
        config_code += f"        \"headline_selector\": \"{source['headline_selector']}\",\n"
        config_code += f"        \"content_selector\": \"{source['content_selector']}\",\n"
        config_code += f"        \"response_time\": {source['response_time']},\n"
        config_code += f"        \"verified_date\": \"{time.strftime('%Y-%m-%d')}\"\n"
        config_code += "    },\n"
    
    config_code += "]\n"
    
    return config_code

def categorize_sources_by_region(sources: List[Dict]) -> Dict:
    """
    Categorize sources by geographical region
    
    Args:
        sources: List of source dictionaries
        
    Returns:
        Dict: Sources categorized by region
    """
    
    regions = {
        'North America': [],
        'Europe': [],
        'Asia': [],
        'Latin America': [],
        'Africa': [],
        'Australia/Oceania': [],
        'Other': []
    }
    
    # Simple categorization based on domains and names
    for source in sources:
        name = source['name'].lower()
        url = source['url'].lower()
        
        if any(x in name or x in url for x in ['canada', 'usa', 'us ', 'america', 'toronto', 'cbc', 'cnn', 'fox', 'nbc', 'cbs']):
            regions['North America'].append(source)
        elif any(x in name or x in url for x in ['uk', 'britain', 'bbc', 'guardian', 'europe', 'germany', 'france', 'italy', 'spain', 'sweden', 'norway', 'denmark']):
            regions['Europe'].append(source)
        elif any(x in name or x in url for x in ['japan', 'china', 'india', 'korea', 'asia', 'singapore', 'thailand', 'hong kong']):
            regions['Asia'].append(source)
        elif any(x in name or x in url for x in ['mexico', 'brazil', 'argentina', 'colombia', 'chile', 'peru']):
            regions['Latin America'].append(source)
        elif any(x in name or x in url for x in ['africa', 'south africa', 'nigeria', 'kenya', 'ghana', 'egypt']):
            regions['Africa'].append(source)
        elif any(x in name or x in url for x in ['australia', 'zealand', 'sydney', 'melbourne']):
            regions['Australia/Oceania'].append(source)
        else:
            regions['Other'].append(source)
    
    return regions

def print_detailed_results(results: Dict):
    """
    Print detailed test results with statistics and categorization
    
    Args:
        results: Results dictionary from test_all_sources()
    """
    
    accessible = results['accessible']
    blocked = results['blocked']
    failed = results['failed']
    timeout = results['timeout']
    total = results['total_tested']
    
    print("\n" + "=" * 70)
    print("📊 COMPREHENSIVE SOURCE TEST RESULTS")
    print("=" * 70)
    
    # Overall statistics
    print(f"Total Sources Tested: {total}")
    print(f"✅ Accessible: {len(accessible)} ({len(accessible)/total*100:.1f}%)")
    print(f"🚫 Blocked/Forbidden: {len(blocked)} ({len(blocked)/total*100:.1f}%)")
    print(f"❌ Failed/Error: {len(failed)} ({len(failed)/total*100:.1f}%)")
    print(f"⏱️  Timeout: {len(timeout)} ({len(timeout)/total*100:.1f}%)")
    
    # Regional breakdown of accessible sources
    if accessible:
        print(f"\n🌍 ACCESSIBLE SOURCES BY REGION:")
        regions = categorize_sources_by_region(accessible)
        for region, sources in regions.items():
            if sources:
                print(f"  {region}: {len(sources)} sources")
                for source in sources[:3]:  # Show first 3 from each region
                    print(f"    - {source['name']} ({source['response_time']}s)")
                if len(sources) > 3:
                    print(f"    ... and {len(sources) - 3} more")
    
    # Top 10 fastest accessible sources
    if accessible:
        print(f"\n⚡ TOP 10 FASTEST ACCESSIBLE SOURCES:")
        fastest = sorted(accessible, key=lambda x: x['response_time'])[:10]
        for i, source in enumerate(fastest, 1):
            print(f"  {i:2d}. {source['name'][:45]:<45} ({source['response_time']:4.1f}s)")
    
    # Sample of blocked sources with reasons
    if blocked:
        print(f"\n🚫 SAMPLE BLOCKED SOURCES:")
        for source in blocked[:10]:
            status = source.get('status', 'blocked').upper()
            print(f"  - {source['name'][:50]:<50} [{status}]")
    
    print(f"\n💾 Configuration files will be generated with {len(accessible)} verified sources.")

def main():
    """
    Main function to run comprehensive source testing
    """
    
    try:
        # Run the comprehensive test
        results = test_all_sources()
        
        # Print detailed results
        print_detailed_results(results)
        
        # Generate configuration for accessible sources
        accessible_sources = results['accessible']
        
        if accessible_sources:
            # Generate config file
            config_content = generate_accessible_config(accessible_sources)
            
            # Save to file
            with open('verified_sources_config.py', 'w', encoding='utf-8') as f:
                f.write(config_content)
            
            print(f"\n📁 Generated: verified_sources_config.py ({len(accessible_sources)} sources)")
            
            # Also create a summary file
            summary = f"""
SOURCE TESTING SUMMARY
Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}

STATISTICS:
- Total Tested: {results['total_tested']}
- Accessible: {len(results['accessible'])}
- Blocked: {len(results['blocked'])}
- Failed: {len(results['failed'])}
- Timeout: {len(results['timeout'])}

SUCCESS RATE: {len(accessible_sources)/results['total_tested']*100:.1f}%

RECOMMENDED ACTION:
Update config.py NEWS_WEBSITES with sources from verified_sources_config.py
"""
            
            with open('source_test_summary.txt', 'w', encoding='utf-8') as f:
                f.write(summary)
            
            print(f"📄 Generated: source_test_summary.txt")
            
            # Suggest next steps
            print(f"\n🎯 NEXT STEPS:")
            print(f"1. Review verified_sources_config.py")
            print(f"2. Update config.py NEWS_WEBSITES with verified sources")
            print(f"3. Run: python main.py --mode test")
            print(f"4. Run: python main.py --mode full")
            
        else:
            print("\n❌ No accessible sources found. Check network connectivity and try again.")
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Testing interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")

if __name__ == "__main__":
    main()
