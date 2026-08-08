import type { AnalysisResult, UploadResult } from "@/types/analysis";

const API_URL = (process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000").replace(/\/$/, "");

async function readError(response: Response, fallback: string) {
  try {
    const data = await response.json();
    if (typeof data?.detail === "string") return data.detail;
    if (typeof data?.message === "string") return data.message;
  } catch {
    // Ignore non-JSON errors.
  }
  return fallback;
}

export async function uploadResume(file: File): Promise<UploadResult> {
  const formData = new FormData();
  formData.append("file", file);

  let response: Response;
  try {
    response = await fetch(`${API_URL}/upload/`, {
      method: "POST",
      body: formData,
    });
  } catch {
    throw new Error(`Cannot reach the backend at ${API_URL}. Make sure FastAPI is running on port 8000.`);
  }

  if (!response.ok) {
    throw new Error(await readError(response, "Resume upload failed."));
  }

  const data: UploadResult = await response.json();

  if (!data || typeof data.resume_id !== "string" || !data.resume_id.trim()) {
    console.error("Invalid upload response:", data);
    throw new Error("Upload succeeded, but the backend did not return a valid resume ID.");
  }

  return data;
}

export async function analyzeResume(resumeId: string): Promise<AnalysisResult> {
  if (!resumeId.trim()) {
    throw new Error("Invalid resume ID.");
  }

  let response: Response;
  try {
    response = await fetch(`${API_URL}/analyze/${encodeURIComponent(resumeId)}`, {
      method: "POST",
    });
  } catch {
    throw new Error(`Cannot reach the backend at ${API_URL}. Make sure FastAPI is running on port 8000.`);
  }

  if (!response.ok) {
    throw new Error(await readError(response, "Resume analysis failed."));
  }

  const data: AnalysisResult = await response.json();

  if (!data?.resume_id || !data?.analysis) {
    throw new Error("Backend returned an invalid analysis response.");
  }

  return data;
}
