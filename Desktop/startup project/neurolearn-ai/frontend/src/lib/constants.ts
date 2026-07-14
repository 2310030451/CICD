export const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const ROUTES = {
  HOME: "/",
  LOGIN: "/login",
  REGISTER: "/register",
  FORGOT_PASSWORD: "/forgot-password",
  DASHBOARD: "/dashboard",
  PROFILE: "/dashboard/profile",
  SETTINGS: "/dashboard/settings",
  NOTIFICATIONS: "/dashboard/notifications",
  LEARN: "/dashboard/learn",
  QUIZ: "/dashboard/quiz",
  AGENTS: "/dashboard/agents",
  ANALYTICS: "/dashboard/analytics",
  FLASHCARDS: "/dashboard/flashcards",
  PLANNER: "/dashboard/planner",
} as const;

export const ROLES = {
  STUDENT: "student",
  PARENT: "parent",
  TEACHER: "teacher",
  ADMIN: "admin",
} as const;

export const SUBSCRIPTION_TIERS = {
  FREE: "free",
  PRO: "pro",
  ENTERPRISE: "enterprise",
} as const;

export const CONTENT_TYPES = {
  PDF: "pdf",
  DOCX: "docx",
  PPTX: "pptx",
  IMAGE: "image",
  AUDIO: "audio",
  VIDEO: "video",
  TEXT: "text",
} as const;

export const QUIZ_DIFFICULTY = {
  EASY: "easy",
  MEDIUM: "medium",
  HARD: "hard",
} as const;

export const AGENT_TYPES = {
  TUTOR: "tutor",
  QUIZ: "quiz",
  CODING: "coding",
  RESEARCH: "research",
  CAREER: "career",
  REVISION: "revision",
  PLANNER: "planner",
} as const;

export const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB

export const ALLOWED_FILE_TYPES = [
  "application/pdf",
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  "application/vnd.openxmlformats-officedocument.presentationml.presentation",
  "image/jpeg",
  "image/png",
  "image/gif",
  "image/webp",
  "audio/mpeg",
  "audio/wav",
  "audio/ogg",
  "video/mp4",
  "video/webm",
  "text/plain",
];

export const XP_LEVELS = [
  { level: 1, xp: 0, name: "Novice" },
  { level: 2, xp: 100, name: "Beginner" },
  { level: 3, xp: 300, name: "Apprentice" },
  { level: 4, xp: 600, name: "Learner" },
  { level: 5, xp: 1000, name: "Student" },
  { level: 6, xp: 1500, name: "Scholar" },
  { level: 7, xp: 2100, name: "Expert" },
  { level: 8, xp: 2800, name: "Master" },
  { level: 9, xp: 3600, name: "Grandmaster" },
  { level: 10, xp: 4500, name: "Legend" },
];

export const ACHIEVEMENTS = {
  FIRST_LOGIN: "first_login",
  FIRST_QUIZ: "first_quiz",
  PERFECT_SCORE: "perfect_score",
  WEEK_STREAK: "week_streak",
  MONTH_STREAK: "month_streak",
  CONTENT_UPLOADER: "content_uploader",
  CHAT_MASTER: "chat_master",
  QUICK_LEARNER: "quick_learner",
  KNOWLEDGE_SEEKER: "knowledge_seeker",
  AI_EXPLORER: "ai_explorer",
} as const;
