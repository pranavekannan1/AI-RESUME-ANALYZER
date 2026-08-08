# AI Resume Analyzer
# AI-RESUME-ANALYZER

Full-stack resume analyzer using Next.js, FastAPI, MongoDB Atlas, PDF text extraction, and Gemini.

## Structure

- `frontend/` — Next.js UI
- `backend/` — FastAPI API

## Local setup

### Backend

1. Create `backend/.env` from `backend/.env.example`.
2. Put your Gemini API key and MongoDB Atlas URI in it.
3. From `backend/` run:

```powershell
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

API: http://127.0.0.1:8000
Docs: http://127.0.0.1:8000/docs

### Frontend

1. Create `frontend/.env.local` from `frontend/.env.local.example`.
2. From `frontend/` run:

```powershell
npm install
npm run dev
```

Open http://localhost:3000.

## Flow

Upload PDF -> extract text -> store resume in MongoDB -> call Gemini -> validate structured analysis -> save analysis -> display results.

## Deployment

Deploy the backend as a Python web service/container and set the same environment variables in the hosting provider. Deploy the frontend as a Next.js app and set `NEXT_PUBLIC_API_URL` to the deployed backend URL.
