from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

def scrape_fordham_links():
    # Initialize the Selenium WebDriver (make sure you have the Chrome driver installed)
    driver = webdriver.Chrome()

    try:
        # Navigate to the webpage
        url = 'https://www.fordham.edu/information-technology/it-security--assurance/it-policies-procedures-and-guidelines/'
        driver.get(url)

        # Find all links on the page
        links = driver.find_elements(By.TAG_NAME, 'a')

        # Extract link URLs and text
        link_data = []
        for link in links:
            href = link.get_attribute('href')
            text = link.text
            if href and text:
                link_data.append({'URL': href, 'Text': text})

        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(link_data)

        # Save the DataFrame to a CSV file
        df.to_csv('fordham_links.csv', index=False)
        print(f"Links have been scraped and saved to fordham_links.csv from {url}")

    finally:
        # Close the WebDriver
        driver.quit()

# Call the function to scrape and save the links
scrape_fordham_links()


