"use client";

import { useState } from "react";
import { useAuth } from "@/lib/hooks/use-auth";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import {
  Brain,
  Bell,
  Check,
  Trophy,
  BookOpen,
  MessageSquare,
  Target,
  Trash2,
  ArrowLeft,
  CheckCheck,
} from "lucide-react";
import Link from "next/link";
import { formatRelativeTime } from "@/lib/utils";

export default function NotificationsPage() {
  const { isAuthenticated, isLoading, user } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push("/login");
    }
  }, [isAuthenticated, isLoading, router]);

  const [notifications, setNotifications] = useState([
    {
      id: 1,
      type: "success",
      title: "Quiz Completed",
      message: "You scored 95% on the Machine Learning quiz",
      time: new Date(Date.now() - 1000 * 60 * 30),
      read: false,
      icon: Trophy,
    },
    {
      id: 2,
      type: "info",
      title: "New Content Available",
      message: "Deep Learning module is now available for learning",
      time: new Date(Date.now() - 1000 * 60 * 60 * 2),
      read: false,
      icon: BookOpen,
    },
    {
      id: 3,
      type: "info",
      title: "AI Recommendation",
      message: "Review Neural Networks fundamentals based on your performance",
      time: new Date(Date.now() - 1000 * 60 * 60 * 5),
      read: true,
      icon: Brain,
    },
    {
      id: 4,
      type: "success",
      title: "Achievement Unlocked",
      message: "You've earned the 'Week Streak' badge",
      time: new Date(Date.now() - 1000 * 60 * 60 * 24),
      read: true,
      icon: Trophy,
    },
    {
      id: 5,
      type: "info",
      title: "Study Reminder",
      message: "Time for your daily study session",
      time: new Date(Date.now() - 1000 * 60 * 60 * 48),
      read: true,
      icon: Bell,
    },
  ]);

  const markAsRead = (id: number) => {
    setNotifications(
      notifications.map((notif) =>
        notif.id === id ? { ...notif, read: true } : notif
      )
    );
  };

  const markAllAsRead = () => {
    setNotifications(notifications.map((notif) => ({ ...notif, read: true })));
  };

  const deleteNotification = (id: number) => {
    setNotifications(notifications.filter((notif) => notif.id !== id));
  };

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

  const unreadCount = notifications.filter((n) => !n.read).length;

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <DashboardHeader user={user} />
      <main className="container mx-auto px-6 py-8">
        <div className="mb-6">
          <Link href="/dashboard">
            <Button variant="ghost" size="sm">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Dashboard
            </Button>
          </Link>
        </div>
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-3xl font-bold mb-2">Notifications</h1>
            <p className="text-gray-500">
              {unreadCount > 0 ? `${unreadCount} unread notifications` : "All caught up!"}
            </p>
          </div>
          {unreadCount > 0 && (
            <Button variant="outline" onClick={markAllAsRead}>
              <CheckCheck className="h-4 w-4 mr-2" />
              Mark All as Read
            </Button>
          )}
        </div>
        <div className="space-y-4">
          {notifications.length === 0 ? (
            <Card>
              <CardContent className="flex flex-col items-center justify-center py-12">
                <Bell className="h-12 w-12 text-gray-400 mb-4" />
                <h3 className="text-lg font-semibold mb-2">No notifications</h3>
                <p className="text-gray-500">You're all caught up!</p>
              </CardContent>
            </Card>
          ) : (
            notifications.map((notification) => (
              <NotificationCard
                key={notification.id}
                notification={notification}
                onMarkAsRead={markAsRead}
                onDelete={deleteNotification}
              />
            ))
          )}
        </div>
      </main>
    </div>
  );
}

function DashboardHeader({ user }: any) {
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
            <Avatar>
              <AvatarImage src={user?.photo_url} />
              <AvatarFallback>{user?.display_name?.charAt(0) || "U"}</AvatarFallback>
            </Avatar>
          </div>
        </div>
      </div>
    </header>
  );
}

function NotificationCard({
  notification,
  onMarkAsRead,
  onDelete,
}: any) {
  const typeColors = {
    success: "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400",
    info: "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400",
    warning: "bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400",
    error: "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400",
  };

  return (
    <Card
      className={`transition-all hover:shadow-md ${
        !notification.read ? "border-l-4 border-l-purple-500" : ""
      }`}
    >
      <CardContent className="p-6">
        <div className="flex items-start space-x-4">
          <div
            className={`h-10 w-10 rounded-lg flex items-center justify-center flex-shrink-0 ${
              typeColors[notification.type as keyof typeof typeColors]
            }`}
          >
            <notification.icon className="h-5 w-5" />
          </div>
          <div className="flex-1 min-w-0">
            <div className="flex items-center justify-between mb-1">
              <h3 className="font-semibold">{notification.title}</h3>
              <span className="text-xs text-gray-500">
                {formatRelativeTime(notification.time)}
              </span>
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
              {notification.message}
            </p>
            <div className="flex items-center space-x-2">
              {!notification.read && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => onMarkAsRead(notification.id)}
                >
                  <Check className="h-4 w-4 mr-2" />
                  Mark as Read
                </Button>
              )}
              <Button
                variant="ghost"
                size="sm"
                onClick={() => onDelete(notification.id)}
              >
                <Trash2 className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
