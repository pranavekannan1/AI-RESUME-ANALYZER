export type Analysis = {
  overall_score?: number;
  score?: number | string;
  summary?: string;
  strengths?: string[];
  weaknesses?: string[];
  suggestions?: string[];
  skills?: string[];
  [key: string]: unknown;
};

export type AnalysisResult = {
  resume_id: string;
  analysis: Analysis;
};

export type UploadResult = {
  resume_id: string;
  filename?: string;
  original_filename?: string;
  file_size?: number;
  message?: string;
  [key: string]: unknown;
};
