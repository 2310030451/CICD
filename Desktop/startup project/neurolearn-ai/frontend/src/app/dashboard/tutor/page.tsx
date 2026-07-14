"use client";

import { useState, useRef, useEffect } from "react";
import { useAuth } from "@/lib/hooks/use-auth";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Send, FileText, BookOpen, MessageSquare, Trash2, Plus } from "lucide-react";
import { toast } from "@/components/ui/use-toast";

interface Message {
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
}

interface Source {
  content: string;
  metadata: {
    document_id: string;
    title: string;
    chunk_index: number;
    subject?: string;
  };
  score: number;
}

interface Document {
  id: string;
  title: string;
  file_name: string;
  status: string;
}

export default function TutorPage() {
  const { user } = useAuth();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [streaming, setStreaming] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [documents, setDocuments] = useState<Document[]>([]);
  const [selectedDocuments, setSelectedDocuments] = useState<string[]>([]);
  const [showSources, setShowSources] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  useEffect(() => {
    loadDocuments();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, streaming]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const loadDocuments = async () => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/documents/`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        const completedDocs = data.filter((doc: Document) => doc.status === "completed");
        setDocuments(completedDocs);
      }
    } catch (error) {
      console.error("Failed to load documents:", error);
    }
  };

  const toggleDocumentSelection = (documentId: string) => {
    setSelectedDocuments((prev) =>
      prev.includes(documentId)
        ? prev.filter((id) => id !== documentId)
        : [...prev, documentId]
    );
  };

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage: Message = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);
    setStreaming(true);

    try {
      const token = localStorage.getItem("access_token");
      abortControllerRef.current = new AbortController();

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/ai/chat/stream`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            question: input,
            conversation_id: conversationId,
            document_ids: selectedDocuments.length > 0 ? selectedDocuments : undefined,
          }),
          signal: abortControllerRef.current.signal,
        }
      );

      if (!response.ok) {
        throw new Error("Chat request failed");
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      let assistantMessage = "";

      if (reader) {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value);
          assistantMessage += chunk;

          setMessages((prev) => {
            const newMessages = [...prev];
            const lastMessage = newMessages[newMessages.length - 1];
            if (lastMessage && lastMessage.role === "assistant") {
              lastMessage.content = assistantMessage;
            } else {
              newMessages.push({ role: "assistant", content: assistantMessage });
            }
            return newMessages;
          });
        }
      }

      setStreaming(false);
      setLoading(false);

      const chatResponse = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/ai/conversations/${conversationId}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (chatResponse.ok) {
        const conversationData = await chatResponse.json();
        setConversationId(conversationData.id);
        const lastMessage = conversationData.messages[conversationData.messages.length - 1];
        if (lastMessage && lastMessage.role === "assistant") {
          setMessages((prev) => {
            const newMessages = [...prev];
            newMessages[newMessages.length - 1] = {
              role: "assistant",
              content: lastMessage.content,
              sources: lastMessage.sources,
            };
            return newMessages;
          });
        }
      }
    } catch (error: any) {
      if (error.name !== "AbortError") {
        toast({
          title: "Error",
          description: "Failed to send message",
          variant: "destructive",
        });
        setMessages((prev) => [...prev.slice(0, -1)]);
      }
      setStreaming(false);
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const startNewConversation = () => {
    setMessages([]);
    setConversationId(null);
    setSelectedDocuments([]);
    toast({
      title: "New Conversation",
      description: "Started a new conversation",
    });
  };

  const formatMessage = (content: string) => {
    if (!content) return "";
    
    let formatted = content
      .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
      .replace(/\*(.*?)\*/g, "<em>$1</em>")
      .replace(/`(.*?)`/g, "<code>$1</code>")
      .replace(/```([\s\S]*?)```/g, "<pre><code>$1</code></pre>")
      .replace(/\n/g, "<br>");

    return formatted;
  };

  return (
    <div className="container mx-auto py-8 px-4 h-[calc(100vh-4rem)]">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold mb-2">AI Tutor</h1>
          <p className="text-muted-foreground">Ask questions about your uploaded documents</p>
        </div>
        <Button onClick={startNewConversation} variant="outline">
          <Plus className="mr-2 h-4 w-4" />
          New Conversation
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 h-[calc(100%-8rem)]">
        <Card className="lg:col-span-1 overflow-hidden flex flex-col">
          <CardHeader>
            <CardTitle className="flex items-center">
              <BookOpen className="mr-2 h-5 w-5" />
              Documents
            </CardTitle>
          </CardHeader>
          <CardContent className="flex-1 overflow-y-auto">
            <div className="space-y-2">
              {documents.length === 0 ? (
                <p className="text-sm text-muted-foreground text-center py-4">
                  No documents available
                </p>
              ) : (
                documents.map((doc) => (
                  <div
                    key={doc.id}
                    className={`p-3 rounded-lg cursor-pointer transition-colors ${
                      selectedDocuments.includes(doc.id)
                        ? "bg-primary text-primary-foreground"
                        : "bg-secondary hover:bg-secondary/80"
                    }`}
                    onClick={() => toggleDocumentSelection(doc.id)}
                  >
                    <div className="flex items-start space-x-2">
                      <FileText className="h-4 w-4 mt-0.5 flex-shrink-0" />
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium truncate">{doc.title}</p>
                        <p className="text-xs opacity-70 truncate">{doc.file_name}</p>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </CardContent>
        </Card>

        <Card className="lg:col-span-3 flex flex-col">
          <CardHeader className="flex-shrink-0">
            <CardTitle className="flex items-center justify-between">
              <div className="flex items-center">
                <MessageSquare className="mr-2 h-5 w-5" />
                Conversation
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setShowSources(!showSources)}
              >
                {showSources ? "Hide" : "Show"} Sources
              </Button>
            </CardTitle>
          </CardHeader>
          <CardContent className="flex-1 flex flex-col overflow-hidden">
            <div className="flex-1 overflow-y-auto mb-4 space-y-4">
              {messages.length === 0 ? (
                <div className="flex flex-col items-center justify-center h-full text-center">
                  <MessageSquare className="h-12 w-12 text-muted-foreground mb-4" />
                  <p className="text-muted-foreground">
                    Start a conversation by asking a question about your documents
                  </p>
                </div>
              ) : (
                messages.map((message, index) => (
                  <div
                    key={index}
                    className={`flex ${
                      message.role === "user" ? "justify-end" : "justify-start"
                    }`}
                  >
                    <div
                      className={`max-w-[80%] rounded-lg p-4 ${
                        message.role === "user"
                          ? "bg-primary text-primary-foreground"
                          : "bg-secondary"
                      }`}
                    >
                      <div
                        className="prose prose-sm dark:prose-invert"
                        dangerouslySetInnerHTML={{
                          __html: formatMessage(message.content),
                        }}
                      />
                      {message.sources && message.sources.length > 0 && showSources && (
                        <div className="mt-3 pt-3 border-t border-current/20">
                          <p className="text-xs font-semibold mb-2">Sources:</p>
                          <div className="space-y-1">
                            {message.sources.map((source, sourceIndex) => (
                              <div
                                key={sourceIndex}
                                className="text-xs p-2 bg-current/10 rounded"
                              >
                                <p className="font-medium">{source.metadata.title}</p>
                                <p className="opacity-70 truncate">
                                  {source.content}
                                </p>
                                <p className="opacity-50 text-xs mt-1">
                                  Score: {source.score.toFixed(3)}
                                </p>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                ))
              )}
              {streaming && (
                <div className="flex justify-start">
                  <div className="bg-secondary rounded-lg p-4">
                    <div className="flex space-x-2">
                      <div className="w-2 h-2 bg-current rounded-full animate-bounce" />
                      <div className="w-2 h-2 bg-current rounded-full animate-bounce delay-100" />
                      <div className="w-2 h-2 bg-current rounded-full animate-bounce delay-200" />
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            <div className="flex-shrink-0 space-y-2">
              {selectedDocuments.length > 0 && (
                <div className="flex items-center space-x-2 text-sm text-muted-foreground">
                  <FileText className="h-4 w-4" />
                  <span>
                    {selectedDocuments.length} document{selectedDocuments.length > 1 ? "s" : ""} selected
                  </span>
                </div>
              )}
              <div className="flex space-x-2">
                <Input
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Ask a question about your documents..."
                  disabled={loading}
                  className="flex-1"
                />
                <Button onClick={handleSend} disabled={loading || !input.trim()}>
                  <Send className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
