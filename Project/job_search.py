# Main loop to go over all jobs
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from functions import scroll

jobs_applied_to = []

# Set up your web driver (make sure you have the correct path to your driver)
driver_path = r"C:\Users\omarb\Desktop\chromedriver-win64\chromedriver.exe"
service = Service(executable_path = 'chromedriver.exe')
driver = webdriver.Chrome(service = service)
# Maximize the window
driver.maximize_window()

# Replace these with your LinkedIn credentials
USERNAME = "********************"
PASSWORD = "******************"

# Set up 10s waits 
wait = WebDriverWait(driver,5)
# Set up 1s waits 
wait2 = WebDriverWait(driver,3)
# Set up 10s wait
#wait3 = WebDriverWait(driver,45)

# Go to LinkedIn Jobs page
driver.get("https://www.linkedin.com/checkpoint/rm/sign-in-another-account")

time.sleep(3)

# Find the input field for USERNAME and clear any existing text
username_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='form__input--floating margin-top-24']//input[@id='username']"))) 
username_box.clear()
username_box.send_keys(USERNAME)

# Find the input field for PASSWORD and clear any existing text
password_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='form__input--floating margin-top-24']//input[@id='password']"))) 
password_box.clear()
password_box.send_keys(PASSWORD)

# Submit login form
password_box.send_keys(Keys.RETURN)

time.sleep(3)

# Go to job page
job_page = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'ivm-view-attr__img-wrapper')]//li-icon[contains(@type, 'job')]")))
job_page.click()

time.sleep(3)

# Search job title in linkedin jobs page
search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='application-outlet']//div[@class='global-nav__content']//div[@class='relative']//input[contains(@id, 'jobs-search-box-keyword-id-ember')]")))
search_box.clear()
search_box.send_keys('Software engineer')
search_box.send_keys(Keys.RETURN)

time.sleep(3)

# Initialize variables
x = 1  
y = 1
i = 1
wait = WebDriverWait(driver, 5)

for y in range(8):

    # Try block to scroll in every page on linkedin
    try:
        # Scroll to load hidden elements
        scrollable_div = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'qwiaGHkwlrieAZoYusFyjMXGbewtMHNtc')]")))
        scroll(scrollable_div)
        print("Scroll complete")
    except Exception as e:
        print("Error scrolling")
        break

    time.sleep(1)

    # Try block for finding Page cards in every page
    try:
        # Find all pagination elements on the current page
        page_cards = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'qwiaGHkwlrieAZoYusFyjMXGbewtMHNtc')]//li[contains(@class, 'artdeco-pagination__indicator')]")))
    except Exception as e:
        print("Error finding pagination elements")
        break

    time.sleep(1)

    # Try block to find all job elements in every page
    try:
        # Find all job elements
        job_cards = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//ul[@class='FRRHBcSAMYNTqdBkJBCtURynxFrHdvwBLeA']//li[contains(@id, 'ember')]//a[contains(@tabindex, '0')]")))
    except Exception as e:
        print("Error getting job cards")
        break

    time.sleep(1)

    # For loop to go over every job in the page
    for i in range(25):   

        # Try block to click every Job in Job cards
        try:
            job = job_cards[i]  # Use zero-based index
            first_text = job.text.split('\n')[0]
            second_text = first_text.strip()
            job.click()

            # Try block for click apply for external link 
            # (not EasyApply) Try block for button says "Apply" and routes to an external link
            try:
                # Handle apply button in linkedin
                original_window = driver.current_window_handle
                apply_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='mt4']//button[@role='link']")))
                apply_link.click()

                # Switch to the new window
                wait.until(lambda d: len(d.window_handles) > 1)
                new_window = [window for window in driver.window_handles if window != original_window][0]
                driver.switch_to.window(new_window)

                # Spend time in new window
                time.sleep(10)

                # Try block to search and click apply button on external link if one is shown BEFORE scrolling 
                try:
                    # Apply buttons on external link
                    apply_button = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//button[contains(text(), 'Apply')] | //a[contains(text(), 'Apply')]")))

                    if (len(apply_button)) > 1:
                        apply_button[0].click()
                    else:
                        apply_button[0].click()


                    time.sleep(5)

                    


                    # Once apply button on external site is found and clicked, run try block below

                    # Try to start application



                    # Except if routed to a page that is not the applicaiton page (login page)



                # Except block to Scroll and then look for apply button if apply button not found without scrolling (apply AFTER scrolling)
                except Exception as e:
                    # Try block to scroll once external link is open apply button is not located already
                    try:
                        # Scroll down to the bottom
                        last_height = driver.execute_script("return document.body.scrollHeight")
                        while True:
                            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                            time.sleep(3)
                            new_height = driver.execute_script("return document.body.scrollHeight")
                            if new_height == last_height:  # Check if we've reached the bottom
                                break
                            last_height = new_height
                        
                        # Pause before scrolling up
                        time.sleep(3)
                        
                        # Scroll up to the top
                        driver.execute_script("window.scrollTo(0, 0);")

                        time.sleep(3)
                    except Exception as e:
                        print("Error scrolling on external link")
                        break

                    # Try block to search and click apply button on external link if one is shown AFTER scrolling 
                    try:
                        # Apply buttons on external link
                        apply_button = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//button[contains(text(), 'Apply')] | //a[contains(text(), 'Apply')]")))

                        if (len(apply_button)) > 1:
                            apply_button[0].click()
                        else:
                            apply_button[0].click()


                        time.sleep(5)
                    except Exception as e:
                        print("Error finding apply button after scrolling")
                

                


                time.sleep(5)

                    


                # Try block to search and click the job title on external link

                '''

                try:
                    # Click apply button on external link
                    job_title = wait.until(EC.presence_of_all_elements_located((By.XPATH, f"//button[contains(text(), '{second_text}')] | //a[contains(text(), '{second_text}')]")))
                    job_title_button = job_title[0]

                    if (len(job_title)) > 1:
                        job_title_button.click()
                    else:
                        job_title_button.click()

                    time.sleep(5)

                except Exception as e:
                    print("Error finding apply button, Error finding job link")

                        
                '''                


                time.sleep(5)


                # Try block if prompted for a login






                # Try block to start application on current page







                driver.close()
                driver.switch_to.window(original_window)

                # 3 sec before next job
                time.sleep(3)





            # (Easy Apply) Try block for Easy Apply




                
            except Exception as e:
                print("Error clicking job (EasyApply)")

        except Exception as e:
            print("Error clicking job")
            break

    next_page = page_cards[x]
    next_page.click()
    time.sleep(2)
    x += 1

    time.sleep(3)

driver.quit()
print("Applied to all jobs successfully")
print("Driver quit successfully.")      
