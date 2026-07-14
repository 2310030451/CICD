"use client";

import { useState } from "react";
import { useAuth } from "@/lib/hooks/use-auth";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Progress } from "@/components/ui/progress";
import {
  Brain,
  Trophy,
  Flame,
  BookOpen,
  Target,
  Calendar,
  MapPin,
  Link as LinkIcon,
  Mail,
  Save,
  Camera,
} from "lucide-react";
import { useToast } from "@/components/ui/use-toast";

export default function ProfilePage() {
  const { user, isAuthenticated, isLoading } = useAuth();
  const router = useRouter();
  const { toast } = useToast();

  const [isEditing, setIsEditing] = useState(false);
  const [displayName, setDisplayName] = useState(user?.display_name || "");
  const [bio, setBio] = useState("");

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push("/login");
    }
  }, [isAuthenticated, isLoading, router]);

  const handleSave = () => {
    setIsEditing(false);
    toast({
      title: "Profile updated",
      description: "Your profile has been updated successfully",
    });
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

  const achievements = [
    { icon: Trophy, title: "First Quiz", description: "Completed your first quiz", unlocked: true },
    { icon: Flame, title: "Week Streak", description: "7 days learning streak", unlocked: true },
    { icon: BookOpen, title: "Content Master", description: "Uploaded 10 documents", unlocked: false },
    { icon: Target, title: "Perfect Score", description: "100% on any quiz", unlocked: false },
  ];

  const stats = [
    { label: "Total XP", value: "2,450", icon: Trophy },
    { label: "Learning Streak", value: "12 days", icon: Flame },
    { label: "Content Learned", value: "24", icon: BookOpen },
    { label: "Quizzes Taken", value: "18", icon: Target },
  ];

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <DashboardHeader />
      <main className="container mx-auto px-6 py-8">
        <div className="grid lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            <ProfileCard
              user={user}
              isEditing={isEditing}
              displayName={displayName}
              setDisplayName={setDisplayName}
              bio={bio}
              setBio={setBio}
              setIsEditing={setIsEditing}
              handleSave={handleSave}
            />
            <LearningStats />
            <Achievements achievements={achievements} />
          </div>
          <div className="space-y-6">
            <QuickStats stats={stats} />
            <LearningProgress />
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
          <div className="flex items-center space-x-4">
            <Button variant="ghost" size="icon">
              <Calendar className="h-5 w-5" />
            </Button>
            <Button variant="ghost" size="icon">
              <Mail className="h-5 w-5" />
            </Button>
          </div>
        </div>
      </div>
    </header>
  );
}

function ProfileCard({
  user,
  isEditing,
  displayName,
  setDisplayName,
  bio,
  setBio,
  setIsEditing,
  handleSave,
}: any) {
  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle>Profile</CardTitle>
          {!isEditing ? (
            <Button variant="outline" size="sm" onClick={() => setIsEditing(true)}>
              Edit Profile
            </Button>
          ) : (
            <Button size="sm" onClick={handleSave}>
              <Save className="h-4 w-4 mr-2" />
              Save Changes
            </Button>
          )}
        </div>
      </CardHeader>
      <CardContent>
        <div className="flex items-start space-x-6">
          <div className="relative">
            <Avatar className="h-24 w-24">
              <AvatarImage src={user?.photo_url} />
              <AvatarFallback className="text-2xl">
                {user?.display_name?.charAt(0) || "U"}
              </AvatarFallback>
            </Avatar>
            {isEditing && (
              <Button
                size="icon"
                className="absolute bottom-0 right-0 h-8 w-8 rounded-full"
              >
                <Camera className="h-4 w-4" />
              </Button>
            )}
          </div>
          <div className="flex-1 space-y-4">
            {isEditing ? (
              <div className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="name">Display Name</Label>
                  <Input
                    id="name"
                    value={displayName}
                    onChange={(e) => setDisplayName(e.target.value)}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="bio">Bio</Label>
                  <Input
                    id="bio"
                    placeholder="Tell us about yourself..."
                    value={bio}
                    onChange={(e) => setBio(e.target.value)}
                  />
                </div>
              </div>
            ) : (
              <div>
                <h3 className="text-2xl font-bold">{user?.display_name || "User"}</h3>
                <p className="text-gray-500">{user?.email}</p>
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
                  {bio || "No bio yet. Add one to tell others about yourself!"}
                </p>
              </div>
            )}
            <div className="flex items-center space-x-4 text-sm text-gray-500">
              <div className="flex items-center space-x-1">
                <MapPin className="h-4 w-4" />
                <span>India</span>
              </div>
              <div className="flex items-center space-x-1">
                <Calendar className="h-4 w-4" />
                <span>Joined {new Date().toLocaleDateString()}</span>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

function LearningStats() {
  const stats = [
    { label: "Total Study Time", value: "45h 30m", icon: BookOpen },
    { label: "Sessions Completed", value: "32", icon: Target },
    { label: "Average Quiz Score", value: "87%", icon: Trophy },
    { label: "Concepts Learned", value: "156", icon: Brain },
  ];

  return (
    <Card>
      <CardHeader>
        <CardTitle>Learning Statistics</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {stats.map((stat, index) => (
            <div key={index} className="text-center p-4 rounded-lg bg-gray-50 dark:bg-gray-800">
              <stat.icon className="h-6 w-6 mx-auto mb-2 text-purple-600" />
              <p className="text-2xl font-bold">{stat.value}</p>
              <p className="text-sm text-gray-500">{stat.label}</p>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

function Achievements({ achievements }: any) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Achievements</CardTitle>
        <CardDescription>Your learning milestones</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 gap-4">
          {achievements.map((achievement: any, index: number) => (
            <div
              key={index}
              className={`p-4 rounded-lg border-2 ${
                achievement.unlocked
                  ? "border-purple-500 bg-purple-50 dark:bg-purple-900/20"
                  : "border-gray-200 dark:border-gray-700 opacity-50"
              }`}
            >
              <achievement.icon
                className={`h-8 w-8 mb-2 ${
                  achievement.unlocked ? "text-purple-600" : "text-gray-400"
                }`}
              />
              <h4 className="font-semibold">{achievement.title}</h4>
              <p className="text-sm text-gray-500">{achievement.description}</p>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

function QuickStats({ stats }: any) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Quick Stats</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {stats.map((stat: any, index: number) => (
            <div key={index} className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="h-10 w-10 rounded-lg bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center">
                  <stat.icon className="h-5 w-5 text-purple-600" />
                </div>
                <div>
                  <p className="text-sm font-medium">{stat.label}</p>
                  <p className="text-2xl font-bold">{stat.value}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

function LearningProgress() {
  const subjects = [
    { name: "Machine Learning", progress: 75 },
    { name: "Deep Learning", progress: 45 },
    { name: "Python Programming", progress: 90 },
    { name: "Data Structures", progress: 60 },
  ];

  return (
    <Card>
      <CardHeader>
        <CardTitle>Subject Progress</CardTitle>
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
