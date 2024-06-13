from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

def scrape_fordham_policies():
    # Initialize the Selenium WebDriver (make sure you have the Chrome driver installed)
    driver = webdriver.Chrome()

    try:
        # Navigate to the webpage
        driver.get('https://www.fordham.edu/information-technology/it-security--assurance/it-policies-procedures-and-guidelines/')
        time.sleep(5)  # Wait for the page to load (adjust time as needed)

        # Scrape the data
        data = []

        # Locate the section containing the policies
        policies_section = driver.find_element(By.XPATH, '//div[@id="main-content"]')

        # Find all policy items within the section
        policies = policies_section.find_elements(By.XPATH, './/h3')

        for policy in policies:
            title = policy.text
            description = policy.find_element(By.XPATH, 'following::p').text  # Updated XPath here
            data.append({'Title': title, 'Description': description})

        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(data)

        # Save the DataFrame to a CSV file
        df.to_csv('fordham_it_policies.csv', index=False)
        print("Data has been scraped and saved to fordham_it_policies.csv")

    finally:
        # Close the WebDriver
        driver.quit()

# Call the function to scrape and save the data
scrape_fordham_policies()
