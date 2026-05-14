# import relevant libraries
import os, pandas as pd, pyautogui, time, random, subprocess, webbrowser
from pathlib import Path
from helper_functions.utility import data_file, MyError, open_with_zoom, setup_shared_logger

## First, open a new default browser window and visit the shopee main site. Ensure that you are logged in, if not,  log in then leave the tab open.
## For each tab that is opened, zoom to 75%, then take screenshots, then close that tab before opening new one

# Set up the shared logger
logger = setup_shared_logger()

if __name__ == "__main__":
    try:
        # 1) Check that the excel file containing the urls of listing exists
        file_path = Path(data_file)
        if not file_path.is_file():
            raise MyError("Listings excel file does not exist, please check!")

        # 2) Read in the urls from excel file
        url = pd.read_excel(data_file, usecols=['URL'])   #need openpyxl
        print(type(url))
 

        urls = [
            "https://shopee.sg/2L-High-Speed-Blender-Heavy-Duty-Ice-Crushing-Juicer-Smoothie-Maker-Food-Processor-Multifunction-Pengisar-Mixer-i.1714340390.54208947162?extraParams=%7B%22display_model_id%22%3A405792851667%2C%22model_selection_logic%22%3A3%7D",
            "https://shopee.sg/Fully-Automatic-Soy-Milk-Maker-Portable-Juicer-Blender-Machine-Smart-Soya-Bean-Milk-Machine-i.299068664.50058759450?extraParams=%7B%22display_model_id%22%3A420778894384%2C%22model_selection_logic%22%3A3%7D"
        ]

        # Iterate through the list and open each in a new tab
        #for url in urls:
        #    open_with_zoom(url)
            # Optional: Short pause to let the browser process each request
        #    time.sleep(random.uniform(0.5,1))
    
    except MyError as e:
        logger.error(f"{e}")
    except (Exception, BaseException) as e:
        logger.error(f"General error while executing {os.path.basename(__file__)} : {e}")