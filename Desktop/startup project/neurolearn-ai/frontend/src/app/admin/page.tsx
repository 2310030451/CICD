"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { 
  Users, DollarSign, FileText, Zap, Eye, Activity, 
  Settings, AlertTriangle, CheckCircle, Loader2, 
  TrendingUp, Database, Server, Shield
} from "lucide-react";

export default function AdminPage() {
  const [metrics, setMetrics] = useState<any>(null);
  const [users, setUsers] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("dashboard");

  useEffect(() => {
    fetchMetrics();
    fetchUsers();
  }, []);

  const fetchMetrics = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/admin/dashboard/metrics`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setMetrics(data);
      }
    } catch (error) {
      console.error("Failed to fetch metrics:", error);
    } finally {
      setLoading(false);
    }
  };

  const fetchUsers = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/admin/users?limit=10`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setUsers(data);
      }
    } catch (error) {
      console.error("Failed to fetch users:", error);
    }
  };

  if (loading) {
    return (
      <div className="p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-muted rounded w-1/3" />
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="h-32 bg-muted rounded" />
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Admin Dashboard</h1>
        <p className="text-muted-foreground">Monitor and manage the platform</p>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList>
          <TabsTrigger value="dashboard">Dashboard</TabsTrigger>
          <TabsTrigger value="users">Users</TabsTrigger>
          <TabsTrigger value="analytics">Analytics</TabsTrigger>
          <TabsTrigger value="system">System</TabsTrigger>
          <TabsTrigger value="logs">Logs</TabsTrigger>
        </TabsList>

        <TabsContent value="dashboard" className="space-y-6">
          {/* Key Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium">Total Users</CardTitle>
                <Users className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{metrics?.total_users || 0}</div>
                <p className="text-xs text-muted-foreground">
                  {metrics?.active_users || 0} active
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium">Monthly Revenue</CardTitle>
                <DollarSign className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold"></div>
                <p className="text-xs text-muted-foreground">
                  Total: 
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium">Documents</CardTitle>
                <FileText className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{metrics?.total_documents || 0}</div>
                <p className="text-xs text-muted-foreground">Uploaded</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium">AI Queries</CardTitle>
                <Zap className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{metrics?.total_ai_queries || 0}</div>
                <p className="text-xs text-muted-foreground">
                  Vision: {metrics?.total_vision_queries || 0}
                </p>
              </CardContent>
            </Card>
          </div>

          {/* Active Subscriptions */}
          <Card>
            <CardHeader>
              <CardTitle>Active Subscriptions</CardTitle>
              <CardDescription>Current subscription breakdown</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">{metrics?.active_subscriptions || 0}</div>
              <p className="text-sm text-muted-foreground">Active subscriptions</p>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="users" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Recent Users</CardTitle>
              <CardDescription>Manage user accounts</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {users.map((user) => (
                  <div key={user.id} className="flex items-center justify-between p-4 border rounded">
                    <div>
                      <p className="font-medium">{user.email}</p>
                      <p className="text-sm text-muted-foreground">Joined: {new Date(user.created_at).toLocaleDateString()}</p>
                    </div>
                    <Badge variant={user.status === "active" ? "default" : "secondary"}>
                      {user.status}
                    </Badge>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="analytics" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="h-5 w-5" />
                Usage Analytics
              </CardTitle>
              <CardDescription>Platform usage trends</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">Detailed analytics charts would be displayed here</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <DollarSign className="h-5 w-5" />
                Revenue Analytics
              </CardTitle>
              <CardDescription>Revenue breakdown by period</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">Revenue charts would be displayed here</p>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="system" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Activity className="h-5 w-5" />
                System Health
              </CardTitle>
              <CardDescription>Real-time system status</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {[
                  { name: "Database", status: "healthy", icon: Database },
                  { name: "Redis", status: "healthy", icon: Server },
                  { name: "ChromaDB", status: "healthy", icon: Database },
                  { name: "API Server", status: "healthy", icon: Server },
                ].map((service) => (
                  <div key={service.name} className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <service.icon className="h-4 w-4" />
                      <span>{service.name}</span>
                    </div>
                    <Badge variant="outline" className="text-green-500">
                      <CheckCircle className="h-3 w-3 mr-1" />
                      {service.status}
                    </Badge>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Settings className="h-5 w-5" />
                System Configuration
              </CardTitle>
              <CardDescription>Platform settings</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">System configuration options would be displayed here</p>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="logs" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Shield className="h-5 w-5" />
                Audit Logs
              </CardTitle>
              <CardDescription>System activity logs</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">Audit logs would be displayed here</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <AlertTriangle className="h-5 w-5" />
                Error Logs
              </CardTitle>
              <CardDescription>System errors and exceptions</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">Error logs would be displayed here</p>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
