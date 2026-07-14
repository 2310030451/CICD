"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { 
  Users, TrendingUp, AlertCircle, Calendar, 
  Brain, Clock, Bell, Loader2, 
  BookOpen, Target
} from "lucide-react";

export default function ParentPage() {
  const [children, setChildren] = useState<any[]>([]);
  const [selectedChild, setSelectedChild] = useState<any>(null);
  const [progress, setProgress] = useState<any>(null);
  const [predictions, setPredictions] = useState<any>(null);
  const [notifications, setNotifications] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("overview");

  useEffect(() => {
    fetchChildren();
    fetchNotifications();
  }, []);

  useEffect(() => {
    if (selectedChild) {
      fetchChildProgress();
      fetchChildPredictions();
    }
  }, [selectedChild]);

  const fetchChildren = async () => {
    try {
      const response = await fetch(${process.env.NEXT_PUBLIC_API_URL}/api/v1/parent/children, {
        headers: {
          Authorization: Bearer ,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setChildren(data);
        if (data.length > 0) {
          setSelectedChild(data[0]);
        }
      }
    } catch (error) {
      console.error("Failed to fetch children:", error);
    } finally {
      setLoading(false);
    }
  };

  const fetchChildProgress = async () => {
    if (!selectedChild) return;
    try {
      const response = await fetch(${process.env.NEXT_PUBLIC_API_URL}/api/v1/parent/child//progress, {
        headers: {
          Authorization: Bearer ,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setProgress(data);
      }
    } catch (error) {
      console.error("Failed to fetch child progress:", error);
    }
  };

  const fetchChildPredictions = async () => {
    if (!selectedChild) return;
    try {
      const response = await fetch(${process.env.NEXT_PUBLIC_API_URL}/api/v1/parent/child//predictions, {
        headers: {
          Authorization: Bearer ,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setPredictions(data[0]);
      }
    } catch (error) {
      console.error("Failed to fetch child predictions:", error);
    }
  };

  const fetchNotifications = async () => {
    try {
      const response = await fetch(${process.env.NEXT_PUBLIC_API_URL}/api/v1/parent/notifications, {
        headers: {
          Authorization: Bearer ,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setNotifications(data);
      }
    } catch (error) {
      console.error("Failed to fetch notifications:", error);
    }
  };

  if (loading) {
    return (
      <div className="p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-muted rounded w-1/3" />
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="h-48 bg-muted rounded" />
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Parent Dashboard</h1>
        <p className="text-muted-foreground">Monitor your child's learning progress</p>
      </div>

      {/* Child Selection */}
      {children.length > 0 && (
        <div className="flex gap-2">
          {children.map((child) => (
            <Button
              key={child.id}
              variant={selectedChild?.id === child.id ? "default" : "outline"}
              onClick={() => setSelectedChild(child)}
            >
              {child.name || child.email}
            </Button>
          ))}
        </div>
      )}

      {children.length === 0 && (
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-12">
            <Users className="w-12 h-12 text-muted-foreground mb-4" />
            <p className="text-muted-foreground">No children linked yet. Link your child's account to get started!</p>
          </CardContent>
        </Card>
      )}

      {selectedChild && (
        <Tabs value={activeTab} onValueChange={setActiveTab}>
          <TabsList>
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="progress">Progress</TabsTrigger>
            <TabsTrigger value="predictions">Predictions</TabsTrigger>
            <TabsTrigger value="calendar">Calendar</TabsTrigger>
            <TabsTrigger value="notifications">Notifications</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <TrendingUp className="h-5 w-5" />
                    Study Hours
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold">{progress?.study_hours || 0}h</div>
                  <p className="text-sm text-muted-foreground">This month</p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Target className="h-5 w-5" />
                    Average Score
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold">{progress?.average_score || 0}%</div>
                  <p className="text-sm text-muted-foreground">Overall performance</p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Clock className="h-5 w-5" />
                    Attendance
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold">{progress?.attendance_percentage || 0}%</div>
                  <p className="text-sm text-muted-foreground">This month</p>
                </CardContent>
              </Card>
            </div>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Brain className="h-5 w-5" />
                  AI Suggestions
                </CardTitle>
                <CardDescription>Personalized recommendations for improvement</CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2">
                  {progress?.ai_suggestions?.map((suggestion: string, index: number) => (
                    <li key={index} className="flex items-start gap-2 text-sm">
                      <Badge variant="outline" className="mt-0.5">AI</Badge>
                      {suggestion}
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="progress" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Weak Subjects</CardTitle>
                <CardDescription>Areas needing attention</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {progress?.weak_subjects?.map((subject: string, index: number) => (
                    <Badge key={index} variant="destructive">
                      <AlertCircle className="w-3 h-3 mr-1" />
                      {subject}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Strong Subjects</CardTitle>
                <CardDescription>Areas of strength</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {progress?.strong_subjects?.map((subject: string, index: number) => (
                    <Badge key={index} variant="default">
                      <TrendingUp className="w-3 h-3 mr-1" />
                      {subject}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="predictions" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Exam Predictions</CardTitle>
                <CardDescription>AI-powered performance forecasts</CardDescription>
              </CardHeader>
              <CardContent>
                {predictions ? (
                  <div className="space-y-4">
                    <div>
                      <p className="text-sm text-muted-foreground">Expected Score</p>
                      <p className="text-3xl font-bold">{predictions.expected_score || 75}%</p>
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground">Failing Risk</p>
                      <Badge variant={predictions.failing_risk > 50 ? "destructive" : "default"}>
                        {predictions.failing_risk || 20}%
                      </Badge>
                    </div>
                  </div>
                ) : (
                  <p className="text-muted-foreground">No predictions available yet</p>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="calendar" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Calendar className="h-5 w-5" />
                  Revision Calendar
                </CardTitle>
                <CardDescription>Scheduled revision sessions</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">Revision calendar would be displayed here</p>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="notifications" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Bell className="h-5 w-5" />
                  Notifications
                </CardTitle>
                <CardDescription>Updates and alerts</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {notifications.map((notification) => (
                    <div key={notification.id} className={p-4 border rounded }>
                      <div className="flex justify-between items-start">
                        <div>
                          <p className="font-medium">{notification.title}</p>
                          <p className="text-sm text-muted-foreground">{notification.message}</p>
                        </div>
                        <Badge variant={notification.is_read ? "secondary" : "default"}>
                          {notification.type}
                        </Badge>
                      </div>
                    </div>
                  ))}
                </div>
                {notifications.length === 0 && (
                  <p className="text-muted-foreground">No notifications</p>
                )}
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      )}
    </div>
  );
}
