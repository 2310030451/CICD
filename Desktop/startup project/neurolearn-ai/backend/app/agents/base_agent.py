from abc import ABC, abstractmethod
from typing import Dict, List, Optional, AsyncGenerator
from datetime import datetime
from app.config import settings
from loguru import logger
from cryptography.fernet import Fernet
import os


class BaseAgent(ABC):
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.memory = []
        self.tools = []
        self.prompt_template = ""
        self.system_prompt = ""
        self.max_memory_tokens = settings.agent_max_memory_tokens
        self.encryption_key = os.getenv("AGENT_ENCRYPTION_KEY", Fernet.generate_key())
        self.cipher = Fernet(self.encryption_key) if settings.agent_memory_encryption else None
        self.last_used = None

    @abstractmethod
    def get_system_prompt(self) -> str:
        pass

    @abstractmethod
    async def process(self, input_data: Dict, context: Optional[Dict] = None) -> Dict:
        pass

    @abstractmethod
    def get_tools(self) -> List[Dict]:
        pass

    def add_to_memory(self, memory_item: Dict):
        try:
            memory_item["timestamp"] = datetime.utcnow().isoformat()
            memory_item["agent"] = self.name
            
            if self.cipher:
                encrypted_memory = self._encrypt_memory(memory_item)
                self.memory.append(encrypted_memory)
            else:
                self.memory.append(memory_item)
            
            if len(self.memory) > 100:
                self.memory = self.memory[-100:]
            
            logger.info(f"Added memory item to {self.name} agent")
        except Exception as e:
            logger.error(f"Failed to add memory to {self.name}: {e}")

    def get_memory(self, limit: int = 10) -> List[Dict]:
        try:
            recent_memory = self.memory[-limit:]
            
            if self.cipher:
                decrypted_memory = [self._decrypt_memory(item) for item in recent_memory]
                return [item for item in decrypted_memory if item is not None]
            
            return recent_memory
        except Exception as e:
            logger.error(f"Failed to get memory from {self.name}: {e}")
            return []

    def clear_memory(self):
        try:
            self.memory = []
            logger.info(f"Cleared memory for {self.name} agent")
        except Exception as e:
            logger.error(f"Failed to clear memory for {self.name}: {e}")

    def _encrypt_memory(self, data: Dict) -> str:
        try:
            import json
            json_data = json.dumps(data).encode()
            encrypted = self.cipher.encrypt(json_data)
            return encrypted.decode()
        except Exception as e:
            logger.error(f"Failed to encrypt memory: {e}")
            return json.dumps(data)

    def _decrypt_memory(self, encrypted_data: str) -> Optional[Dict]:
        try:
            import json
            decrypted = self.cipher.decrypt(encrypted_data.encode())
            return json.loads(decrypted.decode())
        except Exception as e:
            logger.error(f"Failed to decrypt memory: {e}")
            return None

    def format_memory_for_context(self) -> str:
        try:
            memory_items = self.get_memory(5)
            if not memory_items:
                return ""
            
            memory_text = "Recent interactions:\n"
            for item in memory_items:
                memory_text += f"- {item.get('timestamp', '')}: {item.get('content', '')}\n"
            
            return memory_text
        except Exception as e:
            logger.error(f"Failed to format memory: {e}")
            return ""

    def update_last_used(self):
        self.last_used = datetime.utcnow()

    def get_usage_stats(self) -> Dict:
        return {
            "name": self.name,
            "role": self.role,
            "memory_size": len(self.memory),
            "last_used": self.last_used.isoformat() if self.last_used else None,
            "tools_count": len(self.tools),
        }
