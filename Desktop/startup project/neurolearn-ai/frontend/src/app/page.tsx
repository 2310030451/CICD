import Link from "next/link";
import { Button } from "@/components/ui/button";
import {
  BookOpen,
  Brain,
  MessageSquare,
  Target,
  Zap,
  ArrowRight,
  CheckCircle2,
} from "lucide-react";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      <nav className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Brain className="h-8 w-8 text-purple-600" />
            <span className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
              NeuroLearn AI
            </span>
          </div>
          <div className="flex items-center space-x-4">
            <Link href="/login">
              <Button variant="ghost">Sign In</Button>
            </Link>
            <Link href="/register">
              <Button>Get Started</Button>
            </Link>
          </div>
        </div>
      </nav>

      <main className="container mx-auto px-6 py-20">
        <div className="text-center max-w-4xl mx-auto">
          <div className="inline-flex items-center px-4 py-2 rounded-full bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 text-sm font-medium mb-6">
            <Zap className="h-4 w-4 mr-2" />
            Powered by Advanced AI
          </div>
          <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-purple-600 via-blue-600 to-cyan-600 bg-clip-text text-transparent">
            Learn Smarter with AI
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 mb-8 max-w-2xl mx-auto">
            A multimodal AI-powered learning platform that adapts to your learning style, 
            predicts your performance, and provides personalized tutoring.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/register">
              <Button size="lg" className="text-lg px-8">
                Start Learning Free
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </Link>
            <Link href="/login">
              <Button size="lg" variant="outline" className="text-lg px-8">
                View Demo
              </Button>
            </Link>
          </div>
        </div>

        <div className="grid md:grid-cols-3 gap-8 mt-20">
          {features.map((feature, index) => (
            <div
              key={index}
              className="p-6 rounded-2xl bg-white dark:bg-gray-800 shadow-lg hover:shadow-xl transition-shadow"
            >
              <div className="h-12 w-12 rounded-lg bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center mb-4">
                <feature.icon className="h-6 w-6 text-white" />
              </div>
              <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
              <p className="text-gray-600 dark:text-gray-300">{feature.description}</p>
            </div>
          ))}
        </div>

        <div className="mt-20 text-center">
          <h2 className="text-3xl font-bold mb-8">Why Choose NeuroLearn AI?</h2>
          <div className="grid md:grid-cols-2 gap-6 max-w-3xl mx-auto">
            {benefits.map((benefit, index) => (
              <div key={index} className="flex items-start space-x-3">
                <CheckCircle2 className="h-6 w-6 text-green-500 flex-shrink-0 mt-1" />
                <p className="text-left text-gray-700 dark:text-gray-300">{benefit}</p>
              </div>
            ))}
          </div>
        </div>
      </main>

      <footer className="border-t mt-20 py-8">
        <div className="container mx-auto px-6 text-center text-gray-600 dark:text-gray-400">
          <p>&copy; 2024 NeuroLearn AI. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}

const features = [
  {
    icon: Brain,
    title: "AI-Powered Tutoring",
    description: "Get personalized explanations and answers from advanced LLMs tailored to your learning style.",
  },
  {
    icon: BookOpen,
    title: "Smart Content Analysis",
    description: "Upload any document and let AI extract key concepts, generate summaries, and create quizzes.",
  },
  {
    icon: Target,
    title: "Performance Prediction",
    description: "LSTM models predict your learning outcomes and suggest optimal study schedules.",
  },
  {
    icon: MessageSquare,
    title: "Multimodal Learning",
    description: "Learn through text, voice, images, and documents with our advanced AI agents.",
  },
  {
    icon: Zap,
    title: "Instant Feedback",
    description: "Get real-time feedback on quizzes and assignments with detailed explanations.",
  },
  {
    icon: Brain,
    title: "Knowledge Graphs",
    description: "Visualize concept relationships and build a deeper understanding of subject matter.",
  },
];

const benefits = [
  "Personalized learning paths based on your strengths and weaknesses",
  "AI-generated quizzes from your uploaded content",
  "Spaced repetition for optimal memory retention",
  "Real-time progress tracking and analytics",
  "Multi-agent AI system for specialized assistance",
  "Support for multiple file formats and content types",
];
