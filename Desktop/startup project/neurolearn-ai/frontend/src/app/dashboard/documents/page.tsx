"use client";

import { useState, useCallback } from "react";
import { useAuth } from "@/lib/hooks/use-auth";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Upload, FileText, Trash2, CheckCircle, Clock, XCircle } from "lucide-react";
import { toast } from "@/components/ui/use-toast";

interface Document {
  id: string;
  title: string;
  file_name: string;
  file_type: string;
  file_size: number;
  status: "uploading" | "processing" | "completed" | "failed";
  chunk_count: number;
  subject?: string;
  tags: string[];
  created_at: string;
}

export default function DocumentsPage() {
  const { user } = useAuth();
  const [documents, setDocuments] = useState<Document[]>([]);
  const [uploading, setUploading] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [title, setTitle] = useState("");
  const [subject, setSubject] = useState("");
  const [tags, setTags] = useState("");

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
      setTitle(e.target.files[0].name.replace(/\.[^/.]+$/, ""));
    }
  };

  const handleUpload = async () => {
    if (!selectedFile || !title) {
      toast({
        title: "Error",
        description: "Please select a file and enter a title",
        variant: "destructive",
      });
      return;
    }

    setUploading(true);
    const formData = new FormData();
    formData.append("file", selectedFile);
    formData.append("title", title);
    formData.append("subject", subject);
    formData.append("tags", tags);

    try {
      const token = localStorage.getItem("access_token");
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/documents/upload`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      if (response.ok) {
        const newDocument = await response.json();
        setDocuments([newDocument, ...documents]);
        toast({
          title: "Success",
          description: "Document uploaded successfully",
        });
        setSelectedFile(null);
        setTitle("");
        setSubject("");
        setTags("");
      } else {
        throw new Error("Upload failed");
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to upload document",
        variant: "destructive",
      });
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (documentId: string) => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/documents/${documentId}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.ok) {
        setDocuments(documents.filter((doc) => doc.id !== documentId));
        toast({
          title: "Success",
          description: "Document deleted successfully",
        });
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to delete document",
        variant: "destructive",
      });
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + " " + sizes[i];
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "completed":
        return <CheckCircle className="h-5 w-5 text-green-500" />;
      case "processing":
        return <Clock className="h-5 w-5 text-yellow-500" />;
      case "failed":
        return <XCircle className="h-5 w-5 text-red-500" />;
      default:
        return <Clock className="h-5 w-5 text-gray-500" />;
    }
  };

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Document Library</h1>
        <p className="text-muted-foreground">Upload and manage your study documents</p>
      </div>

      <Card className="mb-8">
        <CardHeader>
          <CardTitle>Upload Document</CardTitle>
          <CardDescription>Supported formats: PDF, DOCX, PPTX, TXT, Markdown</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <Label htmlFor="file">File</Label>
              <Input
                id="file"
                type="file"
                accept=".pdf,.docx,.pptx,.txt,.md"
                onChange={handleFileSelect}
                className="mt-1"
              />
            </div>
            <div>
              <Label htmlFor="title">Title</Label>
              <Input
                id="title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Document title"
                className="mt-1"
              />
            </div>
            <div>
              <Label htmlFor="subject">Subject (Optional)</Label>
              <Input
                id="subject"
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
                placeholder="e.g., Mathematics, Physics"
                className="mt-1"
              />
            </div>
            <div>
              <Label htmlFor="tags">Tags (Optional)</Label>
              <Input
                id="tags"
                value={tags}
                onChange={(e) => setTags(e.target.value)}
                placeholder="Comma-separated tags"
                className="mt-1"
              />
            </div>
            <Button onClick={handleUpload} disabled={uploading} className="w-full">
              <Upload className="mr-2 h-4 w-4" />
              {uploading ? "Uploading..." : "Upload Document"}
            </Button>
          </div>
        </CardContent>
      </Card>

      <div className="grid gap-4">
        <h2 className="text-2xl font-semibold">Your Documents</h2>
        {documents.length === 0 ? (
          <Card>
            <CardContent className="flex flex-col items-center justify-center py-12">
              <FileText className="h-12 w-12 text-muted-foreground mb-4" />
              <p className="text-muted-foreground">No documents uploaded yet</p>
            </CardContent>
          </Card>
        ) : (
          documents.map((doc) => (
            <Card key={doc.id}>
              <CardContent className="p-6">
                <div className="flex items-start justify-between">
                  <div className="flex items-start space-x-4">
                    <div className="p-3 bg-primary/10 rounded-lg">
                      <FileText className="h-6 w-6 text-primary" />
                    </div>
                    <div className="flex-1">
                      <h3 className="font-semibold text-lg">{doc.title}</h3>
                      <p className="text-sm text-muted-foreground">{doc.file_name}</p>
                      <div className="flex items-center space-x-4 mt-2 text-sm text-muted-foreground">
                        <span>{formatFileSize(doc.file_size)}</span>
                        <span>{doc.file_type.toUpperCase()}</span>
                        <span>{doc.chunk_count} chunks</span>
                      </div>
                      {doc.subject && (
                        <div className="mt-2">
                          <span className="inline-block px-2 py-1 bg-secondary rounded text-xs">
                            {doc.subject}
                          </span>
                        </div>
                      )}
                      {doc.tags.length > 0 && (
                        <div className="mt-2 flex flex-wrap gap-2">
                          {doc.tags.map((tag, index) => (
                            <span key={index} className="inline-block px-2 py-1 bg-primary/10 rounded text-xs">
                              {tag}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="flex items-center space-x-1 mr-4">
                      {getStatusIcon(doc.status)}
                      <span className="text-sm capitalize">{doc.status}</span>
                    </div>
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={() => handleDelete(doc.id)}
                    >
                      <Trash2 className="h-4 w-4 text-destructive" />
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>
    </div>
  );
}
