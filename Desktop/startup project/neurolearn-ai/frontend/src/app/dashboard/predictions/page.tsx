"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { Brain, TrendingUp, AlertTriangle, Target, Clock, RefreshCw, Loader2 } from "lucide-react";

export default function PredictionsPage() {
  const [prediction, setPrediction] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    fetchPrediction();
  }, []);

  const fetchPrediction = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/predictions/`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setPrediction(data[0]);
      }
    } catch (error) {
      console.error("Failed to fetch prediction:", error);
    } finally {
      setLoading(false);
    }
  };

  const generateNewPrediction = async () => {
    setGenerating(true);
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/predictions/generate`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setPrediction(data);
      }
    } catch (error) {
      console.error("Failed to generate prediction:", error);
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
          <h1 className="text-3xl font-bold">AI Predictions</h1>
          <p className="text-muted-foreground">LSTM-powered learning predictions and insights</p>
        </div>
        <div className="flex gap-2">
          <Button onClick={fetchPrediction} variant="outline">
            <RefreshCw className="w-4 h-4 mr-2" />
            Refresh
          </Button>
          <Button onClick={generateNewPrediction} disabled={generating}>
            {generating ? <Loader2 className="w-4 h-4 mr-2 animate-spin" /> : <Brain className="w-4 h-4 mr-2" />}
            Generate New
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Target className="h-5 w-5" />
              Expected Exam Score
            </CardTitle>
            <CardDescription>Based on your learning patterns</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-4xl font-bold mb-2">{prediction?.expected_exam_score?.toFixed(1) || 0}%</div>
            <Progress value={prediction?.expected_exam_score || 0} className="h-2" />
            <p className="text-sm text-muted-foreground mt-2">Confidence: {prediction?.confidence?.toFixed(2) || 0}</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AlertTriangle className="h-5 w-5" />
              Failing Risk
            </CardTitle>
            <CardDescription>Probability of failing</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-4xl font-bold mb-2">{(prediction?.failing_risk * 100)?.toFixed(1) || 0}%</div>
            <Progress value={(prediction?.failing_risk || 0) * 100} className="h-2" />
            <Badge variant={prediction?.failing_risk > 0.5 ? "destructive" : "default"} className="mt-2">
              {prediction?.failing_risk > 0.5 ? "High Risk" : "Low Risk"}
            </Badge>
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
            <div className="text-4xl font-bold mb-2 capitalize">{prediction?.learning_speed || "moderate"}</div>
            <p className="text-sm text-muted-foreground">Future Trend: {prediction?.future_trend || "stable"}</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Knowledge Analysis</CardTitle>
            <CardDescription>Your strengths and areas for improvement</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <div className="flex justify-between mb-1">
                <span className="text-sm font-medium">Strong Topics</span>
                <span className="text-sm">{prediction?.strong_topic_score?.toFixed(1) || 0}%</span>
              </div>
              <Progress value={prediction?.strong_topic_score || 0} className="h-2" />
            </div>
            <div>
              <div className="flex justify-between mb-1">
                <span className="text-sm font-medium">Weak Topics</span>
                <span className="text-sm">{prediction?.weak_topic_score?.toFixed(1) || 0}%</span>
              </div>
              <Progress value={prediction?.weak_topic_score || 0} className="h-2" />
            </div>
            <div>
              <div className="flex justify-between mb-1">
                <span className="text-sm font-medium">Forgetting Probability</span>
                <span className="text-sm">{(prediction?.forgetting_probability * 100)?.toFixed(1) || 0}%</span>
              </div>
              <Progress value={(prediction?.forgetting_probability || 0) * 100} className="h-2" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Clock className="h-5 w-5" />
              Recommended Revision Time
            </CardTitle>
            <CardDescription>Optimal revision duration</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-4xl font-bold mb-2">{prediction?.recommended_revision_time || 30} min</div>
            <p className="text-sm text-muted-foreground">Per revision session</p>
            <div className="mt-4 p-4 bg-muted rounded">
              <p className="text-sm">
                Based on your learning patterns, spending {prediction?.recommended_revision_time || 30} minutes per revision session is optimal for memory retention.
              </p>
            </div>
          </CardContent>
        </Card>
      </div>

      {prediction && (
        <Card>
          <CardHeader>
            <CardTitle>Prediction Details</CardTitle>
            <CardDescription>Last updated: {new Date(prediction.prediction_date).toLocaleString()}</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              This prediction is generated using an LSTM model trained on your learning history, including study duration, quiz scores, time per topic, and revision patterns.
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
