from typing import Dict, List, Optional
from datetime import datetime, timedelta
from app.learning.digital_twin import digital_twin_manager
from app.learning.lstm_model import learning_predictor
from app.config import settings
from loguru import logger
import random


class RecommendationEngine:
    def __init__(self):
        self.recommendation_cache = {}
        self.cache_ttl = settings.recommendation_cache_ttl

    async def generate_recommendations(self, user_id: str, user_data: Dict) -> Dict:
        try:
            cache_key = f"{user_id}_{datetime.utcnow().strftime('%Y%m%d')}"
            
            if cache_key in self.recommendation_cache:
                cached_time = self.recommendation_cache[cache_key]["timestamp"]
                if (datetime.utcnow() - cached_time).total_seconds() < self.cache_ttl:
                    return self.recommendation_cache[cache_key]["recommendations"]
            
            digital_twin = digital_twin_manager.get_twin(user_id)
            personalization = digital_twin.get_personalization_profile()
            
            recommendations = {
                "topics_to_revise": self._get_revision_topics(personalization, user_data),
                "practice_questions": self._get_practice_recommendations(personalization, user_data),
                "study_schedule": self._get_study_schedule_recommendations(personalization, user_data),
                "difficulty_adjustment": self._get_difficulty_recommendations(personalization, user_data),
                "learning_resources": self._get_resource_recommendations(personalization, user_data),
                "generated_at": datetime.utcnow().isoformat(),
                "confidence": 0.85,
            }
            
            self.recommendation_cache[cache_key] = {
                "recommendations": recommendations,
                "timestamp": datetime.utcnow(),
            }
            
            return recommendations
        except Exception as e:
            logger.error(f"Failed to generate recommendations: {e}")
            return self._get_default_recommendations()

    def _get_revision_topics(self, personalization: Dict, user_data: Dict) -> List[Dict]:
        try:
            knowledge_gaps = personalization.get("knowledge_gaps", [])
            
            revision_topics = []
            for gap in knowledge_gaps[:5]:
                revision_topics.append({
                    "topic": gap["topic"],
                    "priority": gap.get("gap_severity", "medium"),
                    "reason": "Identified as knowledge gap",
                    "suggested_time": 30 if gap.get("gap_severity") == "high" else 20,
                })
            
            if not revision_topics:
                revision_topics.append({
                    "topic": "General review",
                    "priority": "low",
                    "reason": "No specific gaps identified",
                    "suggested_time": 20,
                })
            
            return revision_topics
        except Exception as e:
            logger.error(f"Failed to get revision topics: {e}")
            return []

    def _get_practice_recommendations(self, personalization: Dict, user_data: Dict) -> List[Dict]:
        try:
            confidence = personalization.get("confidence_level", 0.5)
            learning_speed = personalization.get("learning_speed", "moderate")
            
            recommendations = []
            
            if confidence < 0.5:
                recommendations.append({
                    "type": "foundational_practice",
                    "difficulty": "easy",
                    "quantity": 5,
                    "reason": "Build confidence with easier questions",
                })
            elif confidence > 0.8:
                recommendations.append({
                    "type": "challenge_questions",
                    "difficulty": "hard",
                    "quantity": 3,
                    "reason": "Challenge yourself with advanced problems",
                })
            
            if learning_speed == "fast":
                recommendations.append({
                    "type": "timed_practice",
                    "difficulty": "medium",
                    "quantity": 10,
                    "reason": "Practice with time constraints",
                })
            
            if not recommendations:
                recommendations.append({
                    "type": "mixed_practice",
                    "difficulty": "medium",
                    "quantity": 7,
                    "reason": "Balanced practice session",
                })
            
            return recommendations
        except Exception as e:
            logger.error(f"Failed to get practice recommendations: {e}")
            return []

    def _get_study_schedule_recommendations(self, personalization: Dict, user_data: Dict) -> Dict:
        try:
            preferred_time = personalization.get("preferred_study_time", "flexible")
            attention_span = personalization.get("attention_span_minutes", 30)
            learning_style = personalization.get("learning_style", "mixed")
            
            schedule = {
                "preferred_study_time": preferred_time,
                "session_duration": attention_span,
                "break_interval": max(attention_span // 3, 10),
                "learning_style_focus": learning_style,
                "daily_sessions": 3 if attention_span < 30 else 2,
            }
            
            return schedule
        except Exception as e:
            logger.error(f"Failed to get study schedule recommendations: {e}")
            return {
                "preferred_study_time": "flexible",
                "session_duration": 30,
                "break_interval": 10,
                "learning_style_focus": "mixed",
                "daily_sessions": 2,
            }

    def _get_difficulty_recommendations(self, personalization: Dict, user_data: Dict) -> Dict:
        try:
            confidence = personalization.get("confidence_level", 0.5)
            learning_speed = personalization.get("learning_speed", "moderate")
            
            if confidence < 0.4:
                difficulty = "easy"
                increment = 0.05
            elif confidence < 0.7:
                difficulty = "medium"
                increment = 0.1
            else:
                difficulty = "hard"
                increment = 0.15
            
            return {
                "current_difficulty": difficulty,
                "recommended_increment": increment,
                "adjustment_frequency": "weekly",
                "reason": f"Based on confidence level of {confidence:.2f}",
            }
        except Exception as e:
            logger.error(f"Failed to get difficulty recommendations: {e}")
            return {
                "current_difficulty": "medium",
                "recommended_increment": 0.1,
                "adjustment_frequency": "weekly",
                "reason": "Default recommendation",
            }

    def _get_resource_recommendations(self, personalization: Dict, user_data: Dict) -> List[Dict]:
        try:
            learning_style = personalization.get("learning_style", "mixed")
            knowledge_gaps = personalization.get("knowledge_gaps", [])
            
            resources = []
            
            style_resources = {
                "text": ["Textbooks", "Written tutorials", "Documentation"],
                "diagram": ["Infographics", "Mind maps", "Flowcharts"],
                "flashcards": ["Flashcard decks", "Spaced repetition apps"],
                "videos": ["Video lectures", "Tutorials", "Documentaries"],
                "practice_questions": ["Problem sets", "Quizzes", "Practice exams"],
                "mixed": ["Mixed media resources", "Interactive platforms"],
            }
            
            for resource in style_resources.get(learning_style, style_resources["mixed"]):
                resources.append({
                    "type": resource,
                    "recommended": True,
                    "reason": f"Matches {learning_style} learning style",
                })
            
            for gap in knowledge_gaps[:3]:
                resources.append({
                    "type": f"Targeted resources for {gap['topic']}",
                    "recommended": True,
                    "reason": "Address knowledge gap",
                })
            
            return resources
        except Exception as e:
            logger.error(f"Failed to get resource recommendations: {e}")
            return []

    def _get_default_recommendations(self) -> Dict:
        return {
            "topics_to_revise": [
                {
                    "topic": "General review",
                    "priority": "low",
                    "reason": "Default recommendation",
                    "suggested_time": 20,
                }
            ],
            "practice_questions": [
                {
                    "type": "mixed_practice",
                    "difficulty": "medium",
                    "quantity": 7,
                    "reason": "Default practice",
                }
            ],
            "study_schedule": {
                "preferred_study_time": "flexible",
                "session_duration": 30,
                "break_interval": 10,
                "learning_style_focus": "mixed",
                "daily_sessions": 2,
            },
            "difficulty_adjustment": {
                "current_difficulty": "medium",
                "recommended_increment": 0.1,
                "adjustment_frequency": "weekly",
                "reason": "Default",
            },
            "learning_resources": [
                {
                    "type": "Mixed media resources",
                    "recommended": True,
                    "reason": "Default",
                }
            ],
            "generated_at": datetime.utcnow().isoformat(),
            "confidence": 0.5,
        }

    def clear_cache(self, user_id: Optional[str] = None):
        try:
            if user_id:
                keys_to_remove = [k for k in self.recommendation_cache.keys() if k.startswith(user_id)]
                for key in keys_to_remove:
                    del self.recommendation_cache[key]
            else:
                self.recommendation_cache.clear()
            
            logger.info(f"Cleared recommendation cache for {user_id or 'all users'}")
        except Exception as e:
            logger.error(f"Failed to clear cache: {e}")


recommendation_engine = RecommendationEngine()
