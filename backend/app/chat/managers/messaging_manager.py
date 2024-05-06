"""
    Class to manage the messaging
"""
from fastapi import WebSocket
from fastapi.encoders import jsonable_encoder
from ..logger.logger import Logger
from ..models.chat_message import ChatMessage
from ..models.room import Room
from bson import json_util


class MessagingManager:
    '''
        Manages the active connections
    '''

    def __init__(self) -> None:
        '''
            Initializes the active connections
        '''
        self.active_connections: dict[str, set[WebSocket]] = {}
        self.logger = Logger("MessagingManager")


    async def connect(self, websocket: WebSocket, room: Room):
        '''
            Adds the connection to the active connections
        '''
        # Accept the user connection
        await websocket.accept()
        if room not in self.active_connections:
            self.active_connections[room] = set()
        
        if websocket in self.active_connections[room]:
            return True
        
        self.active_connections[room].add(websocket)
        return False
        

    def disconnect(self, websocket: WebSocket, room_id: str):
        '''
            Removes the connection from the active connections
        '''
        self.active_connections[room_id].remove(websocket)

    async def send_message_to(self, websocket: WebSocket, message: ChatMessage):
        '''
            Sends the message to a specific client
        '''
        json_message = json_util.dumps(message.to_dict())
        await websocket.send_json(json_message)

    async def broadcast(self, message: ChatMessage, room_id: str):
        '''
            Sends the message to all the clients
        '''
        self.logger.info(
            f"Broadcasting message to {len(self.active_connections[room_id])} clients")
        for connection in self.active_connections[room_id]:
            await self.send_message_to(connection, message)