# ResumeAI — AI Resume Analyzer

A Next.js frontend for the AI Resume Analyzer project.

## Stack

- Next.js 16
- React 19
- TypeScript
- Tailwind CSS 4
- FastAPI backend
- Gemini AI

## Run locally

1. Start the FastAPI backend on `http://127.0.0.1:8000`.
2. Create `.env.local` from `.env.local.example` if you want to change the backend URL.
3. Install dependencies:

```bash
npm install
```

4. Start Next.js:

```bash
npm run dev
```

5. Open `http://localhost:3000`.

## User flow

PDF → `/upload/` → resume ID → `/analyze/{resume_id}` → structured AI result → dashboard.
