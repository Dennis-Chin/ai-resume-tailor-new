import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Load variables from the .env file into the environment
load_dotenv()

# 1. Initialize the app EXACTLY ONCE
app = FastAPI(title="Resume Tailor API")

# 2. Add the CORS VIP Pass to this specific app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)

# 3. Setup the Rate Limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

class GenerationRequest(BaseModel):
    job_description: str
    resume_text: str

# Initialize the modern Gemini client
client = genai.Client()

@app.post("/api/generate")
@limiter.limit("5/minute") 
async def tailor_resume(request: Request, generation_request: GenerationRequest):
    try:
        # 4. RESTORED: The actual prompt instructions for Gemini!
        prompt = f"""
        Provide a score out of 100 based on how effective it is and list key ways to improve it.
        You are an expert career coach and resume/cv tailor writer.
        Suggest critical concise key improvements where necessary to improve the input only where necessary. 
        Write a professional, compelling resume/cv based on the following inputs.
        Do not include any placeholder brackets like [Your Name] — format it so I can copy and paste it directly.
        Avoid using * excessively and ensure that output is clear and concise and easy to understand.
        
        Job Description:
        {generation_request.job_description}

        My Resume:
        {generation_request.resume_text}
        """

        response = client.models.generate_content(
            model='gemini-3.1-flash-lite',
            contents=prompt,
        )
        
        # THE CONTRACT: Returning the newly named JSON key
        return {"tailored_resume": response.text}
        
    except Exception as e:
        print(f"Error calling Gemini: {e}") 
        raise HTTPException(status_code=500, detail="Failed to tailor resume.")