import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv

# Load variables from the .env file into the environment
load_dotenv()

app = FastAPI(title="Cover Letter API")

# 2. Add this entire block to give the VIP pass to your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows any frontend URL to connect
    allow_credentials=True,
    allow_methods=["*"],  # Allows POST requests
    allow_headers=["*"],
)

class GenerationRequest(BaseModel):
    job_description: str
    resume_text: str

# Initialize the modern Gemini client. 
# It automatically finds GEMINI_API_KEY in the environment.
client = genai.Client()





from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request

# Create the limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Apply the limiter to your route (e.g., 5 requests per minute)
# 1. Cosmetic: Change the title of your API
# Old: app = FastAPI(title="Cover Letter API")
app = FastAPI(title="Resume Tailor API")

# ... (middleware and limiter stay exactly the same) ...

# 2. Internal variable: Rename the function so your Python code makes sense to you
# Old: async def generate_letter(...)
@app.post("/api/generate")
@limiter.limit("5/minute") 
async def tailor_resume(request: Request, generation_request: GenerationRequest):
    try:
        # ... (your prompt stays exactly the same) ...

        response = client.models.generate_content(
            model='gemini-3.1-flash-lite',
            contents=prompt,
        )
        
        # 3. THE CONTRACT: This is the critical change. We are changing the JSON key.
        # Old: return {"cover_letter": response.text}
        return {"tailored_resume": response.text}
        
    except Exception as e:
        print(f"Error calling Gemini: {e}") 
        # 4. Cosmetic: Change the error message
        # Old: detail="Failed to generate cover letter."
        raise HTTPException(status_code=500, detail="Failed to tailor resume.")