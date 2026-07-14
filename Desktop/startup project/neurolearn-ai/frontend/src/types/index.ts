export interface User {
  id: string;
  firebase_uid: string;
  email: string;
  email_verified: boolean;
  display_name: string;
  photo_url?: string;
  provider: string;
  role: "student" | "parent" | "teacher" | "admin";
  created_at: string;
  updated_at: string;
  last_login?: string;
  is_active: boolean;
  subscription_tier: "free" | "pro" | "enterprise";
  subscription_expires?: string;
  settings?: UserSettings;
}

export interface UserSettings {
  language: string;
  theme: "light" | "dark" | "system";
  notifications: {
    email: boolean;
    push: boolean;
    study_reminders: boolean;
  };
  privacy: {
    data_sharing: boolean;
    analytics: boolean;
  };
}

export interface UserProfile {
  id: string;
  user_id: string;
  academic_level: string;
  field_of_study?: string;
  institution?: string;
  grade_level?: string;
  learning_goals: string[];
  interests: string[];
  learning_style: {
    visual: number;
    auditory: number;
    kinesthetic: number;
    reading: number;
  };
  study_preferences: {
    daily_study_hours: number;
    study_time: "morning" | "afternoon" | "evening";
    session_duration: number;
  };
  strengths: string[];
  weaknesses: string[];
  bio?: string;
  social_links?: {
    linkedin?: string;
    github?: string;
    website?: string;
  };
  created_at: string;
  updated_at: string;
}

export interface Content {
  id: string;
  user_id: string;
  title: string;
  description: string;
  content_type: "pdf" | "docx" | "pptx" | "image" | "audio" | "video" | "text";
  file_url: string;
  file_size: number;
  file_hash: string;
  mime_type: string;
  metadata?: {
    page_count?: number;
    duration?: number;
    dimensions?: {
      width: number;
      height: number;
    };
    language?: string;
    author?: string;
    created_date?: string;
  };
  processing_status: "pending" | "processing" | "completed" | "failed";
  processing_steps: {
    ocr_completed: boolean;
    chunking_completed: boolean;
    embedding_completed: boolean;
    cnn_analyzed: boolean;
  };
  tags: string[];
  subject?: string;
  topics: string[];
  is_public: boolean;
  access_count: number;
  created_at: string;
  updated_at: string;
}

export interface Session {
  id: string;
  user_id: string;
  session_type: "chat" | "quiz" | "study" | "revision" | "agent";
  agent_type?: string;
  content_ids: string[];
  title: string;
  started_at: string;
  ended_at?: string;
  duration?: number;
  message_count: number;
  topics_discussed: string[];
  learning_objectives: string[];
  status: "active" | "completed" | "archived";
  summary?: string;
  key_takeaways: string[];
  created_at: string;
  updated_at: string;
}

export interface Message {
  id: string;
  session_id: string;
  user_id: string;
  role: "user" | "assistant" | "system";
  content: string;
  content_type: "text" | "image" | "audio" | "file";
  metadata?: {
    model_used?: string;
    tokens_used?: number;
    latency?: number;
    citations?: Citation[];
    confidence_score?: number;
  };
  timestamp: string;
}

export interface Citation {
  content_id: string;
  chunk_id: string;
  relevance_score: number;
  text_snippet: string;
}

export interface Quiz {
  id: string;
  user_id: string;
  content_id?: string;
  title: string;
  description: string;
  subject: string;
  topics: string[];
  difficulty: "easy" | "medium" | "hard";
  question_count: number;
  time_limit?: number;
  questions: Question[];
  is_public: boolean;
  usage_count: number;
  created_at: string;
  updated_at: string;
}

export interface Question {
  id: string;
  type: "multiple_choice" | "true_false" | "short_answer" | "essay";
  question: string;
  options?: string[];
  correct_answer: string;
  explanation: string;
  points: number;
  difficulty: "easy" | "medium" | "hard";
}

export interface QuizAttempt {
  id: string;
  quiz_id: string;
  user_id: string;
  attempt_number: number;
  started_at: string;
  completed_at?: string;
  time_taken?: number;
  score?: number;
  total_points: number;
  earned_points?: number;
  answers?: Answer[];
  performance_analysis?: {
    strengths: string[];
    weaknesses: string[];
    recommended_topics: string[];
  };
  created_at: string;
}

export interface Answer {
  question_id: string;
  user_answer: string;
  is_correct: boolean;
  points_earned: number;
  time_spent: number;
}

export interface Analytics {
  id: string;
  user_id: string;
  date: string;
  metrics: {
    study_time: number;
    content_consumed: number;
    questions_answered: number;
    quizzes_completed: number;
    average_score: number;
    sessions_completed: number;
    messages_exchanged: number;
    concepts_learned: number;
    revisions_done: number;
  };
  subject_breakdown: SubjectBreakdown[];
  activity_timeline: ActivityTimeline[];
  created_at: string;
}

export interface SubjectBreakdown {
  subject: string;
  study_time: number;
  questions_answered: number;
  average_score: number;
  progress: number;
}

export interface ActivityTimeline {
  timestamp: string;
  activity_type: string;
  details: Record<string, any>;
}

export interface Prediction {
  id: string;
  user_id: string;
  prediction_type: "performance" | "dropout" | "revision" | "learning_speed";
  prediction_date: string;
  predicted_value: number;
  confidence: number;
  features_used: string[];
  model_version: string;
  recommendations: string[];
  historical_data: {
    date: string;
    value: number;
  }[];
  created_at: string;
}

export interface Agent {
  id: string;
  user_id: string;
  agent_type: string;
  name: string;
  description: string;
  configuration: {
    model: string;
    temperature: number;
    max_tokens: number;
    system_prompt: string;
    tools: string[];
    capabilities: string[];
  };
  is_active: boolean;
  usage_count: number;
  created_at: string;
  updated_at: string;
}

export interface Notification {
  id: string;
  user_id: string;
  type: "info" | "success" | "warning" | "error";
  title: string;
  message: string;
  action_url?: string;
  action_label?: string;
  is_read: boolean;
  created_at: string;
}

export interface Achievement {
  id: string;
  user_id: string;
  achievement_type: string;
  title: string;
  description: string;
  icon: string;
  unlocked_at: string;
  progress?: number;
  target?: number;
}
