import Link from "next/link";
import { Button } from "@/components/ui/button";
import { FileQuestion, Home } from "lucide-react";

export default function NotFound() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
      <div className="text-center space-y-6 px-4">
        <div className="flex justify-center">
          <div className="relative">
            <FileQuestion className="w-32 h-32 text-slate-300 dark:text-slate-600" />
            <div className="absolute -top-2 -right-2 bg-red-500 text-white text-2xl font-bold rounded-full w-12 h-12 flex items-center justify-center">
              404
            </div>
          </div>
        </div>
        
        <h1 className="text-4xl font-bold text-slate-900 dark:text-slate-100">
          Page Not Found
        </h1>
        
        <p className="text-lg text-slate-600 dark:text-slate-400 max-w-md">
          Sorry, we couldn't find the page you're looking for. It might have been removed, renamed, or doesn't exist.
        </p>
        
        <div className="flex gap-4 justify-center">
          <Button asChild>
            <Link href="/dashboard">
              <Home className="w-4 h-4 mr-2" />
              Go to Dashboard
            </Link>
          </Button>
          
          <Button variant="outline" asChild>
            <Link href="/">
              Back to Home
            </Link>
          </Button>
        </div>
        
        <div className="pt-8">
          <p className="text-sm text-slate-500 dark:text-slate-500">
            Need help? <Link href="/support" className="text-blue-600 hover:underline">Contact Support</Link>
          </p>
        </div>
      </div>
    </div>
  );
}
