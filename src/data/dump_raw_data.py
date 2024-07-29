import logging
import os
import time
from pathlib import Path
from web_scraper_function import extract_data
from web_crawler import extract_links

def scrape_and_save(base_url, output_filepath):
    i = 0
    logger = logging.getLogger(__name__)
    logger.info('Starting data extraction process')
    
    links = extract_links(base_url)
    all_data = []

    for link in links:
        print(f'Extracting data from {i} {link}')
        data = extract_data(link)
        all_data.append(data)
        i = i+1
        time.sleep(4)


    # Print the extracted data
    # print(all_data)
    print(len(all_data))
    os.makedirs(os.path.dirname(output_filepath), exist_ok=True)

    with open(output_filepath, 'w') as f:
        f.write(str(all_data))


base_url = 'https://www.carwale.com/tata-cars/expert-reviews/'
output_filepath = Path('data/raw/extracted_data.txt').resolve()
scrape_and_save(base_url, output_filepath)