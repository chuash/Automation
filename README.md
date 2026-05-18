**Note:** The `requirements.txt` file in this repository was generated for a Python 3.13 environment.

#### Problem Statement
Imagine if you have a list of ecommerce platform product listing URLs that you need to access, extract relevant information from and also take screenshots. One obvious approach would be to make use of web browser automation tools e.g Selenium or Playwright to open a browser, navigate to the respective URL, access the underlying relevant web elements and scrape the corresponding data, finally take screenshots with scrolls.

This sounds easy enough but what if the ecommerce platform has very robust anti-botting defence mechanisms? One option is to level up the game and work on overcoming the platform's anti-botting defences, however, this is going to be an endless cat-and-mouse game of trying to outdo each other. If there is available API service provided by the platform, that can be considered but API services usually comes with a subscription fee. 

#### Proof of Concept
This project aims to test out a scraping-independent and potentially freemium approach to extracting information and screenshots from a given list of ecommerce platform product listing URLs.<br>
***Approach Overview***:<br>
The key idea is to make use of the computing device (e.g. laptop)'s native web browser to access the ecommerce site's landing page and ensure that the web browser is logged into the ecommerce site at the first instance.<br>
Once this step is done, keep the web browser window open. Then, for each of the product listing URLs, use python library `webbrowser` to first open the URL in a seperate browser tab within the same browser window that has been kept open. After which, use python library `pyautogui` to simulate human interaction with the webpage and take screenshots.<br>
Once the necessary screenshots have been captured, crop and adjust the images before sending them, together with the corresponding prompts, to a suitable Vision Language Model to extract the required information. For this project, `meta-llama/llama-4-scout-17b-16e-instruct` hosted on `Groq` is used because it is free to use (within certain threshold usage limits)

#### Further work
Finetune and apply this approach to be able to work on various specified ecommerce platforms. 