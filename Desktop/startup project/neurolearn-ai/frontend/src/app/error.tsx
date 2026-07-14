"use client";

import { useEffect } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { AlertTriangle, RefreshCw, Home } from "lucide-react";

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
      <div className="text-center space-y-6 px-4">
        <div className="flex justify-center">
          <div className="relative">
            <AlertTriangle className="w-32 h-32 text-red-300 dark:text-red-700" />
            <div className="absolute -top-2 -right-2 bg-red-600 text-white text-2xl font-bold rounded-full w-12 h-12 flex items-center justify-center">
              500
            </div>
          </div>
        </div>
        
        <h1 className="text-4xl font-bold text-slate-900 dark:text-slate-100">
          Something went wrong
        </h1>
        
        <p className="text-lg text-slate-600 dark:text-slate-400 max-w-md">
          We encountered an unexpected error. This has been logged and our team has been notified.
        </p>
        
        {error.message && (
          <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 max-w-md mx-auto">
            <p className="text-sm text-red-700 dark:text-red-400 font-mono">
              {error.message}
            </p>
          </div>
        )}
        
        <div className="flex gap-4 justify-center">
          <Button onClick={reset}>
            <RefreshCw className="w-4 h-4 mr-2" />
            Try Again
          </Button>
          
          <Button variant="outline" asChild>
            <Link href="/dashboard">
              <Home className="w-4 h-4 mr-2" />
              Go to Dashboard
            </Link>
          </Button>
        </div>
        
        <div className="pt-8">
          <p className="text-sm text-slate-500 dark:text-slate-500">
            The issue persists? <Link href="/support" className="text-blue-600 hover:underline">Contact Support</Link>
          </p>
        </div>
      </div>
    </div>
  );
}
