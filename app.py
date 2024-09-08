import streamlit as st

from pdf_to_image import pdf_to_image
from image_to_text import image_to_text
from mirascope_extractor import extractor

import google.generativeai as genai
import pandas as pd

import glob
import os
from dotenv import load_dotenv
import streamlit as st
from resume_recommender import recommend_resume
from db import save_cv_into_db, get_cv_from_db
import db
from typing import List, Tuple
import warnings
warnings.filterwarnings('ignore')


load_dotenv()

global empty_df
openai_api_key = os.getenv('OPENAI_API_KEY')
genai.configure(api_key=openai_api_key)


st.set_page_config(page_title="CV Recommendor Gen AI")
st.title("Gen AI CV Recommender")
st.write("""
**Find the Best Candidates for Your Job!**

🔍 **What It Does:**
- Analyzes multiple resumes in PDF format.
- Matches them with your job description.

📋 **How It Works:**
1. Upload resumes 📄
2. Upload the job description 📝
3. Get a table of top recommended candidates 🏆

Ready to find the perfect fit? Let's get started!
""")

uploaded_files = st.sidebar.file_uploader("Choose PDF files", accept_multiple_files=True, type="pdf")
job_description = st.sidebar.text_input('Enter Job Description')

if uploaded_files and job_description:
    if st.sidebar.button('AI Recommendation'):

        try:
            image_bytes = pdf_to_image(uploaded_files)
        except Exception as e:
            print('An Error in pdf_to_image: ', e, '\n\n')

        try:
            all_texts = []
            for image_byte in image_bytes:
                print('This is image_byte: ', image_byte, '\n\n')
                
                combine_text = ''
                for image in image_byte:
                    text = image_to_text(image)
                    combine_text += text
                all_texts.append(combine_text)  
        except Exception as e:
            print('An error occur in image_to_text: ', e, '\n\n')

                
        empty_df = pd.DataFrame()

        try:
            for text in all_texts:
                extracted_text = extractor(text)
                task_details_dict = extracted_text.dict()
                df = pd.DataFrame([task_details_dict])
                empty_df = pd.concat([empty_df, df])
            
        except Exception as e:
            print('An error occured in mirascope extraction: ', e, '\n\n')
            raise

        # print('This is single list empty_df: ',empty_df.values.flatten().tolist())
        cv_list = empty_df.values.tolist()
        print('This is cv_list: ', cv_list, '\n\n')
        
        try:
            for single_cv in cv_list:
                save_cv_into_db(single_cv)
        except Exception as e:
            print('Failed to save CV into DB: ', e)

        
        all_cvs: List[Tuple] = get_cv_from_db()
        cv_df = pd.DataFrame(all_cvs, columns=[
            'name', 'email', 'phone_number', 'skills', 'education', 'past_company_experience', 'about_section'
        ])
        try:
            recommend_df = recommend_resume(cv_df, job_description)
        except Exception as e:
            print('An error occur in cv recommendation: ', e, '\n\n')
            
        if 'Unnamed: 0' in recommend_df.columns:
            recommend_df = recommend_df.drop('Unnamed: 0', axis=1)

        print('Recommendation process done successfully')
            
        st.write(recommend_df)


        # csv = empty_df.to_csv(index=False)
        # st.download_button(
        #     label = 'Click to Download CSV',
        #     data = csv,
        #     file_name = 'Extracted_data.csv',
        #     mime='text/csv',
        # )
        
