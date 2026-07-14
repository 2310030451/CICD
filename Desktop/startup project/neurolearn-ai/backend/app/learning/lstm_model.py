import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from app.config import settings
from loguru import logger
import os
from datetime import datetime, timedelta


class LearningPredictor:
    def __init__(self):
        self._initialized = False
        self.model = None
        self.scaler = None
        self.sequence_length = settings.lstm_sequence_length
        self.prediction_horizon = settings.lstm_prediction_horizon
        self.feature_columns = [
            "study_duration",
            "quiz_score",
            "time_per_topic",
            "correct_answers",
            "wrong_answers",
            "revision_frequency",
            "assignment_completion",
            "login_frequency",
            "learning_streak",
            "chat_interactions",
        ]
        self.target_columns = [
            "expected_exam_score",
            "weak_topic_score",
            "strong_topic_score",
            "forgetting_probability",
            "failing_risk",
        ]
        self.model_path = "./models/lstm_learning_predictor.h5"
        self.scaler_path = "./models/lstm_scaler.pkl"

    def _ensure_initialized(self):
        """Lazy initialization to avoid startup errors"""
        if self._initialized:
            return
        
        try:
            from sklearn.preprocessing import MinMaxScaler
            import joblib
            
            self.scaler = MinMaxScaler()
            
            if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
                self._load_model()
                logger.info("Loaded existing LSTM model")
            else:
                self._build_model()
                logger.info("Built new LSTM model")
            
            self._initialized = True
        except ImportError as e:
            logger.error(f"TensorFlow/sklearn not available: {e}")
            self._initialized = False
        except Exception as e:
            logger.error(f"Failed to initialize LSTM model: {e}")
            self._initialized = False

    def _build_model(self):
        try:
            from tensorflow.keras.models import Sequential
            from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization
            from tensorflow.keras.optimizers import Adam
            
            self.model = Sequential([
                LSTM(128, return_sequences=True, input_shape=(self.sequence_length, len(self.feature_columns))),
                Dropout(0.2),
                BatchNormalization(),
                LSTM(64, return_sequences=True),
                Dropout(0.2),
                BatchNormalization(),
                LSTM(32),
                Dropout(0.2),
                Dense(64, activation='relu'),
                Dropout(0.1),
                Dense(len(self.target_columns), activation='sigmoid'),
            ])
            
            optimizer = Adam(learning_rate=0.001)
            self.model.compile(
                optimizer=optimizer,
                loss='mse',
                metrics=['mae']
            )
            
            logger.info("LSTM model built successfully")
        except Exception as e:
            logger.error(f"Failed to build LSTM model: {e}")
            raise

    def _load_model(self):
        try:
            import joblib
            self.model.load_weights(self.model_path)
            self.scaler = joblib.load(self.scaler_path)
            logger.info("LSTM model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load LSTM model: {e}")
            raise

    def _save_model(self):
        try:
            import joblib
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            self.model.save_weights(self.model_path)
            joblib.dump(self.scaler, self.scaler_path)
            logger.info("LSTM model saved successfully")
        except Exception as e:
            logger.error(f"Failed to save LSTM model: {e}")
            raise

    def prepare_sequences(self, data: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        try:
            self._ensure_initialized()
            
            data = data[self.feature_columns + self.target_columns].copy()
            data = data.fillna(0)
            
            scaled_data = self.scaler.fit_transform(data)
            
            X, y = [], []
            for i in range(len(scaled_data) - self.sequence_length - self.prediction_horizon):
                X.append(scaled_data[i:i + self.sequence_length, :len(self.feature_columns)])
                y.append(scaled_data[i + self.sequence_length:i + self.sequence_length + self.prediction_horizon, len(self.feature_columns):])
            
            X = np.array(X)
            y = np.array(y)
            
            y = np.mean(y, axis=1)
            
            return X, y
        except Exception as e:
            logger.error(f"Failed to prepare sequences: {e}")
            raise

    def train(self, data: pd.DataFrame):
        try:
            self._ensure_initialized()
            
            if not self._initialized:
                raise RuntimeError("LSTM model is not available")
                
            if len(data) < settings.min_training_samples:
                logger.warning(f"Insufficient training samples: {len(data)} < {settings.min_training_samples}")
                return
            
            from sklearn.model_selection import train_test_split
            from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
            
            X, y = self.prepare_sequences(data)
            
            X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
            
            early_stopping = EarlyStopping(
                monitor='val_loss',
                patience=10,
                restore_best_weights=True
            )
            
            model_checkpoint = ModelCheckpoint(
                self.model_path,
                monitor='val_loss',
                save_best_only=True,
                save_weights_only=True
            )
            
            history = self.model.fit(
                X_train, y_train,
                validation_data=(X_val, y_val),
                epochs=100,
                batch_size=32,
                callbacks=[early_stopping, model_checkpoint],
                verbose=1
            )
            
            self._save_model()
            
            logger.info(f"LSTM model trained successfully. Final loss: {history.history['loss'][-1]:.4f}")
            
            return history
        except Exception as e:
            logger.error(f"Failed to train LSTM model: {e}")
            raise

    def predict(self, recent_data: pd.DataFrame) -> Dict[str, any]:
        try:
            self._ensure_initialized()
            
            if not self._initialized:
                logger.warning("LSTM model not available, returning default prediction")
                return self._get_default_prediction()
                
            if len(recent_data) < self.sequence_length:
                logger.warning(f"Insufficient data for prediction: {len(recent_data)} < {self.sequence_length}")
                return self._get_default_prediction()
            
            data = recent_data[self.feature_columns].copy()
            data = data.fillna(0)
            
            scaled_data = self.scaler.transform(data)
            
            X = scaled_data[-self.sequence_length:].reshape(1, self.sequence_length, len(self.feature_columns))
            
            predictions = self.model.predict(X, verbose=0)[0]
            
            result = {
                "expected_exam_score": float(predictions[0] * 100),
                "weak_topic_score": float(predictions[1] * 100),
                "strong_topic_score": float(predictions[2] * 100),
                "forgetting_probability": float(predictions[3]),
                "failing_risk": float(predictions[4]),
                "learning_speed": self._calculate_learning_speed(recent_data),
                "future_trend": self._calculate_trend(recent_data),
                "recommended_revision_time": self._calculate_revision_time(predictions),
                "confidence": 0.85,
                "prediction_date": datetime.utcnow().isoformat(),
            }
            
            return result
        except Exception as e:
            logger.error(f"Failed to make prediction: {e}")
            return self._get_default_prediction()

    def _calculate_learning_speed(self, data: pd.DataFrame) -> str:
        try:
            recent_scores = data["quiz_score"].tail(10)
            if len(recent_scores) < 2:
                return "moderate"
            
            improvement = recent_scores.iloc[-1] - recent_scores.iloc[0]
            
            if improvement > 10:
                return "fast"
            elif improvement > 5:
                return "moderate"
            elif improvement > 0:
                return "slow"
            else:
                return "declining"
        except Exception as e:
            logger.error(f"Failed to calculate learning speed: {e}")
            return "moderate"

    def _calculate_trend(self, data: pd.DataFrame) -> str:
        try:
            recent_scores = data["quiz_score"].tail(7)
            if len(recent_scores) < 3:
                return "stable"
            
            trend = np.polyfit(range(len(recent_scores)), recent_scores, 1)[0]
            
            if trend > 1:
                return "improving"
            elif trend < -1:
                return "declining"
            else:
                return "stable"
        except Exception as e:
            logger.error(f"Failed to calculate trend: {e}")
            return "stable"

    def _calculate_revision_time(self, predictions: np.ndarray) -> int:
        try:
            forgetting_prob = predictions[3]
            weak_score = predictions[1]
            
            if forgetting_prob > 0.7 or weak_score < 0.4:
                return 60
            elif forgetting_prob > 0.5 or weak_score < 0.6:
                return 45
            else:
                return 30
        except Exception as e:
            logger.error(f"Failed to calculate revision time: {e}")
            return 30

    def _get_default_prediction(self) -> Dict[str, any]:
        return {
            "expected_exam_score": 70.0,
            "weak_topic_score": 50.0,
            "strong_topic_score": 80.0,
            "forgetting_probability": 0.3,
            "failing_risk": 0.2,
            "learning_speed": "moderate",
            "future_trend": "stable",
            "recommended_revision_time": 30,
            "confidence": 0.5,
            "prediction_date": datetime.utcnow().isoformat(),
        }

    def retrain_if_needed(self, data: pd.DataFrame, last_retrain_date: Optional[datetime] = None):
        try:
            if not settings.lstm_model_enabled:
                logger.info("LSTM model training is disabled")
                return False
            
            if last_retrain_date:
                days_since_retrain = (datetime.utcnow() - last_retrain_date).days
                if days_since_retrain < settings.retrain_interval_days:
                    logger.info(f"Retrain not needed. Days since last retrain: {days_since_retrain}")
                    return False
            
            if len(data) >= settings.min_training_samples:
                logger.info("Retraining LSTM model...")
                self.train(data)
                return True
            else:
                logger.warning(f"Insufficient data for retraining: {len(data)} < {settings.min_training_samples}")
                return False
        except Exception as e:
            logger.error(f"Failed to retrain model: {e}")
            return False


learning_predictor = LearningPredictor()
