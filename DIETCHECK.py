#!/usr/bin/env python
# coding: utf-8

# In[1]:


GOOGLE_API_KEY="AIzaSyAK42G8RlWgw1Ahb02H2M2rLJlfQA-8oMQ"


# In[3]:


from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# In[4]:


def get_gemini_repsonse(input,image,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,image[0],prompt])
    return response.text


# In[5]:


def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


# In[6]:


st.set_page_config(page_title="Gemini Health App")

st.header("Gemini Health App")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Tell me the total calories")


# In[7]:


input_prompt = """
As a nutrition expert, you need to analyze food items from an image. Please provide the following information for each food item:

1. Description of the food:
2. Number of calories in the food:
3. Percentage split of macronutrients (carbohydrates, fats, proteins):
   - Carbohydrates percentage:
   - Fats percentage:
   - Proteins percentage:

Please enter the details in the following format:

1. [Food Item 1]
   - Description: [Brief description of the food]
   - Calories: [Enter the number of calories]
   - Carbohydrates Percentage: [Enter the percentage]
   - Fats Percentage: [Enter the percentage]
   - Proteins Percentage: [Enter the percentage]

2. [Food Item 2]
   - Description: [Brief description of the food]
   - Calories: [Enter the number of calories]
   - Carbohydrates Percentage: [Enter the percentage]
   - Fats Percentage: [Enter the percentage]
   - Proteins Percentage: [Enter the percentage]

...

Please provide the details for each food item. Once done, you can describe how healthy the overall meal is based on the nutritional information.
"""


# In[8]:


if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_repsonse(input_prompt,image_data,input)
    st.subheader("The Response is")
    st.write(response)

