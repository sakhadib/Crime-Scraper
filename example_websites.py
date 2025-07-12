"""
Example website configurations for testing the scraper
This file contains real website configurations that can be used for testing
"""

# Example configurations for popular news websites
# Note: Always check robots.txt and terms of service before scraping

EXAMPLE_WEBSITES = [
    {
        "name": "BBC News",
        "url": "https://www.bbc.com/news",
        "article_selector": "h3 a[href*='/news/']",
        "headline_selector": "h1",
        "content_selector": "div[data-component='text-block']"
    },
    {
        "name": "CNN",
        "url": "https://www.cnn.com",
        "article_selector": "h3 a[href*='/2024/']",
        "headline_selector": "h1.headline__text",
        "content_selector": "div.zn-body__paragraph"
    },
    {
        "name": "Reuters",
        "url": "https://www.reuters.com/world/",
        "article_selector": "h3 a[href*='/world/']",
        "headline_selector": "h1",
        "content_selector": "div[data-testid='paragraph']"
    },
    {
        "name": "Local News Example",
        "url": "https://example-local-news.com",
        "article_selector": "article h2 a",
        "headline_selector": "h1.article-title",
        "content_selector": "div.article-content p"
    }
]

# Crime-specific news sources
CRIME_NEWS_SOURCES = [
    {
        "name": "Crime Online",
        "url": "https://www.crimeonline.com",
        "article_selector": "h2.entry-title a",
        "headline_selector": "h1.entry-title",
        "content_selector": "div.entry-content p"
    },
    {
        "name": "Police1",
        "url": "https://www.police1.com/crime/",
        "article_selector": "h3 a[href*='/crime/']",
        "headline_selector": "h1",
        "content_selector": "div.article-content p"
    }
]

# Local news websites (examples - replace with actual local news sources)
LOCAL_NEWS_SOURCES = [
    {
        "name": "Chicago Tribune Crime",
        "url": "https://www.chicagotribune.com/news/breaking/",
        "article_selector": "h3 a[href*='/news/']",
        "headline_selector": "h1",
        "content_selector": "p.trb_ar_page_txt"
    },
    {
        "name": "Los Angeles Times Crime",
        "url": "https://www.latimes.com/california/",
        "article_selector": "h3 a[href*='/california/']",
        "headline_selector": "h1",
        "content_selector": "div.rich-text p"
    },
    {
        "name": "New York Post Crime",
        "url": "https://nypost.com/metro/",
        "article_selector": "h3 a[href*='/2024/']",
        "headline_selector": "h1",
        "content_selector": "div.entry-content p"
    }
]

# RSS feed configurations (alternative approach)
RSS_FEEDS = [
    {
        "name": "Police1 RSS",
        "url": "https://www.police1.com/rss/crime.xml",
        "type": "rss"
    },
    {
        "name": "Crime Online RSS", 
        "url": "https://www.crimeonline.com/feed/",
        "type": "rss"
    }
]

def get_test_website():
    """
    Get a test website configuration for development
    """
    return {
        "name": "Test Website",
        "url": "https://httpbin.org/html",  # Simple HTML test page
        "article_selector": "h1",
        "headline_selector": "h1",
        "content_selector": "p"
    }
