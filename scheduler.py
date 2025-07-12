"""
Automation scheduler for the Crime Data Scraper
Handles scheduling and running the scraper at specified intervals
"""

import schedule
import time
import subprocess
import sys
import os
from datetime import datetime
from utils import setup_logging

class CrimeScraperScheduler:
    """
    Scheduler class for automating crime data scraping
    """
    
    def __init__(self):
        self.logger = setup_logging()
        self.script_path = os.path.join(os.path.dirname(__file__), 'main.py')
        self.python_path = sys.executable
    
    def run_scraper(self):
        """
        Run the scraper script
        """
        try:
            self.logger.info("Starting scheduled scrape")
            start_time = datetime.now()
            
            # Run the main scraper script
            result = subprocess.run(
                [self.python_path, self.script_path, '--mode', 'full'],
                capture_output=True,
                text=True,
                timeout=3600  # 1 hour timeout
            )
            
            end_time = datetime.now()
            duration = end_time - start_time
            
            if result.returncode == 0:
                self.logger.info(f"Scheduled scrape completed successfully in {duration}")
                self.logger.info(f"Output: {result.stdout}")
            else:
                self.logger.error(f"Scheduled scrape failed with return code {result.returncode}")
                self.logger.error(f"Error: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            self.logger.error("Scheduled scrape timed out after 1 hour")
        except Exception as e:
            self.logger.error(f"Error running scheduled scrape: {str(e)}")
    
    def schedule_daily(self, time_str: str = "09:00"):
        """
        Schedule daily scraping at specified time
        
        Args:
            time_str (str): Time in HH:MM format (24-hour)
        """
        schedule.every().day.at(time_str).do(self.run_scraper)
        self.logger.info(f"Scheduled daily scraping at {time_str}")
    
    def schedule_hourly(self):
        """
        Schedule hourly scraping
        """
        schedule.every().hour.do(self.run_scraper)
        self.logger.info("Scheduled hourly scraping")
    
    def schedule_every_n_hours(self, hours: int):
        """
        Schedule scraping every N hours
        
        Args:
            hours (int): Number of hours between scrapes
        """
        schedule.every(hours).hours.do(self.run_scraper)
        self.logger.info(f"Scheduled scraping every {hours} hours")
    
    def run_scheduler(self):
        """
        Run the scheduler (blocking)
        """
        self.logger.info("Starting Crime Data Scraper scheduler")
        self.logger.info("Press Ctrl+C to stop the scheduler")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            self.logger.info("Scheduler stopped by user")
        except Exception as e:
            self.logger.error(f"Scheduler error: {str(e)}")

def main():
    """
    Main function for the scheduler
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Crime Data Scraper Scheduler')
    parser.add_argument('--schedule', choices=['daily', 'hourly', 'custom'], 
                       default='daily', help='Scheduling frequency')
    parser.add_argument('--time', type=str, default='09:00', 
                       help='Time for daily schedule (HH:MM format)')
    parser.add_argument('--hours', type=int, default=6,
                       help='Hours interval for custom schedule')
    parser.add_argument('--run-once', action='store_true',
                       help='Run scraper once and exit')
    
    args = parser.parse_args()
    
    scheduler = CrimeScraperScheduler()
    
    if args.run_once:
        scheduler.run_scraper()
        return
    
    if args.schedule == 'daily':
        scheduler.schedule_daily(args.time)
    elif args.schedule == 'hourly':
        scheduler.schedule_hourly()
    elif args.schedule == 'custom':
        scheduler.schedule_every_n_hours(args.hours)
    
    scheduler.run_scheduler()

if __name__ == "__main__":
    main()
