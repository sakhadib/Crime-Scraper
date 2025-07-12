You are tasked with building an AI Agent that will scrape crime-related news articles from news websites, extract specific details from them, and save this information in a structured format (CSV). The project should be scalable, and the code should be modular and easy to expand upon. Start with scraping and data extraction, and later allow for future scaling to more advanced techniques.

### Requirements:

1. **Web Scraping**:
   - Write Python code to scrape news articles from a specified list of local news websites.
   - Extract the headlines and article links from the main news page.
   - Filter the articles by checking if they contain crime-related keywords like "robbery", "vandalism", "murder", "assault", "theft", etc.
   
2. **NLP for Data Extraction**:
   - Use **spaCy** to process each article's text and extract key information:
     - Who (person names)
     - When (dates)
     - Where (locations)
     - What (type of crime, e.g., robbery, assault)
     - How (method or description of the crime)
     - Why (motivation if available)
     - Additional details like economic loss, injuries, fatalities, arrests.
   - Store the extracted information in a dictionary or similar structure for easy access.

3. **Data Storage in CSV Format**:
   - Create a CSV file to store the extracted details for each crime article.
   - Each row should contain:
     - Date
     - Who (person involved)
     - What (crime type)
     - Where (location)
     - When (date)
     - How (method)
     - Why (if provided)
     - Economic Loss (if available)
     - Injuries (if available)
     - Fatalities (if available)
     - Arrests (if available)
   - The CSV file should be updated automatically with new articles without overwriting existing data.

4. **Automation**:
   - Write Python code to automate the process of scraping and saving new articles on a daily basis.
   - Allow for easy scheduling of the scraping script to run at specific intervals (e.g., daily at 9 AM). Provide instructions for setting up the automation using **cron** (Linux/macOS) or **Task Scheduler** (Windows).

5. **Error Handling**:
   - Implement error handling for issues like network errors, missing data, or broken links during the scraping process.
   - Ensure that failed attempts are logged and retried without disrupting the entire process.

6. **Scalability (Future)**:
   - Provide guidance on how to transition from storing data in CSV to a **vector database** (e.g., FAISS, Weaviate) once the dataset grows large.
   - Explain how to store and search data more efficiently using vector embeddings for crime-related articles when the dataset reaches hundreds of thousands of rows.
   - Provide examples of how to perform similarity searches and clustering of crime data once a vector database is implemented.

7. **Ethical Considerations**:
   - Advise on ethical considerations, including handling potentially biased data and ensuring privacy and fairness in the dataset.
   - Consider strategies for detecting and avoiding bias in crime-related news data.
   - Discuss the potential risks of propagating false information or stereotypes based on scraped data.

8. **Documentation**:
   - Comment the code thoroughly to explain each step and its purpose.
   - Provide documentation on how to run and modify the script, including setup instructions for the required libraries.

### Technologies:
- **Web Scraping**: `requests`, `BeautifulSoup`
- **NLP**: `spaCy` for named entity recognition (NER)
- **Data Storage**: `csv`, `pandas`
- **Automation**: `cron` or **Task Scheduler**
- **Future Scaling**: FAISS, Weaviate (optional for later)

---

Build the entire workflow, including scraping, data extraction, storage, and automation, ensuring that it's modular and can be expanded later. The initial focus should be on scraping crime-related articles, extracting relevant data, and saving that data in a CSV file for easy analysis.

