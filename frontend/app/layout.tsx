import type { Metadata, Viewport } from "next";
import { Inter } from "next/font/google";
import { ThemeProvider } from "@/components/providers/ThemeProvider";
import { QueryProvider } from "@/components/providers/QueryProvider";
import { Toaster } from "sonner";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

export const metadata: Metadata = {
  title: {
    default: "AKM45 Vector AI — AI-Powered Recruitment Platform",
    template: "%s | AKM45 Vector AI",
  },
  description:
    "The intelligent applicant tracking system that uses AI to parse resumes, rank candidates, and help you hire smarter and faster.",
  keywords: [
    "ATS",
    "applicant tracking system",
    "AI recruitment",
    "resume screening",
    "hiring platform",
    "HR software",
    "candidate ranking",
  ],
  authors: [{ name: "AKM45 Vector AI" }],
  creator: "AKM45 Vector AI",
  openGraph: {
    type: "website",
    locale: "en_US",
    title: "AKM45 Vector AI — AI-Powered Recruitment Platform",
    description:
      "The intelligent ATS that uses AI to parse resumes, rank candidates, and help you hire smarter.",
    siteName: "AKM45 Vector AI",
  },
  twitter: {
    card: "summary_large_image",
    title: "AKM45 Vector AI",
    description: "AI-Powered Resume Screening & Candidate Ranking Platform",
  },
  robots: {
    index: true,
    follow: true,
  },
};

export const viewport: Viewport = {
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#ffffff" },
    { media: "(prefers-color-scheme: dark)", color: "#0d0f1a" },
  ],
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning className={inter.variable}>
      <body>
        <ThemeProvider
          attribute="class"
          defaultTheme="dark"
          enableSystem
          disableTransitionOnChange
        >
          <QueryProvider>
            {children}
            <Toaster
              position="top-right"
              richColors
              closeButton
              duration={4000}
            />
          </QueryProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
