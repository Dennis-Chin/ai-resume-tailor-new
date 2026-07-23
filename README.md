# AI Resume/CV Feedback Generator (MVP)

From start to finish completed in under 24 hours. My first full project done on GitHub. Used Gemini for assistance but no agents. Did all coding in VSCode. Learnt about how to use VSCode to create a frontend using TypeScript/React and the backend using Python. Deployed website using Vercel (frontend) and Render (backend) all for free.

A decoupled, full-stack web application that generates tailored resumes/cvs by cross-referencing a user's resume with a target job description using the Gemini 3.1 Flash Lite model.

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

# AI Cover Letter Generator 🚀

A full-stack web application that uses Google's Gemini AI to automatically generate tailored, professional cover letters by comparing a user's resume against a specific job description.

**[Live Demo](https://ai-resume-tailor-new.vercel.app)**

## 🛠️ Tech Stack
* **Frontend:** Next.js, React, TypeScript, Tailwind CSS (Deployed on Vercel)
* **Backend:** Python, FastAPI, SlowAPI for rate limiting (Deployed on Render)
* **AI Integration:** Google Gemini 3.1 Flash-Lite API

## 🧠 What I Learned
Building this MVP took me through the entire full-stack lifecycle. Beyond just writing code, my biggest takeaways were:
* **Cloud Deployment & Infrastructure:** Learned how to deploy separate frontend and backend services to Vercel and Render, and how to manage environment variables (`.env`) securely in production.
* **CORS & Network Requests:** Debugged Cross-Origin Resource Sharing (CORS) errors to securely allow my Vercel frontend to communicate with my Render backend.
* **Git & Version Control:** Navigated Git workflows, including resolving merge conflicts, forcing pushes, and keeping remote/local branches synced.
* **API Constraints:** Navigated geographic restrictions with Google's API by migrating cloud servers to US-based regions to ensure successful API calls.

## 💻 How to Run Locally
1. Clone the repository.
2. Frontend: `cd frontend` -> `npm install` -> `npm run dev`
3. Backend: `cd backend` -> Create a virtual environment -> `pip install -r requirements.txt` -> `uvicorn main:app --reload`
4. Add your own `GEMINI_API_KEY` to a `.env` file in the backend folder.