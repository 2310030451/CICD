"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { User, Brain, Clock, Target, BookOpen, TrendingUp, RefreshCw } from "lucide-react";

export default function DigitalTwinPage() {
  const [twin, setTwin] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDigitalTwin();
  }, []);

  const fetchDigitalTwin = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/digital-twin/`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setTwin(data);
      }
    } catch (error) {
      console.error("Failed to fetch digital twin:", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-muted rounded w-1/3" />
          <div className="h-4 bg-muted rounded w-1/2" />
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
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Digital Twin</h1>
          <p className="text-muted-foreground">Your AI-powered learning profile</p>
        </div>
        <Button onClick={fetchDigitalTwin}>
          <RefreshCw className="w-4 h-4 mr-2" />
          Refresh
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Brain className="h-5 w-5" />
              Learning Style
            </CardTitle>
            <CardDescription>Your preferred learning method</CardDescription>
          </CardHeader>
          <CardContent>
            <Badge className="text-lg px-3 py-1" variant="secondary">
              {twin?.learning_style || "mixed"}
            </Badge>
            <p className="text-sm text-muted-foreground mt-2">
              AI adapts content to match your style
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5" />
              Learning Speed
            </CardTitle>
            <CardDescription>Your learning pace</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold capitalize">{twin?.learning_speed || "moderate"}</div>
            <p className="text-sm text-muted-foreground">Content difficulty adjusted accordingly</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Clock className="h-5 w-5" />
              Attention Span
            </CardTitle>
            <CardDescription>Optimal session duration</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{twin?.attention_span_minutes || 30} min</div>
            <p className="text-sm text-muted-foreground">Recommended session length</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Target className="h-5 w-5" />
              Confidence Level
            </CardTitle>
            <CardDescription>Your self-assessed confidence</CardDescription>
          </CardHeader>
          <CardContent>
            <Progress value={(twin?.confidence_level || 0) * 100} className="h-3" />
            <p className="text-sm text-muted-foreground mt-2">{(twin?.confidence_level * 100)?.toFixed(0) || 0}% confidence</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <BookOpen className="h-5 w-5" />
              Memory Retention
            </CardTitle>
            <CardDescription>Information retention rate</CardDescription>
          </CardHeader>
          <CardContent>
            <Progress value={(twin?.memory_retention || 0) * 100} className="h-3" />
            <p className="text-sm text-muted-foreground mt-2">{(twin?.memory_retention * 100)?.toFixed(0) || 0}% retention</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Knowledge Gaps</CardTitle>
            <CardDescription>Areas needing improvement</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {twin?.knowledge_gaps?.slice(0, 5).
map((gap: any, index: number) => (
                <div key={index} className="flex items-center justify-between p-3 bg-muted rounded">
                  <span className="font-medium">{gap.topic}</span>
                  <Badge variant={gap.gap_severity === "high" ? "destructive" : "secondary"}>
                    {gap.gap_severity}
                  </Badge>
                </div>
              )) || <p className="text-muted-foreground">No knowledge gaps identified</p>}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Strengths</CardTitle>
            <CardDescription>Your strongest areas</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {twin?.strengths?.slice(0, 5).
map((strength: any, index: number) => (
                <div key={index} className="flex items-center justify-between p-3 bg-muted rounded">
                  <span className="font-medium">{strength.topic}</span>
                  <Badge variant="default">{strength.score?.toFixed(0)}%</Badge>
                </div>
              )) || <p className="text-muted-foreground">No strengths identified yet</p>}
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Study Preferences</CardTitle>
          <CardDescription>Your personalized learning preferences</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <p className="text-sm font-medium">Preferred Study Time</p>
              <p className="text-lg capitalize">{twin?.preferred_study_time || "flexible"}</p>
            </div>
            <div>
              <p className="text-sm font-medium">Last Updated</p>
              <p className="text-lg">{twin?.last_updated ? new Date(twin.last_updated).toLocaleDateString() : "N/A"}</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
