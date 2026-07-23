"use client";

import { useState } from "react";

export default function Home() {
  // State variables hold the data as the user types and when the backend responds
  const [jobDescription, setJobDescription] = useState("");
  const [resumeText, setResumeText] = useState("");
  const [generatedLetter, setGeneratedLetter] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  // This function runs when the user clicks "Generate"
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault(); 
    setIsLoading(true);
    setGeneratedLetter(""); // Clear previous errors or letters

    try {
      const response = await fetch("https://ai-resume-tailor-new.onrender.com/api/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          job_description: jobDescription,
          resume_text: resumeText,
        }),
      });

      // NEW: Catch backend errors (like the 503/500 from Google) before they crash the app
      if (!response.ok) {
        throw new Error("The AI server is busy or returned an error. Please try again.");
      }

      const data = await response.json();
      setGeneratedLetter(data.cover_letter);
      
    } catch (error) {
      console.error("Error:", error);
      // This will now successfully display on the screen when Google is overloaded
      setGeneratedLetter(error instanceof Error ? error.message : "Connection failed.");
    } finally {
      // This will now always run, un-sticking the button
      setIsLoading(false);
    }
  };

  return (
    <main className="max-w-4xl mx-auto p-8 font-sans">
      <h1 className="text-3xl font-bold mb-8">AI Cover Letter Generator</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* LEFT COLUMN: Input Form */}
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <div>
            <label className="block text-sm font-medium mb-2">Job Description</label>
            <textarea 
              className="w-full p-3 border rounded-md h-48 text-black" 
              placeholder="Paste the job description here..."
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Your Resume (Text)</label>
            <textarea 
              className="w-full p-3 border rounded-md h-48 text-black" 
              placeholder="Paste your resume text here..."
              value={resumeText}
              onChange={(e) => setResumeText(e.target.value)}
              required
            />
          </div>

          <button 
            type="submit" 
            disabled={isLoading}
            className="bg-blue-600 text-white p-3 rounded-md font-medium hover:bg-blue-700 disabled:bg-gray-400"
          >
            {isLoading ? "Generating..." : "Generate Cover Letter"}
          </button>
        </form>

        {/* RIGHT COLUMN: Results Display */}
        <div className="bg-gray-50 p-6 rounded-md border h-full">
          <h2 className="text-xl font-semibold mb-4 text-gray-800">Output</h2>
          {generatedLetter ? (
            <div className="whitespace-pre-wrap text-gray-700">{generatedLetter}</div>
          ) : (
            <p className="text-gray-400 italic">Your generated letter will appear here.</p>
          )}
        </div>
      </div>
    </main>
  );
}