"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    if (typeof window !== "undefined") {
      const token = localStorage.getItem("token");
      if (token) {
        router.push("/dashboard");
      }
    }
  }, [router]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-600 to-blue-800 text-white">
      {/* Navigation */}
      <nav className="flex justify-between items-center px-8 py-6">
        <div className="text-3xl font-bold">Deployable</div>
        <div className="space-x-4">
          <Link
            href="/login"
            className="px-6 py-2 rounded-lg border border-white hover:bg-white hover:text-blue-600 transition"
          >
            Login
          </Link>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="flex flex-col items-center justify-center min-h-[80vh] px-4 text-center">
        <h1 className="text-6xl font-bold mb-6 leading-tight">
          AI-Powered Recruitment, Deployed Instantly
        </h1>
        <p className="text-xl mb-12 max-w-2xl text-blue-100">
          Match the perfect candidates to your jobs intelligently. Deploy your
          recruitment workflow in minutes, not months.
        </p>

        {/* CTA Buttons */}
        <div className="flex gap-6">
          <Link
            href="/signup"
            className="px-8 py-3 bg-white text-blue-600 font-semibold rounded-lg hover:bg-gray-100 transition shadow-lg"
          >
            Get Started
          </Link>
          <Link
            href="/login"
            className="px-8 py-3 bg-transparent border-2 border-white text-white font-semibold rounded-lg hover:bg-white hover:text-blue-600 transition"
          >
            Login
          </Link>
        </div>
      </div>

      {/* Footer */}
      <footer className="text-center py-8 text-blue-100 border-t border-blue-500">
        <p>&copy; 2026 Deployable. All rights reserved.</p>
      </footer>
    </div>
  );
}
