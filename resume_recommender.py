from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertTokenizer, BertModel
import torch
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

import pandas as pd
import numpy as np

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

def preprocess_text(text: str) -> str:
    nltk.download('stopwords')
    nltk.download('wordnet')
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    words = text.split()
    words = [lemmatizer.lemmatize(word.lower()) for word in words if word.lower() not in stop_words]
    return ' '.join(words)

def get_bert_embedding(text: str):
    inputs = tokenizer(text, return_tensors='pt', max_length=512, truncation=True, padding='max_length')
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).detach().numpy()


def recommend_resume(resume_df: pd.DataFrame, job_desc: str) -> pd.DataFrame:
  
    '''Take Resume and return the recommended resumes aligned with the job description'''
    recommended_resumes = pd.DataFrame()
    rows = resume_df.shape[0]
    job_description_embedding = get_bert_embedding(job_desc)
    all_similarity_scores = []
    for row in range(rows):
        resume_skill_str = " ".join(resume_df['skills'].iloc[row])
        resume_aboutSec_str = " ".join(resume_df['about_section'].iloc[row])
        
        resume_text = preprocess_text(" ".join(resume_skill_str + " " + resume_aboutSec_str))
        resume_embedding = get_bert_embedding(resume_text)
        similarity_score = cosine_similarity(resume_embedding, job_description_embedding).flatten()[0]
        
        try:
            experience_match = int(resume_df['past_company_experience'].iloc[row]) >= 0
        except:
            experience_match = False

        print('similarity_score: ',similarity_score, 'experience_match: ',experience_match)

        matching_threshold = 0.0

        if experience_match:
            if similarity_score >= matching_threshold:
                # Add the resume to the recommended resumes DataFrame
                recommended_resumes = pd.concat([recommended_resumes, resume_df.iloc[[row]]])
                all_similarity_scores.append(similarity_score)
                print("Resume matches the job description \n\n")
            else:
                print("similarity score is out of threshold \n\n")
        else:
            print("Resume does not match the job description \n\n")
    
    # Add similarity scores to the recommended resumes DataFrame
    recommended_resumes['similarity_score'] = all_similarity_scores
    return recommended_resumes



# job_desc = '''
# Here is a job description for a Python Developer role:

# Job Title: Python Developer

# Job Summary:

# We are seeking an experienced and skilled Python Developer to join our team. As a Python Developer, you will be responsible for designing, developing, and deploying scalable and efficient software applications using Python programming language. You will work closely with our cross-functional teams to identify and prioritize project requirements, develop innovative solutions, and ensure timely delivery of high-quality products.

# Responsibilities:

# Design and Development:
# Design, develop, test, and deploy Python applications, scripts, and tools
# Write clean, efficient, and well-documented code
# Participate in code reviews and ensure adherence to coding standards
# Problem-Solving:
# Troubleshoot and debug Python applications and scripts
# Identify and resolve performance bottlenecks and scalability issues
# Collaboration:
# Collaborate with cross-functional teams, including data scientists, DevOps, and QA engineers
# Communicate technical information to non-technical stakeholders
# Best Practices:
# Follow best practices for Python development, including testing, documentation, and version control
# Stay up-to-date with industry trends and emerging technologies
# Requirements:

# Education:
# Bachelor's degree in Computer Science, Engineering, or a related field
# Experience:
# At least 3 years of experience in Python development
# Experience with Python frameworks such as Django, Flask, or Pyramid
# Experience with databases, including MySQL, PostgreSQL, or MongoDB
# Skills:
# Proficient in Python 3.x
# Strong understanding of object-oriented programming, data structures, and algorithms
# Experience with testing frameworks such as Pytest or Unittest
# Familiarity with Agile development methodologies
# Excellent problem-solving skills and attention to detail
# Nice to Have:

# Cloud Experience:
# Experience with cloud platforms such as AWS, Google Cloud, or Azure
# Data Science:
# Familiarity with data science concepts and tools, including NumPy, Pandas, and scikit-learn
# DevOps:
# Experience with containerization using Docker and orchestration using Kubernetes
# What We Offer:

# Competitive salary and benefits package
# Opportunities for professional growth and development
# Collaborative and dynamic work environment
# Flexible working hours and remote work options
# If you're a motivated and talented Python Developer looking for a new challenge, please submit your application, including your resume and a cover letter, to [insert contact information].
# '''
# import pandas as pd
# df = pd.read_csv("D:\Techma\CV-Extractor\check_test.csv")
# return_me = recommend_resume(df ,job_desc)
# print(return_me)