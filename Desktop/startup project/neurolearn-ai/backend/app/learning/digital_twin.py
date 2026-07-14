from typing import Dict, List, Optional
from datetime import datetime, timedelta
from enum import Enum
from app.config import settings
from loguru import logger


class LearningStyle(str, Enum):
    TEXT = "text"
    DIAGRAM = "diagram"
    FLASHCARDS = "flashcards"
    VIDEOS = "videos"
    PRACTICE_QUESTIONS = "practice_questions"
    MIXED = "mixed"


class StudyTimePreference(str, Enum):
    MORNING = "morning"
    AFTERNOON = "afternoon"
    EVENING = "evening"
    NIGHT = "night"
    FLEXIBLE = "flexible"


class DigitalTwin:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.learning_style = LearningStyle.MIXED
        self.learning_speed = "moderate"
        self.attention_span_minutes = 30
        self.knowledge_gaps = []
        self.revision_patterns = {}
        self.preferred_study_time = StudyTimePreference.FLEXIBLE
        self.confidence_level = 0.5
        self.memory_retention = 0.7
        self.strengths = []
        self.weaknesses = []
        self.learning_history = []
        self.interaction_history = []
        self.last_updated = datetime.utcnow()

    def update_learning_style(self, interaction_data: Dict):
        try:
            style_counts = {
                LearningStyle.TEXT: 0,
                LearningStyle.DIAGRAM: 0,
                LearningStyle.FLASHCARDS: 0,
                LearningStyle.VIDEOS: 0,
                LearningStyle.PRACTICE_QUESTIONS: 0,
            }
            
            for interaction in self.interaction_history[-50:]:
                if interaction.get("type") == "document_upload":
                    style_counts[LearningStyle.TEXT] += 1
                elif interaction.get("type") == "vision_image":
                    style_counts[LearningStyle.DIAGRAM] += 1
                elif interaction.get("type") == "flashcard_generation":
                    style_counts[LearningStyle.FLASHCARDS] += 1
                elif interaction.get("type") == "video_watch":
                    style_counts[LearningStyle.VIDEOS] += 1
                elif interaction.get("type") == "quiz_attempt":
                    style_counts[LearningStyle.PRACTICE_QUESTIONS] += 1
            
            dominant_style = max(style_counts, key=style_counts.get)
            
            if style_counts[dominant_style] > 5:
                self.learning_style = dominant_style
            
            self.last_updated = datetime.utcnow()
            logger.info(f"Updated learning style for user {self.user_id}: {self.learning_style}")
        except Exception as e:
            logger.error(f"Failed to update learning style: {e}")

    def update_learning_speed(self, quiz_data: List[Dict]):
        try:
            if len(quiz_data) < 5:
                return
            
            completion_times = [q.get("completion_time", 60) for q in quiz_data]
            avg_time = sum(completion_times) / len(completion_times)
            
            if avg_time < 30:
                self.learning_speed = "fast"
            elif avg_time < 60:
                self.learning_speed = "moderate"
            else:
                self.learning_speed = "slow"
            
            self.last_updated = datetime.utcnow()
            logger.info(f"Updated learning speed for user {self.user_id}: {self.learning_speed}")
        except Exception as e:
            logger.error(f"Failed to update learning speed: {e}")

    def update_attention_span(self, session_data: List[Dict]):
        try:
            if len(session_data) < 3:
                return
            
            session_durations = [s.get("duration", 30) for s in session_data]
            avg_duration = sum(session_durations) / len(session_durations)
            
            self.attention_span_minutes = int(avg_duration)
            self.last_updated = datetime.utcnow()
            logger.info(f"Updated attention span for user {self.user_id}: {self.attention_span_minutes} minutes")
        except Exception as e:
            logger.error(f"Failed to update attention span: {e}")

    def update_knowledge_gaps(self, quiz_results: List[Dict]):
        try:
            topic_scores = {}
            
            for result in quiz_results:
                topic = result.get("topic", "general")
                score = result.get("score", 0)
                
                if topic not in topic_scores:
                    topic_scores[topic] = []
                topic_scores[topic].append(score)
            
            self.knowledge_gaps = []
            for topic, scores in topic_scores.items():
                avg_score = sum(scores) / len(scores)
                if avg_score < 60:
                    self.knowledge_gaps.append({
                        "topic": topic,
                        "average_score": avg_score,
                        "gap_severity": "high" if avg_score < 40 else "medium",
                    })
            
            self.last_updated = datetime.utcnow()
            logger.info(f"Updated knowledge gaps for user {self.user_id}: {len(self.knowledge_gaps)} gaps")
        except Exception as e:
            logger.error(f"Failed to update knowledge gaps: {e}")

    def update_revision_patterns(self, revision_data: List[Dict]):
        try:
            if not revision_data:
                return
            
            revision_intervals = []
            for i in range(1, len(revision_data)):
                prev_date = revision_data[i - 1].get("date")
                curr_date = revision_data[i].get("date")
                if prev_date and curr_date:
                    interval = (curr_date - prev_date).days
                    revision_intervals.append(interval)
            
            if revision_intervals:
                avg_interval = sum(revision_intervals) / len(revision_intervals)
                self.revision_patterns = {
                    "average_interval_days": avg_interval,
                    "consistency_score": 1.0 - (min(avg_interval / 7, 1.0)),
                    "preferred_days": self._extract_preferred_days(revision_data),
                }
            
            self.last_updated = datetime.utcnow()
            logger.info(f"Updated revision patterns for user {self.user_id}")
        except Exception as e:
            logger.error(f"Failed to update revision patterns: {e}")

    def update_study_time_preference(self, activity_data: List[Dict]):
        try:
            if not activity_data:
                return
            
            hour_counts = {h: 0 for h in range(24)}
            
            for activity in activity_data:
                timestamp = activity.get("timestamp")
                if timestamp:
                    hour = timestamp.hour
                    hour_counts[hour] += 1
            
            morning = sum(hour_counts[h] for h in range(6, 12))
            afternoon = sum(hour_counts[h] for h in range(12, 18))
            evening = sum(hour_counts[h] for h in range(18, 22))
            night = sum(hour_counts[h] for h in range(22, 24)) + sum(hour_counts[h] for h in range(0, 6))
            
            max_period = max(morning, afternoon, evening, night)
            
            if max_period == morning:
                self.preferred_study_time = StudyTimePreference.MORNING
            elif max_period == afternoon:
                self.preferred_study_time = StudyTimePreference.AFTERNOON
            elif max_period == evening:
                self.preferred_study_time = StudyTimePreference.EVENING
            elif max_period == night:
                self.preferred_study_time = StudyTimePreference.NIGHT
            else:
                self.preferred_study_time = StudyTimePreference.FLEXIBLE
            
            self.last_updated = datetime.utcnow()
            logger.info(f"Updated study time preference for user {self.user_id}: {self.preferred_study_time}")
        except Exception as e:
            logger.error(f"Failed to update study time preference: {e}")

    def update_confidence_level(self, quiz_results: List[Dict]):
        try:
            if not quiz_results:
                return
            
            recent_scores = [q.get("score", 0) for q in quiz_results[-10:]]
            avg_score = sum(recent_scores) / len(recent_scores)
            
            self.confidence_level = avg_score / 100
            self.last_updated = datetime.utcnow()
            logger.info(f"Updated confidence level for user {self.user_id}: {self.confidence_level:.2f}")
        except Exception as e:
            logger.error(f"Failed to update confidence level: {e}")

    def update_memory_retention(self, review_data: List[Dict]):
        try:
            if len(review_data) < 2:
                return
            
            retention_scores = []
            for i in range(1, len(review_data)):
                initial_score = review_data[i - 1].get("score", 0)
                review_score = review_data[i].get("score", 0)
                
                if initial_score > 0:
                    retention = review_score / initial_score
                    retention_scores.append(retention)
            
            if retention_scores:
                self.memory_retention = sum(retention_scores) / len(retention_scores)
            
            self.last_updated = datetime.utcnow()
            logger.info(f"Updated memory retention for user {self.user_id}: {self.memory_retention:.2f}")
        except Exception as e:
            logger.error(f"Failed to update memory retention: {e}")

    def update_strengths_weaknesses(self, topic_performance: Dict[str, float]):
        try:
            self.strengths = []
            self.weaknesses = []
            
            for topic, score in topic_performance.items():
                if score >= 80:
                    self.strengths.append({"topic": topic, "score": score})
                elif score <= 50:
                    self.weaknesses.append({"topic": topic, "score": score})
            
            self.strengths.sort(key=lambda x: x["score"], reverse=True)
            self.weaknesses.sort(key=lambda x: x["score"])
            
            self.last_updated = datetime.utcnow()
            logger.info(f"Updated strengths/weaknesses for user {self.user_id}")
        except Exception as e:
            logger.error(f"Failed to update strengths/weaknesses: {e}")

    def add_interaction(self, interaction: Dict):
        try:
            interaction["timestamp"] = datetime.utcnow()
            self.interaction_history.append(interaction)
            
            if len(self.interaction_history) > 1000:
                self.interaction_history = self.interaction_history[-1000:]
            
            self.last_updated = datetime.utcnow()
        except Exception as e:
            logger.error(f"Failed to add interaction: {e}")

    def add_learning_event(self, event: Dict):
        try:
            event["timestamp"] = datetime.utcnow()
            self.learning_history.append(event)
            
            if len(self.learning_history) > 500:
                self.learning_history = self.learning_history[-500:]
            
            self.last_updated = datetime.utcnow()
        except Exception as e:
            logger.error(f"Failed to add learning event: {e}")

    def get_personalization_profile(self) -> Dict:
        try:
            return {
                "user_id": self.user_id,
                "learning_style": self.learning_style.value,
                "learning_speed": self.learning_speed,
                "attention_span_minutes": self.attention_span_minutes,
                "knowledge_gaps": self.knowledge_gaps,
                "revision_patterns": self.revision_patterns,
                "preferred_study_time": self.preferred_study_time.value,
                "confidence_level": self.confidence_level,
                "memory_retention": self.memory_retention,
                "strengths": self.strengths,
                "weaknesses": self.weaknesses,
                "last_updated": self.last_updated.isoformat(),
            }
        except Exception as e:
            logger.error(f"Failed to get personalization profile: {e}")
            return {}

    def get_study_recommendations(self) -> List[str]:
        try:
            recommendations = []
            
            if self.knowledge_gaps:
                top_gap = self.knowledge_gaps[0]
                recommendations.append(f"Focus on {top_gap['topic']} - identified as a knowledge gap")
            
            if self.memory_retention < 0.6:
                recommendations.append("Increase revision frequency to improve memory retention")
            
            if self.attention_span_minutes < 20:
                recommendations.append("Try shorter study sessions to match your attention span")
            
            if self.confidence_level < 0.5:
                recommendations.append("Start with easier topics to build confidence")
            
            if self.learning_style != LearningStyle.MIXED:
                recommendations.append(f"Continue using {self.learning_style.value} learning materials")
            
            return recommendations
        except Exception as e:
            logger.error(f"Failed to get study recommendations: {e}")
            return []

    def _extract_preferred_days(self, data: List[Dict]) -> List[str]:
        try:
            day_counts = {day: 0 for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}
            
            for item in data:
                date = item.get("date")
                if date:
                    day_name = date.strftime("%A")
                    day_counts[day_name] += 1
            
            sorted_days = sorted(day_counts.items(), key=lambda x: x[1], reverse=True)
            return [day for day, count in sorted_days if count > 0]
        except Exception as e:
            logger.error(f"Failed to extract preferred days: {e}")
            return []

    def to_dict(self) -> Dict:
        return self.get_personalization_profile()


