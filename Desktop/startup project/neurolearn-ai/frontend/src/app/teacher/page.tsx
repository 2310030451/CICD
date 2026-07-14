"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { 
  BookOpen, Users, FileText, ClipboardCheck, 
  Calendar, TrendingUp, Plus, Loader2, 
  Brain, BarChart3
} from "lucide-react";

export default function TeacherPage() {
  const [courses, setCourses] = useState<any[]>([]);
  const [students, setStudents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("courses");

  useEffect(() => {
    fetchCourses();
    fetchStudents();
  }, []);

  const fetchCourses = async () => {
    try {
      const response = await fetch(${process.env.NEXT_PUBLIC_API_URL}/api/v1/teacher/courses, {
        headers: {
          Authorization: Bearer ,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setCourses(data);
      }
    } catch (error) {
      console.error("Failed to fetch courses:", error);
    } finally {
      setLoading(false);
    }
  };

  const fetchStudents = async () => {
    try {
      const response = await fetch(${process.env.NEXT_PUBLIC_API_URL}/api/v1/teacher/batches, {
        headers: {
          Authorization: Bearer ,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setStudents(data);
      }
    } catch (error) {
      console.error("Failed to fetch students:", error);
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
        <h1 className="text-3xl font-bold">Teacher Dashboard</h1>
        <p className="text-muted-foreground">Manage courses, students, and assignments</p>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList>
          <TabsTrigger value="courses">Courses</TabsTrigger>
          <TabsTrigger value="students">Students</TabsTrigger>
          <TabsTrigger value="assignments">Assignments</TabsTrigger>
          <TabsTrigger value="analytics">Analytics</TabsTrigger>
        </TabsList>

        <TabsContent value="courses" className="space-y-6">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-bold">My Courses</h2>
            <Button>
              <Plus className="w-4 h-4 mr-2" />
              Create Course
            </Button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {courses.map((course) => (
              <Card key={course.id}>
                <CardHeader>
                  <CardTitle>{course.title}</CardTitle>
                  <CardDescription>{course.subject} - {course.grade_level}</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>Students:</span>
                      <span>{course.enrolled_students?.length || 0}</span>
                    </div>
                    <Badge variant={course.status === "published" ? "default" : "secondary"}>
                      {course.status}
                    </Badge>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {courses.length === 0 && (
            <Card>
              <CardContent className="flex flex-col items-center justify-center py-12">
                <BookOpen className="w-12 h-12 text-muted-foreground mb-4" />
                <p className="text-muted-foreground">No courses yet. Create your first course to get started!</p>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        <TabsContent value="students" className="space-y-6">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-bold">Student Batches</h2>
            <Button>
              <Plus className="w-4 h-4 mr-2" />
              Create Batch
            </Button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {students.map((batch) => (
              <Card key={batch.id}>
                <CardHeader>
                  <CardTitle>{batch.name}</CardTitle>
                  <CardDescription>{batch.subject} - {batch.grade_level}</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>Students:</span>
                      <span>{batch.student_ids?.length || 0}</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {students.length === 0 && (
            <Card>
              <CardContent className="flex flex-col items-center justify-center py-12">
                <Users className="w-12 h-12 text-muted-foreground mb-4" />
                <p className="text-muted-foreground">No student batches yet. Create your first batch!</p>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        <TabsContent value="assignments" className="space-y-6">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-bold">Assignments</h2>
            <Button>
              <Plus className="w-4 h-4 mr-2" />
              Create Assignment
            </Button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <ClipboardCheck className="h-5 w-5" />
                  Manage Assignments
                </CardTitle>
                <CardDescription>Create and grade assignments</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">Assignment management features would be displayed here</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Brain className="h-5 w-5" />
                  AI Question Generator
                </CardTitle>
                <CardDescription>Generate questions using AI</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">AI-powered question generation would be displayed here</p>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="analytics" className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TrendingUp className="h-5 w-5" />
                  Class Performance
                </CardTitle>
                <CardDescription>Overall class statistics</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">Performance analytics would be displayed here</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Calendar className="h-5 w-5" />
                  Attendance
                </CardTitle>
                <CardDescription>Student attendance records</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">Attendance tracking would be displayed here</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <BarChart3 className="h-5 w-5" />
                  Progress Reports
                </CardTitle>
                <CardDescription>Student progress analysis</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">Progress reports would be displayed here</p>
              </CardContent>
            </Card>
          </div>

          <Card>
            <CardHeader>
              <CardTitle>AI Feedback</CardTitle>
              <CardDescription>AI-generated insights for student improvement</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">AI feedback and recommendations would be displayed here</p>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
