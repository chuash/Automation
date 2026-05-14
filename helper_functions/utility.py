import logging, os, pyautogui, random, time, webbrowser
from dotenv import load_dotenv
from groq import Groq
from typing import Optional

# Load environment variables
if not load_dotenv(".env"):
    pass

# Define variables
Groq_model = os.getenv("GROQ_MODEL_NAME")
Groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
data_file = os.getenv("DATA_FILE")


# Set up custom exception class
class MyError(Exception):
    def __init__(self, value):
        self.value = value

    # Defining __str__ so that print() returns this
    def __str__(self):
        return self.value
    

# Set up shared logger instance for the entire application.
def setup_shared_logger(log_file_name="application.log"):

    # Create the logger with name "shared_app_logger" if it doesn's exist
    logger = logging.getLogger('shared_app_logger')
    # Set the desired logging level
    logger.setLevel(logging.INFO)

    # Prevent adding multiple handlers if setup_shared_logger is called multiple times
    if not logger.handlers:
        # Create a file handler
        file_handler = logging.FileHandler(log_file_name, mode='a')
        file_handler.setLevel(logging.INFO)

        # Create a formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Add the file handler to the logger
        logger.addHandler(file_handler)

    return logger


# Check for the presence of Chrome browser
def check_chrome_path()->Optional[str]:
    # Common paths for Chrome on Windows
    paths = [
        "C:/Program Files/Google/Chrome/Application/chrome.exe",
        "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
        os.path.expanduser("~") + "/AppData/Local/Google/Chrome/Application/chrome.exe"
    ]
    
    for path in paths:
        if os.path.exists(path):
            return path + " %s"     # the %s is a placeholder for the url to be opened.

    return None


def open_with_zoom(url):
    # 1. Open the new tab using the built-in webbrowser module
    webbrowser.open_new_tab(url)
    # 2. Wait for the browser to load and gain focus
    time.sleep(2) 
    # 3. Reset the zoom to 100%
    pyautogui.hotkey('ctrl', '0')
    # 4 Simulate zoom reduction. Standard browsers use Ctrl + '-' to decrease zoom by ~10% increments.
    # To reach 75%, we typically need 3 steps (100 -> 90 -> 80 -> 75/70).
    press_count = 3  # Adjust based on specific browser increments
    for _ in range(press_count):
        pyautogui.hotkey('ctrl', '-')
        time.sleep(random.uniform(0.2,0.5))