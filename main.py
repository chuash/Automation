# import relevant libraries
import pandas as pd, pyautogui, time, random, subprocess, webbrowser
from utility import open_with_zoom

## First, open a new default browser window and visit the shopee main site. Ensure that you are logged in, if not log in, then leave the tab open.

# 1) Read in the urls from excel in folder
# Check if folder exists, if not raise error
# Check if got file of certain filename, if not raise error
# if got file, check if 

urls = [
    "https://shopee.sg/2L-High-Speed-Blender-Heavy-Duty-Ice-Crushing-Juicer-Smoothie-Maker-Food-Processor-Multifunction-Pengisar-Mixer-i.1714340390.54208947162?extraParams=%7B%22display_model_id%22%3A405792851667%2C%22model_selection_logic%22%3A3%7D",
    "https://shopee.sg/Fully-Automatic-Soy-Milk-Maker-Portable-Juicer-Blender-Machine-Smart-Soya-Bean-Milk-Machine-i.299068664.50058759450?extraParams=%7B%22display_model_id%22%3A420778894384%2C%22model_selection_logic%22%3A3%7D"
]

# Iterate through the list and open each in a new tab
for url in urls:
    open_with_zoom(url)
    # Optional: Short pause to let the browser process each request
    time.sleep(random.uniform(0.5,1))