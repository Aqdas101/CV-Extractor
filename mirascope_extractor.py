from mirascope.openai import OpenAIExtractor
from mirascope.gemini import GeminiExtractor
from mirascope.groq import GroqExtractor

from tenacity import retry, stop_after_attempt, wait_fixed, before_sleep_log

from pydantic import FilePath, BaseModel
from typing import List, Type


class TaskDetails(BaseModel):
    name: str
    email: str
    phone_number: str
    skills: List[str]
    education: List[str]
    past_company_experience: int
    about_section: str

class TaskExtractor(OpenAIExtractor[TaskDetails]):
    extract_schema: Type[TaskDetails] = TaskDetails
    prompt_template = """
    Extract the Resume details from the following Resume:
    
    Note: Extract Experience by calculating the working tenure
    {resume}
    """
    resume: str

def retry_callback(retry_state):
    print(f"Retrying... Attempt {retry_state.attempt_number}")

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2), before_sleep=retry_callback)
def extractor(text):
    print('Start -- Transforming CV Text into Tabular Form')
    task_details = TaskExtractor(resume=text).extract()
    assert isinstance(task_details, TaskDetails)
    print('End -- Transforming CV Text into Tabular Form \n\n')
    return task_details

