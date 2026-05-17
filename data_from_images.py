import json, os
import pandas as pd
from helper_functions.utility import (Groq_client, Groq_model, sys_msg, user_msg, MyError, data_file,
                                      VLM_response_0, VLM_response_1, setup_shared_logger, llm_output)
from pathlib import Path
from tqdm import tqdm

# Set up the shared logger
logger = setup_shared_logger()

if __name__ == "__main__":
    try:
        # retrieve the image files in the images folder
        image_files = [
            file for file in Path("images").rglob("*") if file.name.lower()[1:] in ["-0.png", "-1.png"]  #file.suffix.lower() in [".png", ".jpg", ".jpeg"]
        ]

        # initialise list to hold VLM responses
        extractions=[]

        # Loop through all the image files
        for image_path in tqdm(image_files):
            # Determine which user message and VLM response template to use
            if '-0' in image_path.name:
                input = user_msg[0]
                schema = VLM_response_0
            else:
                input = user_msg[1]
                schema = VLM_response_1

            # VLM response
            response = llm_output(client=Groq_client, model=Groq_model, sys_msg=sys_msg, input=input, image_path=image_path, schema=schema,delay_in_seconds=3)
            extractions.append(json.loads(response.choices[0].message.content))
        
        # seperate the even and odd entries into seperate dataframes
        df_evens = pd.DataFrame([d for i, d in enumerate(extractions) if i % 2 == 0])
        df_odds = pd.DataFrame([d for i, d in enumerate(extractions) if i % 2 != 0])
        
        # Read in the URL excel file
        df_URL = pd.read_excel(data_file, usecols=['URL'])

        # Create a dataframe out of the images list
        df_images = pd.DataFrame(list(zip(image_files[0::2], image_files[1::2])), columns=['Image_1', 'Image_2'])

        # Concatenate the dfs and output the final df to excel
        df = pd.concat([df_URL, df_odds, df_evens, df_images], axis=1)
        df.to_excel('Enhanced_Listings.xlsx', index=False)
    
        logger.info(f"{os.path.basename(__file__)} successfully run.")
    
    except MyError as e:
        logger.error(f"{e}")
    except (Exception, BaseException) as e:
        logger.error(f"General error while executing {os.path.basename(__file__)} : {e}")
