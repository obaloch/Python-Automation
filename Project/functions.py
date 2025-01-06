# Scroll
from selenium.webdriver.common.keys import Keys
import time

def scroll(scrollable_div):
    """
    Function to scroll down and up in a scrollable div to load hidden elements.

    Args:
        scrollable_div (WebElement): The scrollable element to perform the scrolling.
    """
    try:
        # Scroll down 10 times
        for _ in range(10):
            scrollable_div.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.2)  # Short delay to allow loading

        # Scroll up 10 times
        for _ in range(10):
            scrollable_div.send_keys(Keys.PAGE_UP)
            time.sleep(0.2)  # Short delay to allow loading

    except Exception as e:
        print(f"Error during scrolling: {e}")

def scrollDown(scrollable_div):
    """
    Function to scroll down in a scrollable div to load hidden elements.

    Args:
        scrollable_div (WebElement): The scrollable element to perform the scrolling.
    """
    try:
        # Scroll down 10 times
        for _ in range(10):
            scrollable_div.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.2)  # Short delay to allow loading

    except Exception as e:
        print(f"Error during scrolling: {e}")

def scrollUp(scrollable_div):
    """
    Function to scroll up in a scrollable div to load hidden elements.

    Args:
        scrollable_div (WebElement): The scrollable element to perform the scrolling.
    """
    try:
        # Scroll up 10 times
        for _ in range(10):
            scrollable_div.send_keys(Keys.PAGE_UP)
            time.sleep(0.2)  # Short delay to allow loading

    except Exception as e:
        print(f"Error during scrolling: {e}")