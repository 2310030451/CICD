from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, Set
import json
from loguru import logger
from datetime import datetime

class ConnectionManager:
    """Manages WebSocket connections for real-time communication"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_rooms: Dict[str, Set[str]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: str):
        """Accept a new WebSocket connection"""
        await websocket.accept()
        self.active_connections[user_id] = websocket
        logger.info(f"User {user_id} connected via WebSocket")
        
        # Send welcome message
        await self.send_personal_message({
            "type": "connected",
            "message": "Successfully connected to NeuroLearn AI",
            "timestamp": datetime.utcnow().isoformat()
        }, user_id)
    
    def disconnect(self, user_id: str):
        """Remove a WebSocket connection"""
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            logger.info(f"User {user_id} disconnected from WebSocket")
        
        # Remove user from all rooms
        if user_id in self.user_rooms:
            del self.user_rooms[user_id]
    
    async def send_personal_message(self, message: dict, user_id: str):
        """Send a message to a specific user"""
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_json(message)
            except Exception as e:
                logger.error(f"Failed to send message to user {user_id}: {e}")
                self.disconnect(user_id)
    
    async def broadcast(self, message: dict, room_id: str = None):
        """Broadcast a message to all users or users in a specific room"""
        if room_id:
            # Send to users in the room
            for user_id, rooms in self.user_rooms.items():
                if room_id in rooms and user_id in self.active_connections:
                    await self.send_personal_message(message, user_id)
        else:
            # Send to all connected users
            for user_id in self.active_connections:
                await self.send_personal_message(message, user_id)
    
    def join_room(self, user_id: str, room_id: str):
        """Add a user to a room"""
        if user_id not in self.user_rooms:
            self.user_rooms[user_id] = set()
        self.user_rooms[user_id].add(room_id)
        logger.info(f"User {user_id} joined room {room_id}")
    
    def leave_room(self, user_id: str, room_id: str):
        """Remove a user from a room"""
        if user_id in self.user_rooms and room_id in self.user_rooms[user_id]:
            self.user_rooms[user_id].remove(room_id)
            logger.info(f"User {user_id} left room {room_id}")

# Global connection manager instance
manager = ConnectionManager()

async def handle_websocket_connection(websocket: WebSocket, user_id: str):
    """Handle WebSocket connection lifecycle"""
    await manager.connect(websocket, user_id)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            
            # Handle different message types
            message_type = data.get("type")
            
            if message_type == "join_room":
                room_id = data.get("room_id")
                if room_id:
                    manager.join_room(user_id, room_id)
                    await manager.send_personal_message({
                        "type": "room_joined",
                        "room_id": room_id,
                        "timestamp": datetime.utcnow().isoformat()
                    }, user_id)
            
            elif message_type == "leave_room":
                room_id = data.get("room_id")
                if room_id:
                    manager.leave_room(user_id, room_id)
                    await manager.send_personal_message({
                        "type": "room_left",
                        "room_id": room_id,
                        "timestamp": datetime.utcnow().isoformat()
                    }, user_id)
            
            elif message_type == "chat_message":
                # Handle chat messages
                room_id = data.get("room_id")
                message = data.get("message")
                
                await manager.broadcast({
                    "type": "chat_message",
                    "user_id": user_id,
                    "message": message,
                    "room_id": room_id,
                    "timestamp": datetime.utcnow().isoformat()
                }, room_id)
            
            elif message_type == "typing":
                # Handle typing indicators
                room_id = data.get("room_id")
                is_typing = data.get("is_typing", False)
                
                await manager.broadcast({
                    "type": "typing",
                    "user_id": user_id,
                    "is_typing": is_typing,
                    "room_id": room_id,
                    "timestamp": datetime.utcnow().isoformat()
                }, room_id)
            
            elif message_type == "ping":
                # Respond to ping with pong
                await manager.send_personal_message({
                    "type": "pong",
                    "timestamp": datetime.utcnow().isoformat()
                }, user_id)
    
    except WebSocketDisconnect:
        manager.disconnect(user_id)
        logger.info(f"WebSocket disconnected for user {user_id}")
    
    except Exception as e:
        logger.error(f"WebSocket error for user {user_id}: {e}")
        manager.disconnect(user_id)

async def send_notification(user_id: str, notification: dict):
    """Send a real-time notification to a user"""
    await manager.send_personal_message({
        "type": "notification",
        "data": notification,
        "timestamp": datetime.utcnow().isoformat()
    }, user_id)

async def send_system_update(message: str):
    """Broadcast a system update to all users"""
    await manager.broadcast({
        "type": "system_update",
        "message": message,
        "timestamp": datetime.utcnow().isoformat()
    })
