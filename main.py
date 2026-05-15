# import relevant libraries
import os, pyautogui, time, random, subprocess, webbrowser
import pandas as pd
from pathlib import Path
from PIL import Image    # pip install pillow
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

        # Iterate through the list and open each in a new tab
        for index, url in enumerate(urls):
            open_with_zoom(url)
            time.sleep(random.uniform(1,2))
            scroll_screenshot(index=index)
            time.sleep(random.uniform(1,2))
            # close the current tab
            pyautogui.hotkey('ctrl','w')
        
        logger.info(f"{os.path.basename(__file__)} successfully run.")
    
    except MyError as e:
        logger.error(f"{e}")
    except (Exception, BaseException) as e:
        logger.error(f"General error while executing {os.path.basename(__file__)} : {e}")