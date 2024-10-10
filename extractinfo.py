from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup Selenium WebDriver with Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Go to the recycling calendar page
driver.get("https://poriruacity.govt.nz/services/rubbish-and-recycling/recycling-calendar/")

# Let the page load
time.sleep(2)  # Adjust sleep if necessary

# Locate the address input field and submit button
address_input = driver.find_element(By.NAME, 'address')  # Replace with correct name or id
submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')  # Replace with correct XPATH

# Input the address (replace with the desired address)
address_input.send_keys("Add Address")  # Replace with actual address
submit_button.click()

# Wait for the result to load
time.sleep(3)  # Adjust time based on page response time

# Scrape the resulting data (example: grab the schedule information)
# Adjust this XPATH to match the data element
results = driver.find_element(By.XPATH, '//*[@id="collection-results"]')  # Replace with actual XPATH of the results

# Print or process the result
print(results.text)

# Close the browser
driver.quit()
