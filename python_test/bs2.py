import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the empty list called zips
zips = []

# Function to read the Excel file and store data from row A into the zips list
def read_excel_and_store_in_zips(excel_file):
    global zips  # Access the global zips list
    
    try:
        # Read the Excel file without assuming a header (header=None)
        df = pd.read_excel(excel_file, header=None, skiprows=5000)

        # Check if there is at least one row in the file
        if not df.empty:
            for number in df.iloc[:, 0]:
                if number < 1000:
                    modified_number = '00' + str(number)  # Add '0' to the beginning of the number
                    zips.append(modified_number)  # Add the modified number to the list
                elif number < 10000:
                    modified_number = '0' + str(number)  # Add '0' to the beginning of the number
                    zips.append(modified_number)  # Add the modified number to the list
                else:
                    zips.append(number)  # Add the modified number to the list
        else:
            print("The Excel file is empty.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Path to your Excel file (Make sure the file extension is correct)
excel_file = r'C:\Users\omarb\Desktop\python_test\file.xlsx'  # Use raw string for file path

# Call the function to read the Excel file and store row A data into zips
read_excel_and_store_in_zips(excel_file)

# List to store results
xfinity_availability = []

# Set up your web driver (make sure you have the correct path to your driver)
driver_path = r"C:\Users\omarb\Desktop\chromedriver-win64\chromedriver.exe"
service = Service(executable_path = 'chromedriver.exe')
driver = webdriver.Chrome(service = service)

# Open the BroadbandNow website
driver.get("https://broadbandnow.com")

# Wait for the page to load
wait = WebDriverWait(driver,10)
wait2 = WebDriverWait(driver,1)

for zip in zips:
    # Get only 
    #if int(zip) > 34140:
    #    break

    # Find the search input field for zip code and clear any existing text
    search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='form-wrapper zip-search__form-wrapper js-zip-search-form-wrapper']//input[@name='zip']"))) 
    search_box.clear()

    # Enter the zip code and submit the form
    search_box.send_keys(zip)
    search_box.send_keys(Keys.RETURN)

    try:
        # Locate the Xfinity availability percentage (make sure this XPath is correct for your page)
        xfinity_element = wait2.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@data-provider='Xfinity']//div[@class='f-provider-card__availability']//span[@class='f-provider-card__connection-value']")))

        # Locate the city element (make sure this XPath is correct for your page)
        #city_element = wait2.until(EC.presence_of_all_elements_located((By.XPATH, "//h1[@class='city-zip-providers__zip-header-title']//span")))

        # Iterate over Xfinity and city elements together
        for element in xfinity_element:
            # Extract the text from each element and strip any surrounding whitespace
            availability = element.text.strip()
            # Store the result
            xfinity_availability.append({'zip_code': zip, 'xfinity_availability': availability})

        # Click the homepage link
        homepage_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='header__brand-menu-container']//a[@class='header__brand']")))
        homepage_link.click()

    except Exception as e:
        
        xfinity_availability.append({'zip_code': zip, 'xfinity_availability': 'N/A'})

        # Click the homepage link in case of error
        homepage_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='header__brand-menu-container']//a[@class='header__brand']")))
        homepage_link.click()


# Close the browser
driver.quit()

# Create a pandas DataFrame from the results
df = pd.DataFrame(xfinity_availability)

# Save the results to a CSV file
df.to_csv('fivethousand-to-end.csv', index=False)