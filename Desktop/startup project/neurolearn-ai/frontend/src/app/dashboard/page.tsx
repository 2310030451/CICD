"use client";

import { useAuth } from "@/lib/hooks/use-auth";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Progress } from "@/components/ui/progress";
import {
  Brain,
  Flame,
  Trophy,
  Calendar,
  Clock,
  BookOpen,
  MessageSquare,
  Target,
  TrendingUp,
  Zap,
  LogOut,
  Settings,
  Bell,
  Search,
  Plus,
  ArrowRight,
} from "lucide-react";
import Link from "next/link";

export default function DashboardPage() {
  const { isAuthenticated, isLoading, user } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push("/login");
    }
  }, [isAuthenticated, isLoading, router]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <DashboardHeader user={user} />
      <main className="container mx-auto px-6 py-8">
        <WelcomeSection user={user} />
        <QuickStats />
        <div className="grid lg:grid-cols-3 gap-6 mt-6">
          <div className="lg:col-span-2 space-y-6">
            <RecentActivity />
            <AIRecommendations />
          </div>
          <div className="space-y-6">
            <LearningProgress />
            <UpcomingTasks />
            <QuickActions />
          </div>
        </div>
      </main>
    </div>
  );
}

function DashboardHeader({ user }: { user: any }) {
  return (
    <header className="bg-white dark:bg-gray-800 border-b sticky top-0 z-10">
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Brain className="h-8 w-8 text-purple-600" />
            <span className="text-xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
              NeuroLearn AI
            </span>
          </div>
          <div className="flex items-center space-x-4">
            <Button variant="ghost" size="icon">
              <Search className="h-5 w-5" />
            </Button>
            <Button variant="ghost" size="icon">
              <Bell className="h-5 w-5" />
            </Button>
            <Link href="/dashboard/settings">
              <Button variant="ghost" size="icon">
                <Settings className="h-5 w-5" />
              </Button>
            </Link>
            <div className="flex items-center space-x-3">
              <Avatar>
                <AvatarImage src={user?.photo_url} />
                <AvatarFallback>{user?.display_name?.charAt(0) || "U"}</AvatarFallback>
              </Avatar>
              <div className="hidden md:block">
                <p className="text-sm font-medium">{user?.display_name || "User"}</p>
                <p className="text-xs text-gray-500">{user?.email}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}

function WelcomeSection({ user }: { user: any }) {
  const hours = new Date().getHours();
  let greeting = "Good morning";
  if (hours >= 12 && hours < 18) greeting = "Good afternoon";
  if (hours >= 18) greeting = "Good evening";

  return (
    <div className="mb-8">
      <h1 className="text-3xl font-bold mb-2">
        {greeting}, {user?.display_name?.split(" ")[0] || "User"}! 👋
      </h1>
      <p className="text-gray-600 dark:text-gray-400">
        Ready to continue your learning journey?
      </p>
    </div>
  );
}

function QuickStats() {
  const stats = [
    { icon: Trophy, label: "Total XP", value: "2,450", change: "+150", color: "text-yellow-500" },
    { icon: Flame, label: "Learning Streak", value: "12 days", change: "+2", color: "text-orange-500" },
    { icon: BookOpen, label: "Content Learned", value: "24", change: "+3", color: "text-blue-500" },
    { icon: Target, label: "Quiz Score Avg", value: "87%", change: "+5%", color: "text-green-500" },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {stats.map((stat, index) => (
        <Card key={index}>
          <CardContent className="p-6">
            <div className="flex items-center justify-between mb-2">
              <stat.icon className={`h-5 w-5 ${stat.color}`} />
              <span className="text-xs text-green-600 dark:text-green-400 font-medium">
                {stat.change}
              </span>
            </div>
            <p className="text-2xl font-bold">{stat.value}</p>
            <p className="text-sm text-gray-500">{stat.label}</p>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}

function RecentActivity() {
  const activities = [
    {
      icon: BookOpen,
      title: "Completed Machine Learning module",
      time: "2 hours ago",
      type: "learning",
    },
    {
      icon: Trophy,
      title: "Achieved 'Quick Learner' badge",
      time: "5 hours ago",
      type: "achievement",
    },
    {
      icon: MessageSquare,
      title: "Chat session with AI Tutor",
      time: "1 day ago",
      type: "chat",
    },
    {
      icon: Target,
      title: "Scored 95% on Python Quiz",
      time: "2 days ago",
      type: "quiz",
    },
  ];

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          Recent Activity
          <Button variant="ghost" size="sm">
            View All
            <ArrowRight className="h-4 w-4 ml-2" />
          </Button>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {activities.map((activity, index) => (
            <div key={index} className="flex items-start space-x-3">
              <div className="h-10 w-10 rounded-lg bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center flex-shrink-0">
                <activity.icon className="h-5 w-5 text-purple-600" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium">{activity.title}</p>
                <p className="text-xs text-gray-500">{activity.time}</p>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

function AIRecommendations() {
  const recommendations = [
    {
      title: "Review Neural Networks fundamentals",
      reason: "Based on your quiz performance",
      action: "Start Review",
      icon: Brain,
    },
    {
      title: "Complete Deep Learning module",
      reason: "Continue your learning path",
      action: "Continue",
      icon: BookOpen,
    },
    {
      title: "Practice Python coding problems",
      reason: "Improve your coding skills",
      action: "Practice",
      icon: Zap,
    },
  ];

  return (
    <Card>
      <CardHeader>
        <CardTitle>AI Recommendations</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {recommendations.map((rec, index) => (
            <div
              key={index}
              className="flex items-center justify-between p-3 rounded-lg bg-gray-50 dark:bg-gray-800"
            >
              <div className="flex items-center space-x-3">
                <div className="h-8 w-8 rounded-lg bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center">
                  <rec.icon className="h-4 w-4 text-blue-600" />
                </div>
                <div>
                  <p className="text-sm font-medium">{rec.title}</p>
                  <p className="text-xs text-gray-500">{rec.reason}</p>
                </div>
              </div>
              <Button variant="ghost" size="sm">
                {rec.action}
              </Button>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

function LearningProgress() {
  const subjects = [
    { name: "Machine Learning", progress: 75, color: "bg-purple-500" },
    { name: "Deep Learning", progress: 45, color: "bg-blue-500" },
    { name: "Python Programming", progress: 90, color: "bg-green-500" },
    { name: "Data Structures", progress: 60, color: "bg-orange-500" },
  ];

  return (
    <Card>
      <CardHeader>
        <CardTitle>Learning Progress</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {subjects.map((subject, index) => (
            <div key={index}>
              <div className="flex items-center justify-between mb-1">
                <span className="text-sm font-medium">{subject.name}</span>
                <span className="text-sm text-gray-500">{subject.progress}%</span>
              </div>
              <Progress value={subject.progress} className="h-2" />
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

function UpcomingTasks() {
  const tasks = [
    { title: "Complete CNN module", due: "Today", priority: "high" },
    { title: "Take LSTM quiz", due: "Tomorrow", priority: "medium" },
    { title: "Review flashcards", due: "In 2 days", priority: "low" },
  ];

  const priorityColors = {
    high: "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400",
    medium: "bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400",
    low: "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400",
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          Upcoming Tasks
          <Link href="/dashboard/planner">
            <Button variant="ghost" size="sm">
              Calendar
              <Calendar className="h-4 w-4 ml-2" />
            </Button>
          </Link>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {tasks.map((task, index) => (
            <div key={index} className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="h-2 w-2 rounded-full bg-purple-500" />
                <div>
                  <p className="text-sm font-medium">{task.title}</p>
                  <p className="text-xs text-gray-500 flex items-center">
                    <Clock className="h-3 w-3 mr-1" />
                    {task.due}
                  </p>
                </div>
              </div>
              <span
                className={`text-xs px-2 py-1 rounded-full ${priorityColors[task.priority as keyof typeof priorityColors]}`}
              >
                {task.priority}
              </span>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

function QuickActions() {
  const actions = [
    { icon: Plus, label: "Upload Content", href: "/dashboard/learn/upload", color: "bg-purple-500" },
    { icon: MessageSquare, label: "Chat with AI", href: "/dashboard/agents/tutor", color: "bg-blue-500" },
    { icon: Target, label: "Take Quiz", href: "/dashboard/quiz", color: "bg-green-500" },
    { icon: BookOpen, label: "Study Flashcards", href: "/dashboard/flashcards", color: "bg-orange-500" },
  ];

  return (
    <Card>
      <CardHeader>
        <CardTitle>Quick Actions</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 gap-3">
          {actions.map((action, index) => (
            <Link key={index} href={action.href}>
              <Button
                variant="outline"
                className="w-full h-20 flex flex-col items-center justify-center space-y-2"
              >
                <div className={`h-8 w-8 rounded-lg ${action.color} flex items-center justify-center`}>
                  <action.icon className="h-4 w-4 text-white" />
                </div>
                <span className="text-xs">{action.label}</span>
              </Button>
            </Link>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
