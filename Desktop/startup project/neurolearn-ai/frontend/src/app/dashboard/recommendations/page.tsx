"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Lightbulb, BookOpen, Clock, Target, TrendingUp, RefreshCw, Loader2 } from "lucide-react";

export default function RecommendationsPage() {
  const [recommendations, setRecommendations] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    fetchRecommendations();
  }, []);

  const fetchRecommendations = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/recommendations/`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setRecommendations(data[0]);
      }
    } catch (error) {
      console.error("Failed to fetch recommendations:", error);
    } finally {
      setLoading(false);
    }
  };

  const generateNewRecommendations = async () => {
    setGenerating(true);
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/recommendations/generate`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setRecommendations(data);
      }
    } catch (error) {
      console.error("Failed to generate recommendations:", error);
    } finally {
      setGenerating(false);
    }
  };

  if (loading) {
    return (
      <div className="p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-muted rounded w-1/3" />
          <div className="h-4 bg-muted rounded w-1/2" />
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {[1, 2].map((i) => (
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
          <h1 className="text-3xl font-bold">Personalized Recommendations</h1>
          <p className="text-muted-foreground">AI-powered learning suggestions based on your profile</p>
        </div>
        <div className="flex gap-2">
          <Button onClick={fetchRecommendations} variant="outline">
            <RefreshCw className="w-4 h-4 mr-2" />
            Refresh
          </Button>
          <Button onClick={generateNewRecommendations} disabled={generating}>
            {generating ? <Loader2 className="w-4 h-4 mr-2 animate-spin" /> : <Lightbulb className="w-4 h-4 mr-2" />}
            Generate New
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <BookOpen className="h-5 w-5" />
              Topics to Revise
            </CardTitle>
            <CardDescription>Priority topics based on your knowledge gaps</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {recommendations?.topics_to_revise?.slice(0, 5).
map((topic: any, index: number) => (
                <div key={index} className="flex items-center justify-between p-3 bg-muted rounded">
                  <div>
                    <p className="font-medium">{topic.topic}</p>
                    <p className="text-xs text-muted-foreground">{topic.reason}</p>
                  </div>
                  <Badge variant={topic.priority === "high" ? "destructive" : "secondary"}>
                    {topic.priority}
                  </Badge>
                </div>
              )) || <p className="text-muted-foreground">No recommendations available</p>}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Target className="h-5 w-5" />
              Practice Questions
            </CardTitle>
            <CardDescription>Recommended practice sessions</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {recommendations?.practice_questions?.slice(0, 5).
map((practice: any, index: number) => (
                <div key={index} className="flex items-center justify-between p-3 bg-muted rounded">
                  <div>
                    <p className="font-medium capitalize">{practice.type.replace("_", " ")}</p>
                    <p className="text-xs text-muted-foreground">{practice.reason}</p>
                  </div>
                  <Badge>{practice.difficulty}</Badge>
                </div>
              )) || <p className="text-muted-foreground">No practice recommendations</p>}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Clock className="h-5 w-5" />
              Study Schedule
            </CardTitle>
            <CardDescription>Personalized study schedule recommendations</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {recommendations?.study_schedule && Object.entries(recommendations.study_schedule).map(([key, value]: [string, any]) => (
                <div key={key} className="flex justify-between p-2 bg-muted rounded">
                  <span className="text-sm font-medium capitalize">{key.replace("_", " ")}</span>
                  <span className="text-sm">{value}</span>
                </div>
              )) || <p className="text-muted-foreground">No schedule recommendations</p>}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5" />
              Difficulty Adjustment
            </CardTitle>
            <CardDescription>Recommended difficulty progression</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {recommendations?.difficulty_adjustment && Object.entries(recommendations.difficulty_adjustment).map(([key, value]: [string, any]) => (
                <div key={key} className="flex justify-between p-2 bg-muted rounded">
                  <span className="text-sm font-medium capitalize">{key.replace("_", " ")}</span>
                  <span className="text-sm">{typeof value === "number" ? (value * 100).toFixed(0) + "%" : value}</span>
                </div>
              )) || <p className="text-muted-foreground">No difficulty recommendations</p>}
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Learning Resources</CardTitle>
          <CardDescription>Recommended resources based on your learning style</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {recommendations?.learning_resources?.slice(0, 6).
map((resource: any, index: number) => (
              <div key={index} className="flex items-center justify-between p-3 bg-muted rounded">
                <span className="font-mediumcapitalize">{resource.type}</span>
                <Badge variant={resource.recommended ? "default" : "secondary"}>
                  {resource.recommended ? "Recommended" : "Optional"}
                </Badge>
              </div>
            )) || <p className="text-muted-foreground">No resource recommendations</p>}
          </div>
        </CardContent>
      </Card>

      {recommendations && (
        <Card>
          <CardHeader>
            <CardTitle>Recommendation Details</CardTitle>
            <CardDescription>Generated: {new Date(recommendations.generated_at).toLocaleString()}</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-2">
              <Badge variant="outline">Confidence: {(recommendations.confidence * 100).toFixed(0)}%</Badge>
              <p className="text-sm text-muted-foreground">
                These recommendations are generated using your Digital Twin profile and learning history.
              </p>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
