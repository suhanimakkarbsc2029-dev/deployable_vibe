import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Deployable - AI-Powered Recruitment",
  description:
    "Get started with Deployable: AI-Powered Recruitment, Deployed Instantly",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
