# import relevant libraries
import pandas as pd, pyautogui, time, random, webbrowser
from utility import check_chrome_path

# Set the Chrome path if Chrome is installed in device
chrome_path = check_chrome_path()
if chrome_path:
    chrome_path = chrome_path + " %s"     # the %s is a placeholder for the url to be opened.

print(chrome_path)

urls = [
    "https://www.ccs.gov.sg",
    "https://shopee.sg/2L-High-Speed-Blender-Heavy-Duty-Ice-Crushing-Juicer-Smoothie-Maker-Food-Processor-Multifunction-Pengisar-Mixer-i.1714340390.54208947162?extraParams=%7B%22display_model_id%22%3A405792851667%2C%22model_selection_logic%22%3A3%7D",
    "https://shopee.sg/Fully-Automatic-Soy-Milk-Maker-Portable-Juicer-Blender-Machine-Smart-Soya-Bean-Milk-Machine-i.299068664.50058759450?extraParams=%7B%22display_model_id%22%3A420778894384%2C%22model_selection_logic%22%3A3%7D"
]

# Iterate through the list and open each in a new tab
for index, url in enumerate(urls):
    if index == 0:
        # Opens the first URL in a new browser window
        webbrowser.open_new(url)
    else:
        # Opens subsequent URLs in new tabs within the same browser window
        webbrowser.open_new_tab(url)
    
    # Optional: Short pause to let the browser process each request
    time.sleep(random.uniform(0.3,0.5))