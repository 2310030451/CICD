"use client";

import { useState } from "react";
import { useAuth } from "@/lib/hooks/use-auth";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Switch } from "@/components/ui/switch";
import {
  Brain,
  User,
  Bell,
  Shield,
  Palette,
  Globe,
  Save,
  ArrowLeft,
  LogOut,
  Trash2,
} from "lucide-react";
import Link from "next/link";
import { useToast } from "@/components/ui/use-toast";
import { signOut } from "@/lib/firebase";

export default function SettingsPage() {
  const { user, isAuthenticated, isLoading } = useAuth();
  const router = useRouter();
  const { toast } = useToast();

  const [emailNotifications, setEmailNotifications] = useState(true);
  const [pushNotifications, setPushNotifications] = useState(true);
  const [studyReminders, setStudyReminders] = useState(true);
  const [dataSharing, setDataSharing] = useState(false);
  const [analytics, setAnalytics] = useState(true);

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push("/login");
    }
  }, [isAuthenticated, isLoading, router]);

  const handleSave = () => {
    toast({
      title: "Settings saved",
      description: "Your settings have been updated successfully",
    });
  };

  const handleLogout = async () => {
    try {
      await signOut();
      router.push("/login");
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Error",
        description: "Failed to sign out",
      });
    }
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

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <DashboardHeader />
      <main className="container mx-auto px-6 py-8">
        <div className="mb-6">
          <Link href="/dashboard">
            <Button variant="ghost" size="sm">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Dashboard
            </Button>
          </Link>
        </div>
        <h1 className="text-3xl font-bold mb-6">Settings</h1>
        <div className="grid lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            <ProfileSection user={user} />
            <NotificationSettings
              emailNotifications={emailNotifications}
              setEmailNotifications={setEmailNotifications}
              pushNotifications={pushNotifications}
              setPushNotifications={setPushNotifications}
              studyReminders={studyReminders}
              setStudyReminders={setStudyReminders}
            />
            <PrivacySettings
              dataSharing={dataSharing}
              setDataSharing={setDataSharing}
              analytics={analytics}
              setAnalytics={setAnalytics}
            />
            <AppearanceSettings />
          </div>
          <div className="space-y-6">
            <AccountActions handleLogout={handleLogout} />
            <DangerZone />
          </div>
        </div>
      </main>
    </div>
  );
}

function DashboardHeader() {
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
        </div>
      </div>
    </header>
  );
}

function ProfileSection({ user }: any) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <User className="h-5 w-5" />
          <span>Profile</span>
        </CardTitle>
        <CardDescription>Manage your account information</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="flex items-center space-x-4 mb-6">
          <Avatar className="h-16 w-16">
            <AvatarImage src={user?.photo_url} />
            <AvatarFallback className="text-xl">
              {user?.display_name?.charAt(0) || "U"}
            </AvatarFallback>
          </Avatar>
          <div>
            <h3 className="text-lg font-semibold">{user?.display_name || "User"}</h3>
            <p className="text-sm text-gray-500">{user?.email}</p>
          </div>
        </div>
        <div className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input id="email" value={user?.email || ""} disabled />
          </div>
          <div className="space-y-2">
            <Label htmlFor="name">Display Name</Label>
            <Input id="name" defaultValue={user?.display_name || ""} />
          </div>
          <Button onClick={() => {}}>
            <Save className="h-4 w-4 mr-2" />
            Save Changes
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}

function NotificationSettings({
  emailNotifications,
  setEmailNotifications,
  pushNotifications,
  setPushNotifications,
  studyReminders,
  setStudyReminders,
}: any) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <Bell className="h-5 w-5" />
          <span>Notifications</span>
        </CardTitle>
        <CardDescription>Manage your notification preferences</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <Label htmlFor="email-notif">Email Notifications</Label>
              <p className="text-sm text-gray-500">Receive updates via email</p>
            </div>
            <Switch
              id="email-notif"
              checked={emailNotifications}
              onCheckedChange={setEmailNotifications}
            />
          </div>
          <div className="flex items-center justify-between">
            <div>
              <Label htmlFor="push-notif">Push Notifications</Label>
              <p className="text-sm text-gray-500">Receive push notifications</p>
            </div>
            <Switch
              id="push-notif"
              checked={pushNotifications}
              onCheckedChange={setPushNotifications}
            />
          </div>
          <div className="flex items-center justify-between">
            <div>
              <Label htmlFor="study-reminders">Study Reminders</Label>
              <p className="text-sm text-gray-500">Get reminded to study</p>
            </div>
            <Switch
              id="study-reminders"
              checked={studyReminders}
              onCheckedChange={setStudyReminders}
            />
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

function PrivacySettings({
  dataSharing,
  setDataSharing,
  analytics,
  setAnalytics,
}: any) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <Shield className="h-5 w-5" />
          <span>Privacy & Security</span>
        </CardTitle>
        <CardDescription>Manage your privacy settings</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <Label htmlFor="data-sharing">Data Sharing</Label>
              <p className="text-sm text-gray-500">Share anonymous data for improvements</p>
            </div>
            <Switch
              id="data-sharing"
              checked={dataSharing}
              onCheckedChange={setDataSharing}
            />
          </div>
          <div className="flex items-center justify-between">
            <div>
              <Label htmlFor="analytics">Analytics</Label>
              <p className="text-sm text-gray-500">Allow usage analytics</p>
            </div>
            <Switch
              id="analytics"
              checked={analytics}
              onCheckedChange={setAnalytics}
            />
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

function AppearanceSettings() {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <Palette className="h-5 w-5" />
          <span>Appearance</span>
        </CardTitle>
        <CardDescription>Customize your experience</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="theme">Theme</Label>
            <select
              id="theme"
              className="w-full h-10 px-3 rounded-md border border-input bg-background"
            >
              <option value="system">System</option>
              <option value="light">Light</option>
              <option value="dark">Dark</option>
            </select>
          </div>
          <div className="space-y-2">
            <Label htmlFor="language">Language</Label>
            <select
              id="language"
              className="w-full h-10 px-3 rounded-md border border-input bg-background"
            >
              <option value="en">English</option>
              <option value="es">Spanish</option>
              <option value="fr">French</option>
              <option value="de">German</option>
            </select>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

function AccountActions({ handleLogout }: any) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Account Actions</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          <Button variant="outline" className="w-full" onClick={handleLogout}>
            <LogOut className="h-4 w-4 mr-2" />
            Sign Out
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}

function DangerZone() {
  return (
    <Card className="border-red-200 dark:border-red-900">
      <CardHeader>
        <CardTitle className="text-red-600">Danger Zone</CardTitle>
        <CardDescription>Irreversible account actions</CardDescription>
      </CardHeader>
      <CardContent>
        <Button variant="destructive" className="w-full">
          <Trash2 className="h-4 w-4 mr-2" />
          Delete Account
        </Button>
      </CardContent>
    </Card>
  );
}
