# import relevant libraries
import ctypes, os, pyautogui, time, random, subprocess, webbrowser
import pandas as pd
from pathlib import Path
from PIL import Image    # pip install pillow
from tqdm import tqdm
from helper_functions.utility import data_file, MyError, open_with_zoom, scroll_screenshot, setup_shared_logger

## First, open a new default browser window and visit the shopee main site. Ensure that you are logged in, if not,  log in then leave the tab open.
## For each tab that is opened, zoom to 75%, then take screenshots, then close that tab before opening new one

# Set up the shared logger
logger = setup_shared_logger()

# Create folder used to store extracted images, if it does't exist
Path('images').mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    try:
        # 1) Check that the excel file containing the urls of reported listings exists
        file_path = Path(data_file)
        if not file_path.is_file():
            raise MyError("Listings excel file does not exist, please check!")

        # 2) Read in the urls from excel file
        url_df = pd.read_excel(data_file, usecols=['URL'])
        urls =  url_df['URL'].values.tolist()

        # 3) Iterate through the list of URLs
        for index, url in enumerate(tqdm(urls)):
            # for each URL, open in a new tab, and zoom out to 75%
            open_with_zoom(url)
            # stop for a while to mimic normal human interactions
            time.sleep(random.uniform(1,2))
            # scroll and take screenshots
            scroll_screenshot(index=index, num_scrolls=3)
            # stop for a while before closing tab
            time.sleep(random.uniform(1,2))
            # close the current tab
            pyautogui.hotkey('ctrl','w')
        
        logger.info(f"{os.path.basename(__file__)} successfully run.")

        # 4) Once job done, inform user via a pop-up window and a sound
            # first 0 means to create a completely independent window, 
            # Options: 0 = OK button only, 1 = OK/Cancel, etc. 0x40 adds an Information Icon and plays the "System Asterisk" chime. 0x0 adds a standard OK button
            # timeout in 60000 miliseconds
        ctypes.windll.user32.MessageBoxTimeoutW(0, "All URLs opened and screenshot", "Task completed", 
                                                0x40 | 0x0, 0, 60000)

    
    except MyError as e:
        logger.error(f"{e}")
    except (Exception, BaseException) as e:
        logger.error(f"General error while executing {os.path.basename(__file__)} : {e}")