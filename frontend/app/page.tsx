"use client";

import { useState } from "react";
import { uploadResume, analyzeResume } from "@/lib/api";
import type { Analysis } from "@/types/analysis";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleAnalyze() {
    if (!file) {
      setError("Please select a valid resume PDF first.");
      return;
    }

    setLoading(true);
    setError("");
    setAnalysis(null);

    try {
      const uploadResult = await uploadResume(file);

      console.log("Upload result:", uploadResult);

      const resumeId = uploadResult.resume_id;

      if (!resumeId || typeof resumeId !== "string") {
        throw new Error(`Invalid resume ID returned by backend: ${uploadResult.resume_id}`);
      }

      const analysisResult = await analyzeResume(resumeId);

      console.log("Analysis result:", analysisResult);

      setAnalysis(analysisResult.analysis);
    } catch (err) {
      console.error(err);

      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong while analyzing the resume."
      );
    } finally {
      setLoading(false);
    }
  }

  function handleFileChange(selectedFile: File | null) {
    setError("");
    setAnalysis(null);

    if (!selectedFile) {
      setFile(null);
      return;
    }

    const filename = selectedFile.name.toLowerCase();
    const isPdfFile =
      filename.endsWith(".pdf") ||
      selectedFile.type === "application/pdf";

    if (!isPdfFile) {
      setError("Only a resume PDF file is allowed.");
      setFile(null);
      return;
    }

    setFile(selectedFile);
  }

  function removeFile() {
    setFile(null);
    setAnalysis(null);
    setError("");
  }

  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <header className="border-b border-white/10 bg-slate-950/80 backdrop-blur-xl">
        <div className="mx-auto flex min-h-[88px] max-w-6xl items-center justify-between px-6">
          <div className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-gradient-to-br from-emerald-300 to-blue-500 shadow-lg shadow-emerald-500/20">
              <span className="text-base font-black text-slate-950">R</span>
            </div>
            <div>
              <h1 className="text-2xl font-black leading-none tracking-tight text-white">
                Reslytics v1.0
              </h1>
              <p className="mt-1 text-[10px] font-semibold uppercase tracking-[0.2em] text-slate-400">
                Powered by Resume Intelligence
              </p>
            </div>
          </div>

          <nav className="hidden items-center gap-10 md:flex">
            <a className="text-sm font-bold text-slate-300 transition hover:text-emerald-300" href="#">
              Dashboard
            </a>
            <a className="text-sm font-bold text-slate-300 transition hover:text-emerald-300" href="#">
              Analysis
            </a>
            <a className="text-sm font-bold text-slate-300 transition hover:text-emerald-300" href="#">
              Insights
            </a>
          </nav>

          <div className="rounded-full border border-emerald-400/30 bg-emerald-400/10 px-4 py-2 text-[10px] font-black uppercase tracking-[0.22em] text-emerald-300">
            Reslytics AI
          </div>
        </div>
      </header>

      <div className="mx-auto max-w-6xl px-6 py-12 md:py-14">
        {!analysis ? (
          <>
            <section className="mx-auto max-w-4xl text-center">
              <div className="mb-5 inline-flex rounded-full border border-emerald-400/30 bg-emerald-400/10 px-4 py-2 text-sm font-semibold text-emerald-300">
                Reslytics Resume Analysis
              </div>

              <h2 className="text-4xl font-black leading-none tracking-tight sm:text-6xl">
                Turn your resume
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-300 to-blue-400">
                  {" "}into opportunity.
                </span>
              </h2>

              <p className="mx-auto mt-7 max-w-3xl text-lg leading-8 text-slate-400">
                Reslytics helps you understand where your resume stands,
                what recruiters are looking for, and how to improve your
                chances of landing the next role.
              </p>

              <div className="mt-8 flex items-center justify-center gap-4">
                <a href="#resume" className="rounded-full bg-emerald-400 px-7 py-3 text-sm font-black text-slate-950 transition hover:bg-emerald-300">
                  Analyze Resume
                </a>
                <a href="#features" className="rounded-full border border-white/15 px-7 py-3 text-sm font-bold text-slate-300 transition hover:bg-white/8 hover:text-white">
                  Explore Features
                </a>
              </div>
            </section>

            <section className="mx-auto mt-12 max-w-2xl">
              <div className="rounded-[2rem] border border-white/10 bg-white/[0.05] p-8 shadow-2xl shadow-emerald-950/40 backdrop-blur-xl">
                {!file ? (
                  <label
                    htmlFor="resume"
                    className="flex cursor-pointer flex-col items-center justify-center rounded-2xl border-2 border-dashed border-slate-600 px-6 py-16 text-center transition duration-300 hover:border-emerald-300 hover:bg-emerald-300/5 hover:scale-[1.01]"
                  >
                    <div className="mb-5 flex h-20 w-20 items-center justify-center rounded-3xl bg-gradient-to-br from-blue-500/20 to-emerald-500/20 text-4xl ring-1 ring-white/15">
                      📄
                    </div>

                    <h3 className="text-xl font-bold text-white">
                      Upload your resume
                    </h3>

                    <p className="mt-2 text-sm text-slate-400">
                      Drag and drop your resume PDF here or click to browse
                    </p>

                    <span className="mt-6 rounded-xl bg-gradient-to-r from-emerald-300 to-blue-500 px-6 py-3 text-sm font-black text-slate-950 shadow-lg shadow-emerald-950/30">
                      Choose Resume PDF
                    </span>

                    <input
                      id="resume"
                      type="file"
                      accept="application/pdf,.pdf"
                      className="hidden"
                      onChange={(event) =>
                        handleFileChange(
                          event.target.files?.[0] ?? null
                        )
                      }
                    />
                  </label>
                ) : (
                  <div className="rounded-2xl border border-emerald-500/30 bg-emerald-500/7 p-6">
                    <div className="flex items-center gap-4">
                      <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-red-500/10 text-2xl">
                        PDF
                      </div>

                      <div className="min-w-0 flex-1">
                        <p className="truncate font-semibold text-white">
                          {file.name}
                        </p>

                        <p className="mt-1 text-sm text-slate-400">
                          {(file.size / 1024 / 1024).toFixed(2)} MB
                        </p>
                      </div>

                      <button
                        onClick={removeFile}
                        className="rounded-lg px-3 py-2 text-sm font-medium text-slate-400 transition hover:bg-white/10 hover:text-white"
                      >
                        Remove
                      </button>
                    </div>
                  </div>
                )}

                {error && (
                  <div className="mt-5 rounded-xl border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-300">
                    {error}
                  </div>
                )}

                {file && (
                  <button
                    onClick={handleAnalyze}
                    disabled={loading}
                    className="mt-6 w-full rounded-2xl bg-gradient-to-r from-blue-500 to-emerald-400 px-6 py-4 font-black text-slate-950 transition hover:scale-[1.01] disabled:cursor-not-allowed disabled:opacity-50"
                  >
                    {loading ? (
                      <span className="flex items-center justify-center gap-3">
                        <span className="h-5 w-5 animate-spin rounded-full border-2 border-slate-950/30 border-t-slate-950" />
                        Analyzing Resume...
                      </span>
                    ) : (
                      "Analyze Resume →"
                    )}
                  </button>
                )}
              </div>
            </section>

            <section id="features" className="mx-auto mt-16 grid max-w-4xl gap-5 sm:grid-cols-3">
              <Feature
                icon="🎯"
                title="Resume Score"
                description="Get a clear AI-powered evaluation of your resume."
              />

              <Feature
                icon="💡"
                title="Smart Suggestions"
                description="Uncover improvements that support stronger job applications."
              />

              <Feature
                icon="🧠"
                title="Skill Analysis"
                description="Understand your professional strengths and skill gaps."
              />
            </section>
          </>
        ) : (
          <Results
            analysis={analysis}
            onBack={() => {
              setAnalysis(null);
              setFile(null);
              setError("");
            }}
            onAnalyzeAnother={() => {
              setAnalysis(null);
              setFile(null);
              setError("");
            }}
          />
        )}
      </div>

      <footer className="mt-12 border-t border-white/10 bg-slate-950/60">
        <div className="mx-auto flex min-h-[72px] max-w-6xl flex-col items-center justify-center gap-2 px-6 text-center md:flex-row md:justify-between md:text-left">
          <div className="flex flex-col gap-1">
            <div className="text-base font-black tracking-tight text-white">
              Reslytics v1.0
            </div>
            <div className="text-[10px] font-bold uppercase tracking-[0.22em] text-slate-500">
              Powered by Resume Intelligence
            </div>
          </div>
          <div className="text-xs font-semibold text-slate-400">
            Developed by Mahi Devs
          </div>
          <div className="text-xs font-semibold text-slate-500">
            © 2026 Reslytics. All rights reserved.
          </div>
        </div>
      </footer>
    </main>
  );
}

