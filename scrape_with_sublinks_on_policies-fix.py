# Import Libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

# CSV File Names
csv_links = 'fordham_links.csv'
csv_policies = 'fordham_policies.csv'
csv_links_in_policies = 'fordham_links_in_policies.csv'

# FUNCTION: Scrape Links from Main Policy Page
def scrape_fordham_links():
    # Initialize the Selenium WebDriver (make sure you have the Chrome driver installed)
    driver = webdriver.Chrome()

    try:
        # Navigate to the webpage
        url = 'https://www.fordham.edu/information-technology/it-security--assurance/it-policies-procedures-and-guidelines/'
        driver.get(url)
        time.sleep(5)  # Wait for the page to load (adjust time as needed)

        # Find all links on the page
        links = driver.find_elements(By.TAG_NAME, 'a')

        # Extract link URLs and text
        link_data = []
        for link in links:
            href = link.get_attribute('href')
            text = link.text
            if href and text and (url in href):
                link_data.append({'URL': href, 'Text': text})

        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(link_data)

        # Save the DataFrame to a CSV file
        df.to_csv(csv_links, index=False)
        print(f"Links have been scraped and saved to " + csv_links + " from " + url)

        # Call scrape_fordham_sublinks after the DataFrame is saved
        scrape_fordham_sublinks()

    finally:
        # Close the WebDriver
        driver.quit()

# FUNCTION: Scrape Sub-Links Found on Main Policy Page
def scrape_fordham_sublinks():
    # Initialize the Selenium WebDriver (make sure you have the Chrome driver installed)
    driver = webdriver.Chrome()

    try:
        # Open/Read CSV File
        df = pd.read_csv(csv_links)

        # Extract URLs from the DataFrame
        urls = df['URL'].tolist()

        # Initialize an empty list to store body data from all URLs
        all_body_data = []

        # Iterate through each URL
        for url in urls:
            print("Scraping Link: " + url)

            # Navigate to the webpage
            driver.get(url)
            time.sleep(5)  # Wait for the page to load (adjust time as needed)

            # Find elements containing body text
            visible_text_elements = driver.find_elements(By.CSS_SELECTOR, '.general-content.sm-margin-divider.side-divider')

            # Extract body text from each element
            for element in visible_text_elements:
                text = element.text
                if text:
                    all_body_data.append({'URL': url, 'Text': text})  # Associate text with URL

        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(all_body_data)

        # Save the DataFrame to a CSV file
        df.to_csv(csv_policies, index=False)
        print(f"Data has been scraped and saved to " + csv_policies)

    finally:
        # Close the WebDriver
        driver.quit()

# Call the function to scrape and save the links
scrape_fordham_links()