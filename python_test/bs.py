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
        df = pd.read_excel(excel_file, header=None, skiprows=2)

        # Check if there is at least one row in the file
        if not df.empty:
            for number in df.iloc[:, 0]:
                if number < 10000:
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
driver.get("https://broadbandnow.com/Massachusetts/Agawam?zip=01001")

# Wait for the page to load
wait = WebDriverWait(driver,30)

# Loop through the zip codes
for zip in zips:
    # Find the search input field for zip code and clear any existing text
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "address-check-redesign"))) 
    search_box.clear()

    # Enter the zip code and submit the form
    search_box.send_keys(zip)
    search_box.send_keys(Keys.RETURN)

    # Wait for the page to load the results (adjust the sleep time if necessary)
    wait = WebDriverWait(driver, 15)

    try:
        # Locate the Xfinity availability percentage (you need to inspect the correct element)
        xfinity_element = driver.find_element(By.XPATH, "//span[@class='f-provider-card__connection-label']")
        availability = xfinity_element.text.strip()
        
        # Store the result
        xfinity_availability.append({'zip_code': zip, 'xfinity_availability': availability})
    except Exception as e:
        # If there's an issue, store a placeholder value
        xfinity_availability.append({'zip_code': zip_code, 'xfinity_availability': 'N/A'})

# Close the browser
driver.quit()

# Create a pandas DataFrame from the results
df = pd.DataFrame(xfinity_availability)

# Save the results to a CSV file
df.to_csv('xfinity_availability.csv', index=False)

# Print its length
#print("Data in zips:", zips)
#print("Length of zips list:", len(zips))
