from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# Set up Selenium and the Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run headless if you don't want to open the browser window
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# Define the URL for the Porirua recycling calendar
url = "https://poriruacity.govt.nz/services/recycling-and-rubbish/recycling-calendar/"  # Update with the correct URL

try:
    # Navigate to the recycling calendar page
    driver.get(url)
    
    # Wait for the page to load
    time.sleep(5)  # Adjust this as necessary for the page to fully load

    # Get the page source and parse it with Beautiful Soup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Find the recycling calendar table (adjust the selector based on the website's structure)
    calendar_table = soup.find('table')  # This is an example; update as needed
    rows = calendar_table.find_all('tr')  # Get all table rows

    # Extract and print relevant information from the table
    for row in rows:
        cells = row.find_all('td')  # Get all cells in the row
        if cells:
            # Extract information (e.g., date and type of waste)
            date = cells[0].text.strip()  # Assuming the first cell is the date
            waste_type = cells[1].text.strip()  # Assuming the second cell is the waste type
            print(f"Date: {date}, Waste Type: {waste_type}")

finally:
    # Close the browser
    driver.quit()
