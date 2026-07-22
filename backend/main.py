import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv

# Load variables from the .env file into the environment
load_dotenv()

app = FastAPI(title="Cover Letter API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerationRequest(BaseModel):
    job_description: str
    resume_text: str

# Initialize the modern Gemini client. 
# It automatically finds GEMINI_API_KEY in the environment.
client = genai.Client()

@app.post("/api/generate")
async def generate_letter(request: GenerationRequest):
    try:
        prompt = f"""
        You are an expert career coach and cover letter writer. 
        Write a professional, compelling cover letter based on the following inputs.
        Do not include any placeholder brackets like [Your Name] — format it so I can copy and paste it directly.

        Job Description:
        {request.job_description}

        My Resume:
        {request.resume_text}
        """

        # Make the call using the new SDK syntax
        response = client.models.generate_content(
            model='gemini-3.1-flash-lite',
            contents=prompt,
        )
        
        return {"cover_letter": response.text}
        
    except Exception as e:
        print(f"Error calling Gemini: {e}") 
        raise HTTPException(status_code=500, detail="Failed to generate cover letter.")