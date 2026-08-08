import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ReScan | AI Resume Analyzer",
  description: "ReScan analyzes resumes with AI and delivers clear, actionable career feedback.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>{children}</body>
    </html>
  );
}