function Feature({
  icon,
  title,
  description,
}: {
  icon: string;
  title: string;
  description: string;
}) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-6">
      <div className="mb-4 text-2xl">{icon}</div>

      <h3 className="font-semibold">
        {title}
      </h3>

      <p className="mt-2 text-sm leading-6 text-slate-400">
        {description}
      </p>
    </div>
  );
}

function Results({
  analysis,
  onBack,
  onAnalyzeAnother,
}: {
  analysis: Analysis;
  onBack: () => void;
  onAnalyzeAnother: () => void;
}) {
  return (
    <section className="mx-auto max-w-6xl px-2 sm:px-4">
      {/* RESULTS HEADER */}
      <div className="mb-10 flex flex-col gap-6">
        <div>
          <p className="text-sm font-medium text-blue-400">
            ANALYSIS COMPLETE
          </p>

          <h2 className="mt-2 text-3xl font-bold leading-tight sm:text-4xl lg:text-5xl">
            Your Resume Results
          </h2>

          <p className="mt-3 text-sm leading-6 text-slate-400 sm:text-base">
            Here's what our AI found in your resume.
          </p>
        </div>

        <div className="flex flex-col gap-3 sm:flex-row">
          <button
            onClick={onBack}
            className="inline-flex items-center justify-center rounded-2xl border border-white/15 px-5 py-3 text-sm font-black text-white transition hover:bg-white/10"
          >
            ← Back
          </button>

          <button
            onClick={onAnalyzeAnother}
            className="inline-flex items-center justify-center rounded-2xl bg-gradient-to-r from-emerald-300 to-blue-500 px-5 py-3 text-sm font-black text-slate-950 transition hover:scale-[1.02]"
          >
            Analyze Another Resume
          </button>
        </div>
      </div>

      {/* SCORE */}
      <div className="grid gap-6 sm:grid-cols-2 xl:grid-cols-3">

        <div className="rounded-2xl border border-white/10 bg-white/[0.04] p-6">
          <p className="text-sm text-slate-400">
            Resume Score
          </p>

          <div className="mt-4 text-5xl font-bold text-blue-400">
            {analysis.overall_score ?? analysis.score ?? "N/A"}
          </div>

          <p className="mt-2 text-sm text-slate-500">
            Overall resume evaluation
          </p>
        </div>

        <ResultCard
          title="Strengths"
          items={analysis.strengths}
          icon="✓"
        />

        <ResultCard
          title="Weaknesses"
          items={analysis.weaknesses}
          icon="!"
        />
      </div>

      {/* SUMMARY */}
      <div className="mt-6 rounded-2xl border border-white/10 bg-white/[0.04] p-5 sm:p-7">
        <h3 className="text-xl font-semibold">
          Summary
        </h3>

        <p className="mt-4 leading-8 text-slate-300">
          {analysis.summary || "No summary available."}
        </p>
      </div>

      {/* SUGGESTIONS */}
      <div className="mt-6 rounded-2xl border border-white/10 bg-white/[0.04] p-5 sm:p-7">
        <h3 className="text-xl font-semibold">
          Improvement Suggestions
        </h3>

        {analysis.suggestions?.length ? (
          <ul className="mt-5 space-y-4">
            {analysis.suggestions.map((suggestion, index) => (
              <li
                key={index}
                className="flex gap-3 rounded-xl bg-white/[0.03] p-4"
              >
                <span className="text-blue-400">
                  {index + 1}.
                </span>

                <span className="text-slate-300">
                  {suggestion}
                </span>
              </li>
            ))}
          </ul>
        ) : (
          <p className="mt-4 text-slate-400">
            No suggestions available.
          </p>
        )}
      </div>

      {/* SKILLS */}
      <div className="mt-6 rounded-2xl border border-white/10 bg-white/[0.04] p-5 sm:p-7">
        <h3 className="text-xl font-semibold">
          Detected Skills
        </h3>

        {analysis.skills?.length ? (
          <div className="mt-5 flex flex-wrap gap-3">
            {analysis.skills.map((skill, index) => (
              <span
                key={index}
                className="rounded-full border border-blue-400/20 bg-blue-400/10 px-4 py-2 text-sm text-blue-300"
              >
                {skill}
              </span>
            ))}
          </div>
        ) : (
          <p className="mt-4 text-slate-400">
            No skills detected.
          </p>
        )}
      </div>
    </section>
  );
}

function ResultCard({
  title,
  items,
  icon,
}: {
  title: string;
  items?: string[];
  icon: string;
}) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/[0.04] p-6">
      <h3 className="font-semibold">
        {icon} {title}
      </h3>

      {items?.length ? (
        <ul className="mt-4 space-y-3">
          {items.slice(0, 4).map((item, index) => (
            <li
              key={index}
              className="text-sm leading-6 text-slate-400"
            >
              • {item}
            </li>
          ))}
        </ul>
      ) : (
        <p className="mt-4 text-sm text-slate-500">
          None available.
        </p>
      )}
    </div>
  );
}