class DigitalTwinManager:
    def __init__(self):
        self.twins = {}

    def get_twin(self, user_id: str) -> DigitalTwin:
        if user_id not in self.twins:
            self.twins[user_id] = DigitalTwin(user_id)
        return self.twins[user_id]

    def update_twin_from_data(self, user_id: str, data: Dict):
        try:
            twin = self.get_twin(user_id)
            
            if "interactions" in data:
                for interaction in data["interactions"]:
                    twin.add_interaction(interaction)
            
            if "learning_events" in data:
                for event in data["learning_events"]:
                    twin.add_learning_event(event)
            
            if "quiz_results" in data:
                twin.update_learning_speed(data["quiz_results"])
                twin.update_confidence_level(data["quiz_results"])
                twin.update_knowledge_gaps(data["quiz_results"])
            
            if "session_data" in data:
                twin.update_attention_span(data["session_data"])
                twin.update_study_time_preference(data["session_data"])
            
            if "revision_data" in data:
                twin.update_revision_patterns(data["revision_data"])
            
            if "review_data" in data:
                twin.update_memory_retention(data["review_data"])
            
            if "topic_performance" in data:
                twin.update_strengths_weaknesses(data["topic_performance"])
            
            twin.update_learning_style({})
            
            logger.info(f"Updated digital twin for user {user_id}")
        except Exception as e:
            logger.error(f"Failed to update digital twin: {e}")


digital_twin_manager = DigitalTwinManager()
