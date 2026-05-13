import os, pyautogui, random, time, webbrowser
from typing import Optional

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