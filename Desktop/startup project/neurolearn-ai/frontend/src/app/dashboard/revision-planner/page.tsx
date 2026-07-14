"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { RefreshCw, Plus, Trash2, Edit, Clock, Target } from "lucide-react";

export default function RevisionPlannerPage() {
  const [plans, setPlans] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    subjects: "",
    daily_hours: "2",
    goals: "",
  });

  useEffect(() => {
    fetchPlans();
  }, []);

  const fetchPlans = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/revision-planner/`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setPlans(data);
      }
    } catch (error) {
      console.error("Failed to fetch revision plans:", error);
    } finally {
      setLoading(false);
    }
  };

  const createPlan = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/revision-planner/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify({
          title: formData.title,
          description: formData.description,
          subjects: formData.subjects.split(",").map((s) => s.trim()),
          daily_hours: parseFloat(formData.daily_hours),
          goals: formData.goals.split("\n").filter((g) => g.trim()),
          start_date: new Date().toISOString(),
          end_date: new Date(Date.now() + 14 * 24 * 60 * 60 * 1000).toISOString(),
        }),
      });
      if (response.ok) {
        setShowCreate(false);
        setFormData({ title: "", description: "", subjects: "", daily_hours: "2", goals: "" });
        fetchPlans();
      }
    } catch (error) {
      console.error("Failed to create revision plan:", error);
    }
  };

  const deletePlan = async (planId: string) => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/revision-planner/${planId}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      if (response.ok) {
        fetchPlans();
      }
    } catch (error) {
      console.error("Failed to delete revision plan:", error);
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
          <h1 className="text-3xl font-bold">Revision Planner</h1>
          <p className="text-muted-foreground">Create effective revision plans with spaced repetition</p>
        </div>
        <Button onClick={() => setShowCreate(true)}>
          <Plus className="w-4 h-4 mr-2" />
          Create Plan
        </Button>
      </div>

      {showCreate && (
        <Card>
          <CardHeader>
            <CardTitle>Create New Revision Plan</CardTitle>
            <CardDescription>Set up your spaced repetition revision schedule</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="text-sm font-medium">Title</label>
              <Input
                placeholder="e.g., Final Exam Revision"
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              />
            </div>
            <div>
              <label className="text-sm font-medium">Description</label>
              <Textarea
                placeholder="Describe your revision plan"
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              />
            </div>
            <div>
              <label className="text-sm font-medium">Subjects to Revise (comma-separated)</label>
              <Input
                placeholder="e.g., Math, Physics, Chemistry"
                value={formData.subjects}
                onChange={(e) => setFormData({ ...formData, subjects: e.target.value })}
              />
            </div>
            <div>
              <label className="text-sm font-medium">Daily Revision Hours</label>
              <Input
                type="number"
                placeholder="2"
                value={formData.daily_hours}
                onChange={(e) => setFormData({ ...formData, daily_hours: e.target.value })}
              />
            </div>
            <div>
              <label className="text-sm font-medium">Revision Goals (one per line)</label>
              <Textarea
                placeholder="Review chapter 1-5&#10;Solve past papers&#10;Memorize formulas"
                value={formData.goals}
                onChange={(e) => setFormData({ ...formData, goals: e.target.value })}
              />
            </div>
            <div className="flex gap-2">
              <Button onClick={createPlan}>Create Plan</Button>
              <Button variant="outline" onClick={() => setShowCreate(false)}>
                Cancel
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {plans.map((plan) => (
          <Card key={plan._id}>
            <CardHeader>
              <div className="flex items-start justify-between">
                <div>
                  <CardTitle>{plan.title}</CardTitle>
                  <CardDescription>{plan.description}</CardDescription>
                </div>
                <Badge variant={plan.status === "active" ? "default" : "secondary"}>
                  {plan.status}
                </Badge>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <p className="text-sm font-medium">Subjects to Revise</p>
                <div className="flex flex-wrap gap-2 mt-1">
                  {plan.subjects?.map((subject: string, index: number) => (
                    <Badge key={index} variant="outline">
                      {subject}
                    </Badge>
                  ))}
                </div>
              </div>
              <div>
                <p className="text-sm font-medium">Daily Revision Hours</p>
                <p className="text-sm">{plan.daily_hours} hours</p>
              </div>
              <div>
                <p className="text-sm font-medium">Revision Goals</p>
                <ul className="text-sm list-disc list-inside mt-1">
                  {plan.goals?.slice(0, 3).
map((goal: string, index: number) => (
                    <li key={index}>{goal}</li>
                  ))}
                </ul>
              </div>
              <div className="flex gap-2">
                <Button variant="outline" size="sm">
                  <Edit className="w-4 h-4 mr-2" />
                  Edit
                </Button>
                <Button variant="destructive" size="sm" onClick={() => deletePlan(plan._id)}>
                  <Trash2 className="w-4 h-4 mr-2" />
                  Delete
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {plans.length === 0 && !showCreate && (
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-12">
            <RefreshCw className="w-12 h-12 text-muted-foreground mb-4" />
            <p className="text-muted-foreground">No revision plans yet. Create your first plan to start effective revision!</p>
          </CardContent>
        </Card>
      )}

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Clock className="h-5 w-5" />
            Spaced Repetition Tips
          </CardTitle>
          <CardDescription>Optimize your revision with these techniques</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 bg-muted rounded">
              <Target className="h-6 w-6 mb-2" />
              <p className="font-medium">Review at Intervals</p>
              <p className="text-sm text-muted-foreground">Review material at increasing intervals (1, 3, 7, 14 days)</p>
            </div>
            <div className="p-4 bg-muted rounded">
              <Clock className="h-6 w-6 mb-2" />
              <p className="font-medium">Active Recall</p>
              <p className="text-sm text-muted-foreground">Test yourself instead of just re-reading notes</p>
            </div>
            <div className="p-4 bg-muted rounded">
              <RefreshCw className="h-6 w-6 mb-2" />
              <p className="font-medium">Mix Topics</p>
              <p className="text-sm text-muted-foreground">Interleave different subjects for better retention</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
