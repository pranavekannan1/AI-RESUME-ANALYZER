import type { AnalysisResult, UploadResult } from "@/types/analysis";

const API_URL = (
  process.env.NEXT_PUBLIC_API_URL ||
  "http://127.0.0.1:8000"
).replace(/\/$/, "");

async function readError(response: Response, fallback: string) {
  try {
    const data = await response.json();

    if (typeof data?.detail === "string") {
      return data.detail;
    }

    if (typeof data?.message === "string") {
      return data.message;
    }
  } catch {
    // Ignore non-JSON errors.
  }

  return fallback;
}

export async function uploadResume(
  file: File
): Promise<UploadResult> {
  const formData = new FormData();
  formData.append("file", file);

  let response: Response;

  try {
    response = await fetch(`${API_URL}/upload/`, {
      method: "POST",
      body: formData,
    });
  } catch {
    throw new Error(
      `Cannot reach the backend at ${API_URL}. Make sure FastAPI is running.`
    );
  }

  if (!response.ok) {
    throw new Error(
      await readError(response, "Resume upload failed.")
    );
  }

  return response.json();
}

export async function analyzeResume(
  resumeId: string
): Promise<AnalysisResult> {
  let response: Response;

  try {
    response = await fetch(`${API_URL}/analyze/${resumeId}`, {
      method: "POST",
    });
  } catch {
    throw new Error(
      `Cannot reach the backend at ${API_URL}.`
    );
  }

  if (!response.ok) {
    throw new Error(
      await readError(response, "Resume analysis failed.")
    );
  }

  return response.json();
}