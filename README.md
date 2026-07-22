# AI Cover Letter Generator (MVP)

A decoupled, full-stack web application that generates tailored cover letters by cross-referencing a user's resume with a target job description using the Gemini 3.1 Flash Lite model.

## 🏗 Architecture & Design Decisions

This project uses a **Service-Boundary** pattern, strictly separating the user interface from the AI inference engine. 

*   **Frontend (Next.js / TypeScript / React):** 
    Handles state management and user input via controlled components. It is completely blind to the AI logic, acting only as a client that sends JSON payloads and receives text.
*   **Backend (Python / FastAPI):** 
    Acts as an isolated microservice. It handles prompt construction, secures the API keys via environment variables, and manages the network call to the Google Generative AI API.

**Why decoupled?** 
This architecture provides maximum leverage. The Python backend can be scaled independently, swapped to a different LLM (like Claude or OpenAI) without touching the UI, or connected to a completely different frontend (like a React Native mobile app) in the future.

## 🚀 Local Setup

1. **Start the AI Engine (Backend):**
   ```bash
   cd backend
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn main:app --reload
