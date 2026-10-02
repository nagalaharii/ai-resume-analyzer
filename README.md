# AI Resume Analyzer

A simple web app that compares a resume with a job description using the Gemini API and gives a match score, matching skills, missing skills and improvement tips.

## How it works
1. The user pastes a resume and a job description.
2. The app builds a prompt and sends it to the Gemini API.
3. The AI returns the result in JSON format.
4. The app shows the score, skills and tips.

## Tech used
- Python
- Streamlit
- Google Gemini API

## How to run
1. Install libraries: `pip install -r requirements.txt`
2. Create `.streamlit/secrets.toml` and add: `GEMINI_API_KEY = "your_key"`
3. Run: `streamlit run app.py`

## Limitations
- AI can make mistakes, so the score is guidance, not a final decision.
- Resume text must be pasted (no PDF upload yet).

## Future improvements
- PDF resume upload
- Save analysis history
- Generate an improved version of the resume
Live demo: https://ai-resume-analyzer-d8w5vm5txqo6ag3xzukmnc.streamlit.app/
