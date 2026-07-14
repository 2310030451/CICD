"use client";

import { useState, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Mic, Volume2, Languages } from "lucide-react";

export default function VoiceAIPage() {
  const [isRecording, setIsRecording] = useState(false);
  const [transcription, setTranscription] = useState("");
  const [selectedLanguage, setSelectedLanguage] = useState("en");
  const [isPlaying, setIsPlaying] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  const languages = [
    { code: "en", name: "English" },
    { code: "es", name: "Spanish" },
    { code: "fr", name: "French" },
    { code: "de", name: "German" },
    { code: "hi", name: "Hindi" },
    { code: "ja", name: "Japanese" },
    { code: "ko", name: "Korean" },
    { code: "zh", name: "Chinese" },
  ];

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      audioChunksRef.current = [];

      mediaRecorderRef.current.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };

      mediaRecorderRef.current.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: "audio/webm" });
        await transcribeAudio(audioBlob);
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
    } catch (error) {
      console.error("Error starting recording:", error);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const transcribeAudio = async (audioBlob: Blob) => {
    const formData = new FormData();
    formData.append("audio_file", audioBlob, "audio.webm");
    formData.append("language", selectedLanguage);

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/voice/speech-to-text`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: formData,
      });

      const data = await response.json();
      if (data.success) {
        setTranscription(data.data.text);
      }
    } catch (error) {
      console.error("Error transcribing audio:", error);
    }
  };

  const textToSpeech = async (text: string) => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/voice/text-to-speech?text=${encodeURIComponent(text)}&language=${selectedLanguage}`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );

      if (response.ok) {
        const audioBlob = await response.blob();
        const audioUrl = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioUrl);
        audio.play();
        setIsPlaying(true);
        audio.onended = () => setIsPlaying(false);
      }
    } catch (error) {
      console.error("Error converting text to speech:", error);
    }
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Voice AI</h1>
        <Badge variant="outline" className="flex items-center gap-2">
          <Languages className="w-4 h-4" />
          Multilingual Support
        </Badge>
      </div>

      <Tabs defaultValue="speech-to-text" className="w-full">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="speech-to-text">Speech to Text</TabsTrigger>
          <TabsTrigger value="text-to-speech">Text to Speech</TabsTrigger>
        </TabsList>

        <TabsContent value="speech-to-text" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Mic className="w-5 h-5" />
                Speech to Text
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="text-sm font-medium mb-2 block">Select Language</label>
                <select
                  value={selectedLanguage}
                  onChange={(e) => setSelectedLanguage(e.target.value)}
                  className="w-full p-2 border rounded-md"
                >
                  {languages.map((lang) => (
                    <option key={lang.code} value={lang.code}>
                      {lang.name}
                    </option>
                  ))}
                </select>
              </div>

              <div className="flex gap-4">
                {!isRecording ? (
                  <Button onClick={startRecording} className="flex-1">
                    <Mic className="w-4 h-4 mr-2" />
                    Start Recording
                  </Button>
                ) : (
                  <Button onClick={stopRecording} variant="destructive" className="flex-1">
                    <Mic className="w-4 h-4 mr-2" />
                    Stop Recording
                  </Button>
                )}
              </div>

              {isRecording && (
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse" />
                  Recording...
                </div>
              )}

              {transcription && (
                <div className="p-4 bg-muted rounded-md">
                  <h3 className="font-medium mb-2">Transcription:</h3>
                  <p className="text-sm">{transcription}</p>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="text-to-speech" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Volume2 className="w-5 h-5" />
                Text to Speech
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="text-sm font-medium mb-2 block">Select Language</label>
                <select
                  value={selectedLanguage}
                  onChange={(e) => setSelectedLanguage(e.target.value)}
                  className="w-full p-2 border rounded-md"
                >
                  {languages.map((lang) => (
                    <option key={lang.code} value={lang.code}>
                      {lang.name}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="text-sm font-medium mb-2 block">Enter Text</label>
                <textarea
                  id="tts-text"
                  className="w-full p-2 border rounded-md min-h-[100px]"
                  placeholder="Enter text to convert to speech..."
                />
              </div>

              <Button
                onClick={() => {
                  const text = (document.getElementById("tts-text") as HTMLTextAreaElement).value;
                  if (text) textToSpeech(text);
                }}
                disabled={isPlaying}
                className="w-full"
              >
                <Volume2 className="w-4 h-4 mr-2" />
                {isPlaying ? "Playing..." : "Convert to Speech"}
              </Button>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
