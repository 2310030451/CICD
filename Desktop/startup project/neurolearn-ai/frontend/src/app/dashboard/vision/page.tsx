"use client";

import { useState, useCallback } from "react";
import { useAuth } from "@/lib/hooks/use-auth";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Upload, Image as ImageIcon, FileText, Brain, BookOpen, Download, Trash2, CheckCircle, Clock, XCircle, Sparkles } from "lucide-react";
import { toast } from "@/components/ui/use-toast";

interface VisionImage {
  id: string;
  title: string;
  file_name: string;
  file_type: string;
  file_size: number;
  file_url: string;
  status: "pending" | "processing" | "completed" | "failed";
  image_type?: string;
  classification_confidence: number;
  ocr_text?: string;
  ocr_confidence: number;
  layout_analysis?: any;
  image_quality?: any;
  ai_explanation?: string;
  generated_quiz?: any;
  generated_flashcards?: any[];
  created_at: string;
}

export default function VisionPage() {
  const { user } = useAuth();
  const [images, setImages] = useState<VisionImage[]>([]);
  const [uploading, setUploading] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [title, setTitle] = useState("");
  const [subject, setSubject] = useState("");
  const [tags, setTags] = useState("");
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [selectedImage, setSelectedImage] = useState<VisionImage | null>(null);
  const [generatingQuiz, setGeneratingQuiz] = useState(false);
  const [generatingFlashcards, setGeneratingFlashcards] = useState(false);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);
      setTitle(file.name.replace(/\.[^/.]+$/, ""));
      
      const url = URL.createObjectURL(file);
      setPreviewUrl(url);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile || !title) {
      toast({
        title: "Error",
        description: "Please select an image and enter a title",
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
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/vision/upload`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      if (response.ok) {
        const newImage = await response.json();
        setImages([newImage, ...images]);
        toast({
          title: "Success",
          description: "Image uploaded and processed successfully",
        });
        setSelectedFile(null);
        setTitle("");
        setSubject("");
        setTags("");
        setPreviewUrl(null);
      } else {
        throw new Error("Upload failed");
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to upload image",
        variant: "destructive",
      });
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (imageId: string) => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/vision/${imageId}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.ok) {
        setImages(images.filter((img) => img.id !== imageId));
        if (selectedImage?.id === imageId) {
          setSelectedImage(null);
        }
        toast({
          title: "Success",
          description: "Image deleted successfully",
        });
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to delete image",
        variant: "destructive",
      });
    }
  };

  const handleGenerateQuiz = async (imageId: string) => {
    setGeneratingQuiz(true);
    try {
      const token = localStorage.getItem("access_token");
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/vision/${imageId}/quiz`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const quiz = await response.json();
        setSelectedImage((prev) => prev ? { ...prev, generated_quiz: quiz } : null);
        toast({
          title: "Success",
          description: "Quiz generated successfully",
        });
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to generate quiz",
        variant: "destructive",
      });
    } finally {
      setGeneratingQuiz(false);
    }
  };

  const handleGenerateFlashcards = async (imageId: string) => {
    setGeneratingFlashcards(true);
    try {
      const token = localStorage.getItem("access_token");
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/vision/${imageId}/flashcards`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setSelectedImage((prev) => prev ? { ...prev, generated_flashcards: data.flashcards } : null);
        toast({
          title: "Success",
          description: "Flashcards generated successfully",
        });
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to generate flashcards",
        variant: "destructive",
      });
    } finally {
      setGeneratingFlashcards(false);
    }
  };

  const downloadNotes = () => {
    if (!selectedImage) return;
    
    const notes = `
# ${selectedImage.title}

## Image Type
${selectedImage.image_type?.replace(/_/g, " ").toUpperCase() || "Unknown"}

## OCR Extracted Text
${selectedImage.ocr_text || "No text extracted"}

## AI Explanation
${selectedImage.ai_explanation || "No explanation available"}

## Image Quality
- Overall Quality: ${(selectedImage.image_quality?.overall_quality * 100).toFixed(1)}%
- Blur Score: ${(selectedImage.image_quality?.blur_score * 100).toFixed(1)}%
- Brightness Score: ${(selectedImage.image_quality?.brightness_score * 100).toFixed(1)}%
- Contrast Score: ${(selectedImage.image_quality?.contrast_score * 100).toFixed(1)}%

## Layout Analysis
- Layout Type: ${selectedImage.layout_analysis?.layout_type || "Unknown"}
- Has Text: ${selectedImage.layout_analysis?.has_text ? "Yes" : "No"}
- Has Images: ${selectedImage.layout_analysis?.has_images ? "Yes" : "No"}
- Has Tables: ${selectedImage.layout_analysis?.has_tables ? "Yes" : "No"}

Generated by NeuroLearn AI Vision
    `.trim();

    const blob = new Blob([notes], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${selectedImage.title}_notes.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
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
        <h1 className="text-3xl font-bold mb-2">Vision AI</h1>
        <p className="text-muted-foreground">Upload images for AI-powered analysis, OCR, and learning content generation</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Upload className="mr-2 h-5 w-5" />
                Upload Image
              </CardTitle>
              <CardDescription>Supported formats: JPG, PNG, BMP, TIFF, WebP</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <Label htmlFor="file">Image</Label>
                  <Input
                    id="file"
                    type="file"
                    accept="image/*"
                    onChange={handleFileSelect}
                    className="mt-1"
                  />
                </div>
                {previewUrl && (
                  <div className="relative">
                    <img
                      src={previewUrl}
                      alt="Preview"
                      className="w-full h-48 object-cover rounded-lg"
                    />
                  </div>
                )}
                <div>
                  <Label htmlFor="title">Title</Label>
                  <Input
                    id="title"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    placeholder="Image title"
                    className="mt-1"
                  />
                </div>
                <div>
                  <Label htmlFor="subject">Subject (Optional)</Label>
                  <Input
                    id="subject"
                    value={subject}
                    onChange={(e) => setSubject(e.target.value)}
                    placeholder="e.g., Mathematics, Biology"
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
                  {uploading ? "Processing..." : "Upload & Analyze"}
                </Button>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <ImageIcon className="mr-2 h-5 w-5" />
                Your Images
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2 max-h-96 overflow-y-auto">
                {images.length === 0 ? (
                  <p className="text-sm text-muted-foreground text-center py-4">
                    No images uploaded yet
                  </p>
                ) : (
                  images.map((img) => (
                    <div
                      key={img.id}
                      className={`p-3 rounded-lg cursor-pointer transition-colors ${
                        selectedImage?.id === img.id
                          ? "bg-primary text-primary-foreground"
                          : "bg-secondary hover:bg-secondary/80"
                      }`}
                      onClick={() => setSelectedImage(img)}
                    >
                      <div className="flex items-start space-x-2">
                        <ImageIcon className="h-4 w-4 mt-0.5 flex-shrink-0" />
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium truncate">{img.title}</p>
                          <p className="text-xs opacity-70 truncate">{img.file_name}</p>
                        </div>
                        {getStatusIcon(img.status)}
                      </div>
                    </div>
                  ))
                )}
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="lg:col-span-2 space-y-6">
          {selectedImage ? (
            <>
              <Card>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="flex items-center">
                      <Brain className="mr-2 h-5 w-5" />
                      {selectedImage.title}
                    </CardTitle>
                    <div className="flex items-center space-x-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={downloadNotes}
                      >
                        <Download className="mr-2 h-4 w-4" />
                        Notes
                      </Button>
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => handleDelete(selectedImage.id)}
                      >
                        <Trash2 className="h-4 w-4 text-destructive" />
                      </Button>
                    </div>
                  </div>
                  <CardDescription>
                    {selectedImage.image_type?.replace(/_/g, " ").toUpperCase()} • 
                    Confidence: {(selectedImage.classification_confidence * 100).toFixed(1)}%
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 gap-4 mb-6">
                    <div>
                      <p className="text-sm font-medium mb-1">Image Quality</p>
                      <div className="w-full bg-secondary rounded-full h-2">
                        <div
                          className="bg-primary h-2 rounded-full"
                          style={{
                            width: `${(selectedImage.image_quality?.overall_quality || 0) * 100}%`,
                          }}
                        />
                      </div>
                      <p className="text-xs text-muted-foreground mt-1">
                        {(selectedImage.image_quality?.overall_quality || 0) * 100}% Quality
                      </p>
                    </div>
                    <div>
                      <p className="text-sm font-medium mb-1">OCR Confidence</p>
                      <div className="w-full bg-secondary rounded-full h-2">
                        <div
                          className="bg-primary h-2 rounded-full"
                          style={{ width: `${selectedImage.ocr_confidence * 100}%` }}
                        />
                      </div>
                      <p className="text-xs text-muted-foreground mt-1">
                        {(selectedImage.ocr_confidence * 100).toFixed(1)}% Confidence
                      </p>
                    </div>
                  </div>

                  <div className="space-y-6">
                    <div>
                      <h3 className="text-lg font-semibold mb-3 flex items-center">
                        <FileText className="mr-2 h-5 w-5" />
                        OCR Extracted Text
                      </h3>
                      <div className="bg-secondary p-4 rounded-lg max-h-48 overflow-y-auto">
                        <p className="text-sm whitespace-pre-wrap">
                          {selectedImage.ocr_text || "No text extracted"}
                        </p>
                      </div>
                    </div>

                    <div>
                      <h3 className="text-lg font-semibold mb-3 flex items-center">
                        <Sparkles className="mr-2 h-5 w-5" />
                        AI Explanation
                      </h3>
                      <div className="bg-secondary p-4 rounded-lg">
                        <p className="text-sm whitespace-pre-wrap">
                          {selectedImage.ai_explanation || "No explanation available"}
                        </p>
                      </div>
                    </div>

                    <div className="flex space-x-4">
                      <Button
                        onClick={() => handleGenerateQuiz(selectedImage.id)}
                        disabled={generatingQuiz}
                        className="flex-1"
                      >
                        <BookOpen className="mr-2 h-4 w-4" />
                        {generatingQuiz ? "Generating..." : "Generate Quiz"}
                      </Button>
                      <Button
                        onClick={() => handleGenerateFlashcards(selectedImage.id)}
                        disabled={generatingFlashcards}
                        variant="outline"
                        className="flex-1"
                      >
                        <Sparkles className="mr-2 h-4 w-4" />
                        {generatingFlashcards ? "Generating..." : "Flashcards"}
                      </Button>
                    </div>

                    {selectedImage.generated_quiz && (
                      <div>
                        <h3 className="text-lg font-semibold mb-3">Generated Quiz</h3>
                        <div className="bg-secondary p-4 rounded-lg">
                          <p className="text-sm whitespace-pre-wrap">
                            {selectedImage.generated_quiz.questions}
                          </p>
                        </div>
                      </div>
                    )}

                    {selectedImage.generated_flashcards && selectedImage.generated_flashcards.length > 0 && (
                      <div>
                        <h3 className="text-lg font-semibold mb-3">Generated Flashcards</h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                          {selectedImage.generated_flashcards.map((card, index) => (
                            <Card key={index}>
                              <CardContent className="p-4">
                                <p className="font-semibold mb-2">{card.front}</p>
                                <p className="text-sm text-muted-foreground">{card.back}</p>
                              </CardContent>
                            </Card>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            </>
          ) : (
            <Card>
              <CardContent className="flex flex-col items-center justify-center py-24">
                <Brain className="h-16 w-16 text-muted-foreground mb-4" />
                <p className="text-muted-foreground text-center">
                  Select an image to view analysis and generate learning content
                </p>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
