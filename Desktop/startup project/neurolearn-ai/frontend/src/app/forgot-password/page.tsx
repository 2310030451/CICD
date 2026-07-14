"use client";

import { useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Brain, Loader2, ArrowLeft, CheckCircle2 } from "lucide-react";
import { resetPassword } from "@/lib/firebase";
import { useToast } from "@/components/ui/use-toast";

export default function ForgotPasswordPage() {
  const { toast } = useToast();

  const [email, setEmail] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isSent, setIsSent] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setIsLoading(true);
      await resetPassword(email);
      setIsSent(true);
      toast({
        title: "Success",
        description: "Password reset email sent successfully",
      });
    } catch (error: any) {
      toast({
        variant: "destructive",
        title: "Error",
        description: error.message || "Failed to send reset email",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-50 via-white to-blue-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 px-4">
      <Card className="w-full max-w-md">
        <CardHeader className="space-y-1">
          <div className="flex items-center justify-center mb-4">
            <Brain className="h-10 w-10 text-purple-600" />
          </div>
          <CardTitle className="text-2xl text-center">Reset your password</CardTitle>
          <CardDescription className="text-center">
            Enter your email address and we'll send you a link to reset your password
          </CardDescription>
        </CardHeader>
        <CardContent>
          {!isSent ? (
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="name@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  disabled={isLoading}
                />
              </div>
              <Button type="submit" className="w-full" disabled={isLoading}>
                {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                Send Reset Link
              </Button>
            </form>
          ) : (
            <div className="text-center space-y-4">
              <div className="flex justify-center">
                <CheckCircle2 className="h-16 w-16 text-green-500" />
              </div>
              <div>
                <h3 className="text-lg font-semibold">Email sent!</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
                  Check your email for the password reset link
                </p>
              </div>
              <Button
                variant="outline"
                className="w-full"
                onClick={() => setIsSent(false)}
              >
                Send again
              </Button>
            </div>
          )}
        </CardContent>
        <CardFooter>
          <Link href="/login" className="flex items-center text-sm text-purple-600 hover:text-purple-700">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to login
          </Link>
        </CardFooter>
      </Card>
    </div>
  );
}
