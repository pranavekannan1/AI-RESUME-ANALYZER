# AI Resume Analyzer Backend

Production-ready FastAPI backend using MongoDB Atlas and Gemini.

## Features

- PDF upload and text extraction
- MongoDB persistence
- PDF bytes stored with the resume document (5 MB upload limit)
- Gemini-powered resume analysis
- Strict Pydantic validation of AI JSON
- CORS for Next.js
- Health endpoint
- Deployment-friendly environment configuration

## Local setup

```powershell
cd "C:\Users\Asus\Projects\AI Resume Analyzer\backend"
python -m pip install -r requirements.txt
```

Create `.env` from `.env.example` and set:

```env
GEMINI_API_KEY=...
GEMINI_MODEL=gemini-3.5-flash
MONGODB_URI=mongodb+srv://...
MONGODB_DATABASE=ai_resume_analyzer
CORS_ORIGINS=http://localhost:3000
```

Run:

```powershell
uvicorn main:app --reload
```

## Production start

```powershell
uvicorn main:app --host 0.0.0.0 --port $env:PORT
```

If your hosting provider injects `PORT`, use that value. Otherwise use 8000.

## API flow

1. `POST /upload/` with a PDF.
2. Read the returned `resume_id`.
3. `POST /analyze/{resume_id}`.
4. The response contains the validated analysis.

## MongoDB

The uploaded PDF is stored as binary data inside the MongoDB resume document. The maximum upload size is 5 MB, keeping each document safely below MongoDB's 16 MB BSON document limit.

## Security

Never put `GEMINI_API_KEY` or `MONGODB_URI` in the Next.js frontend or commit `.env` to Git.
