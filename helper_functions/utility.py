import base64, logging, openai, os, pyautogui, random, time, webbrowser
from dotenv import load_dotenv
from groq import Groq
from openai import OpenAI
from openai.types.chat import ChatCompletion
from pydantic import BaseModel, Field
from typing import Optional, List

# Load environment variables
if not load_dotenv(".env"):
    pass

# Define variables
Groq_model = os.getenv("GROQ_MODEL_NAME")
Groq_client = OpenAI(api_key=os.getenv("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1")
data_file = os.getenv("DATA_FILE")
sys_msg = "You are an expert in extracting text from images"
user_msg = ["extract 1) title of product (found at top right hand corner immediately above the ratings), 2) the shop name selling the product (found immediately above the 'Chat Now' button).",
            "extract 1) whether there is safety mark number (found to the right of the text 'Safety Mark', if no number is detected, return empty string) and 2) where the product ships from (found to the right of the text 'Ships From')."]


# Set up custom exception class
class MyError(Exception):
    def __init__(self, value):
        self.value = value

    # Defining __str__ so that print() returns this
    def __str__(self):
        return self.value


# Set up structured LLM output schema
class VLM_response_0(BaseModel):
    """Pydantic response class to ensure that VLM always responds in the same format."""
    Product_Title: str = Field(..., description="Title of product, per extracted from product listing image")
    Seller_Name: str = Field(..., description="Name of shop selling product, per extracted from product listing image")


class VLM_response_1(BaseModel):
    """Pydantic response class to ensure that VLM always responds in the same format."""
    Safety_Mark: Optional[str] = Field(..., description="The Safety Mark number, per extracted from product listing image. If no Safety Mark number, return empty string")
    Ships_From: str = Field(..., description="Place where product ships from, per extracted from product listing image")
    

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
        # Introduce random delays between zooms, to simulate human actions
        time.sleep(random.uniform(0.2,0.5))


def scroll_screenshot(index, scroll_amount = 800, num_scrolls = 2):
     
     # Click to focus window
     pyautogui.click(x=50, y=500)
     # Scroll to the top
     time.sleep(1)
     pyautogui.scroll(1000)
    
     for i in range(num_scrolls):
        time.sleep(2)
        # Take screenshot of current viewport
        im = pyautogui.screenshot(os.path.join('images', f"{index}-{i}.png"))
        if i == num_scrolls-1:
            pass
        else:
            pyautogui.scroll(-scroll_amount)


# Function to encode the image
def encode_image(image_path):
  # Opens the image file located at image_path in read-binary mode
  with open(image_path, "rb") as image_file:
    # converts the binary image bytes into Base64-encoded bytes. Base64 is a text-safe representation of binary data. 
    # Need to convert to python string before further processing as most python processes work with str, not bytes
    return base64.b64encode(image_file.read()).decode('utf-8')


# Set up synchronous LLM API response
def llm_output(client:Groq, model:str, sys_msg:str, input:str, image_path:str, schema:BaseModel|None = None,
                temperature:int=0, delay_in_seconds:float=0.0)-> BaseModel|ChatCompletion:
    """ Takes in both text and image inputs while producing text outputs"""
    try:         
        # Introduce time delay, if necessary, so as to keep within rate limit of VLM API request.
        if delay_in_seconds > 0:
             time.sleep(delay_in_seconds)
        
        # Encode the image bytes into Base64 representation 
        base64_image = encode_image(image_path)

        # The case when LLM response is expected to follow a particular schema
        if schema is not None:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                    "role": "system",
                    "content": sys_msg
                    },
                    
                    {
                    "role": "user",
                    "content": [
                            {
                                "type": "text", 
                                "text": f"Given the following product listing image, {input}"
                            },
                            {
                                "type": "image_url",
                                "detail": "auto",
                                "image_url": {"url": f"data:image/png;base64,{base64_image}"}
                            },
                        ]
                    }
                ],
                temperature=temperature,
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                            "name": "VLM_response",
                            "schema": schema.model_json_schema()
                    } 
                }  
                )
        else:
             # The case when LLM response is just normal string
             response = client.responses.parse(
                model=model,
                input=[
                    {
                    "role": "system",
                    "content": sys_msg
                    },
                    {
                    "role": "user",
                    "content": [
                            {
                                "type": "text", 
                                "text": f"Given the following product listing image, {input}"
                            },
                            {
                                "type": "image_url",
                                "detail": "auto",
                                "image_url": {"url": f"data:image/png;base64,{base64_image}"}
                            },
                        ]
                    }
                ],
                temperature=temperature
                )
        return response
    
    except openai.APIError as e:
            raise MyError(f"llm_output function API error: {e}")
    except (Exception, BaseException) as e:
            raise MyError(f"llm_output function error: {e}")
