"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Bot, MessageSquare, BookOpen, Calendar, Code, FileText, Briefcase, BarChart3, Send, Loader2 } from "lucide-react";

const AGENTS = [
  { name: "tutor", role: "Explains concepts", icon: MessageSquare, color: "bg-blue-500" },
  { name: "quiz", role: "Creates quizzes", icon: BookOpen, color: "bg-green-500" },
  { name: "planner", role: "Study schedules", icon: Calendar, color: "bg-purple-500" },
  { name: "revision", role: "Revision plans", icon: FileText, color: "bg-orange-500" },
  { name: "coding", role: "Code mentor", icon: Code, color: "bg-cyan-500" },
  { name: "research", role: "Research assistant", icon: FileText, color: "bg-pink-500" },
  { name: "career", role: "Career advisor", icon: Briefcase, color: "bg-yellow-500" },
  { name: "analytics", role: "Learning analytics", icon: BarChart3, color: "bg-red-500" },
];

export default function AgentsPage() {
  const [selectedAgent, setSelectedAgent] = useState<string | null>(null);
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [agentStats, setAgentStats] = useState<any>(null);

  useEffect(() => {
    fetchAgentStats();
  }, []);

  const fetchAgentStats = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/agents/agents`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setAgentStats(data.agents);
      }
    } catch (error) {
      console.error("Failed to fetch agent stats:", error);
    }
  };

  const sendMessage = async () => {
    if (!selectedAgent || !message.trim()) return;

    setLoading(true);
    setResponse("");

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/agents/execute/${selectedAgent}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify({ question: message }),
      });

      if (response.ok) {
        const data = await response.json();
        setResponse(data.response || data.primary_response || JSON.stringify(data));
      } else {
        setResponse("Failed to get response from agent.");
      }
    } catch (error) {
      setResponse("Error communicating with agent.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">AI Agents</h1>
          <p className="text-muted-foreground">Specialized AI assistants for your learning journey</p>
        </div>
      </div>

      <Tabs defaultValue="chat" className="space-y-6">
        <TabsList>
          <TabsTrigger value="chat">Chat with Agents</TabsTrigger>
          <TabsTrigger value="explore">Explore Agents</TabsTrigger>
        </TabsList>

        <TabsContent value="chat" className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Select Agent</CardTitle>
                <CardDescription>Choose an AI agent to assist you</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-3">
                  {AGENTS.map((agent) => {
                    const Icon = agent.icon;
                    return (
                      <button
                        key={agent.name}
                        onClick={() => setSelectedAgent(agent.name)}
                        className={`p-4 rounded-lg border-2 transition-all ${
                          selectedAgent === agent.name
                            ? "border-primary bg-primary/10"
                            : "border-border hover:border-primary/50"
                        }`}
                      >
                        <div className="flex items-center gap-3">
                          <div className={`p-2 rounded-lg ${agent.color}`}>
                            <Icon className="w-5 h-5 text-white" />
                          </div>
                          <div className="text-left">
                            <p className="font-semibold capitalize">{agent.name}</p>
                            <p className="text-xs text-muted-foreground">{agent.role}</p>
                          </div>
                        </div>
                      </button>
                    );
                  })}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Conversation</CardTitle>
                <CardDescription>
                  {selectedAgent ? `Chat with ${selectedAgent} agent` : "Select an agent to start chatting"}
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {selectedAgent && (
                  <>
                    <div className="min-h-[200px] p-4 rounded-lg bg-muted/50">
                      {response ? (
                        <p className="text-sm whitespace-pre-wrap">{response}</p>
                      ) : (
                        <p className="text-sm text-muted-foreground">
                          Start a conversation with the {selectedAgent} agent...
                        </p>
                      )}
                    </div>
                    <div className="flex gap-2">
                      <Textarea
                        placeholder="Type your message..."
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                        className="flex-1"
                        onKeyDown={(e) => {
                          if (e.key === "Enter" && !e.shiftKey) {
                            e.preventDefault();
                            sendMessage();
                          }
                        }}
                      />
                      <Button onClick={sendMessage} disabled={loading}>
                        {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
                      </Button>
                    </div>
                  </>
                )}
                {!selectedAgent && (
                  <div className="flex items-center justify-center h-[250px] text-muted-foreground">
                    <div className="text-center">
                      <Bot className="w-12 h-12 mx-auto mb-2 opacity-50" />
                      <p>Select an agent to start chatting</p>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="explore" className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {AGENTS.map((agent) => {
              const Icon = agent.icon;
              const stats = agentStats?.find((a: any) => a.name === agent.name);
              return (
                <Card key={agent.name} className="hover:shadow-lg transition-shadow">
                  <CardHeader>
                    <div className={`w-12 h-12 rounded-lg ${agent.color} flex items-center justify-center mb-3`}>
                      <Icon className="w-6 h-6 text-white" />
                    </div>
                    <CardTitle className="capitalize">{agent.name}</CardTitle>
                    <CardDescription>{agent.role}</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">Memory Size:</span>
                        <span>{stats?.stats?.memory_size || 0}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">Tools:</span>
                        <span>{stats?.stats?.tools_count || 0}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">Status:</span>
                        <Badge variant="outline" className="text-green-600">
                          Active
                        </Badge>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
