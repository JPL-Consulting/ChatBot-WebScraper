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

        scrape_fordham_sublinks()

    finally:
        # Close the WebDriver
        driver.quit()

# FUNCTION: Scrape Sub-Links Found on Main Policy Page
def scrape_fordham_sublinks():

    # Initialize the Selenium WebDriver (make sure you have the Chrome driver installed)
    driver = webdriver.Chrome()

    # Iterate through URLs (Row xx Column 0), Scrape each sub-link, Save to a single CSV file
    try:

        run_count = 0
        # Open/Read CSV File
        df = pd.read_csv(csv_links)

        # Iterate through each URL
        # Specify the column name you want to extract (e.g., 'Column2')
        target_column_name = 'URL'  # Adjust this to the desired column name

        # Access the specific column
        target_column_values = df[target_column_name]

        # Iterate through the values in the column
        for value in target_column_values:
            # TEST PURPOSES: Ensure proper URL is being read
            print("Scraping Link: " + value)

            # Set URL variable to sub-link found in main link
            url = value

            # Navigate to the webpage
            driver.get(url)
            time.sleep(5)  # Wait for the page to load (adjust time as needed)

            # Find all links on the page
            visible_text = driver.find_elements(By.CSS_SELECTOR, '.general-content.sm-margin-divider.side-divider')

            # Extract link URLs and text
            body_data = []
            other_link_data = []
            for body in visible_text:

                # ---------------SUB-SUB-LINKS
                # Find all links on the page
                other_links = driver.find_elements(By.TAG_NAME, 'a')

                # Extract link URLs and text
                for link in other_links:
                    href = link.get_attribute('href')
                    text = link.text
                    if href and text and (url in href):
                        other_link_data.append({'URL': href, 'Text': text})

                # END SUB-SUB-LINKS ------------------------------

                # Finding Body Text in Each Sub-link
                text = body.text
                if text:
                    body_data.append({'Text': text})

            # Convert the list of dictionaries to a DataFrame
            df = pd.DataFrame(body_data)

            # Save the DataFrame to a CSV file
            df.to_csv(csv_policies, index=False)
            print(f"Links have been scraped and saved to " + csv_policies + " from " + url)

            # Convert the list of dictionaries to a DataFrame
            df = pd.DataFrame(other_link_data)

            # Save the DataFrame to a CSV file
            df.to_csv(csv_links_in_policies, index=False)
            print(f"Links have been scraped and saved to " + csv_links_in_policies)

            run_count += 1

            if run_count==3:
                break
    finally:
        # Close the WebDriver
        driver.quit()


# Call the function to scrape and save the links
scrape_fordham_links()
