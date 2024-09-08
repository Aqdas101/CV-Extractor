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
  
    '''Take Resume and return the recommended resumes align with the job description'''
    recommended_resumes = pd.DataFrame()
    rows = resume_df.shape[0]
    job_description_embedding = get_bert_embedding(job_desc)
    all_similarity_scores = []
    for row in range(rows):
        # print('This is row', row)
        # print("This is row skill: ",resume_df['skills'].iloc[row])
          
        resume_skill_str = " ".join(resume_df['skills'].iloc[row])
        resume_aboutSec_str = " ".join(resume_df['about_section'].iloc[row])
        
        
        resume_text = preprocess_text(" ".join(resume_skill_str + " " + resume_aboutSec_str))
        resume_embedding = get_bert_embedding(resume_text)
        similarity_score = cosine_similarity(resume_embedding, job_description_embedding).flatten()[0]
        experience_match = resume_df['past_company_experience'].iloc[row] >= 0
        print('similarity_score: ',similarity_score, 'experience_match: ',experience_match )
        all_similarity_scores.append(similarity_score)
        matching_threshold = 0.0
        if experience_match:
            if similarity_score >= matching_threshold:
              recommended_resumes = pd.concat([recommended_resumes, resume_df.iloc[[row]]])
              print("Resume matches the job description \n\n")
            else:
                print("similarity score is out of threshold \n\n")
                continue
        else:
            print("Resume does not match the job description \n\n")
    recommended_resumes['similarity_score'] = all_similarity_scores
    return recommended_resumes

