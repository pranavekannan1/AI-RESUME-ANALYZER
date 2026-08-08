import type { AnalysisResult, UploadResult } from "@/types/analysis";

const API_URL = "https://ai-resume-analyzer-zcu2.onrender.com";

async function readError(
  response: Response,
  fallback: string
): Promise<string> {
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
  } catch (error) {
    console.error("BACKEND FETCH ERROR:", error);

    throw new Error(
      `Cannot connect to ${API_URL}. Check the browser console for the actual network/CORS error.`
    );
  }

  if (!response.ok) {
    const errorMessage = await readError(
      response,
      "Resume upload failed."
    );

    console.error("BACKEND ERROR:", response.status, errorMessage);

    throw new Error(errorMessage);
  }

  const data = await response.json();

  console.log("UPLOAD RESPONSE:", data);

  return data;
}

export async function analyzeResume(
  resumeId: string
): Promise<AnalysisResult> {
  let response: Response;

  try {
    response = await fetch(
      `${API_URL}/analyze/${resumeId}`,
      {
        method: "POST",
      }
    );
  } catch (error) {
    console.error("ANALYZE FETCH ERROR:", error);

    throw new Error(
      `Cannot connect to ${API_URL}. Check the browser console.`
    );
  }

  if (!response.ok) {
    throw new Error(
      await readError(
        response,
        "Resume analysis failed."
      )
    );
  }

  return response.json();
}