import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def score_resume_with_jd(resume_text, job_description):
    prompt = f"""
You are an expert technical recruiter. Based on the job description (if provided) and resume below, respond in the following JSON format:

{{
  "score": <integer from 0 to 100>,
  "strengths": ["<bullet point 1>", "<bullet point 2>", "..."],
  "weaknesses": ["<bullet point 1>", "<bullet point 2>", "..."]
}}

Job Description:
{job_description}

Resume:
{resume_text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    content = response.choices[0].message.content.strip()
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        match = re.search(r'\{.*', content, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
    print("Could not parse this response from OpenAI:", content)
    return {"score": 0, "strengths": [], "weaknesses": ["Could not parse feedback."]}