
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from .models.chat_message import ChatMessage
from .managers.rooms_manager import RoomsManager
from .managers.messaging_manager import MessagingManager
from .logger.logger import Logger
from .data.rooms_data import RoomsData
from .data.messaging_data import MessageData
from bson import ObjectId
import asyncio
from bson import json_util

app = FastAPI()
origins = [
    "http://localhost:8001",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Creating the managers
chat_manager = MessagingManager()
rooms_manager = RoomsManager()

# Creating the data
rooms_data = RoomsData()
messages_data = MessageData()

# Creating the logger
api_logger = Logger("API")


async def handle_add_room(room_tup: list[str]):
    '''
        Function to handle new room created by a client
    '''
    room = rooms_data.add_room(room_tup)
    if room:
        return room
    else:
        return None


@app.websocket("/rooms")
async def handle_new_connection_rooms(websocket: WebSocket):
    '''
        Function to handle new connections to the rooms
        The function accepts the connection from the client
        and sends all the available rooms to the client
    '''
    try:
        await rooms_manager.add_rooms_listner(websocket)
        rooms = rooms_data.get_all_rooms()
        api_logger.info(f"Sending rooms: {len(rooms)}")
        for room in rooms:
            await rooms_manager.send_room_to(websocket, room)
        while True:
            # we keep the connection alive
            # when a new room is created by a client
            # we broadcast the new room to all the clients
            await asyncio.sleep(1)

    except WebSocketDisconnect:
        await rooms_manager.remove_rooms_listner(websocket)


@app.websocket("/connect-rooms/{sender}/{receiver}")
async def handle_connect_to_room(websocket: WebSocket, sender: str, receiver: str):
    '''
        The function accepts the connection from the client
        and sends the messages to the clients of a specific room
    '''
    room_tup = [sender, receiver]
    room_id = await handle_add_room(room_tup)

    # Accept the connection from the client
    already_connected = await chat_manager.connect(websocket, room_id)

    if not already_connected:
        # Sending the messages to the new client
        messages = messages_data.get_messages_of(room_id)

        api_logger.info("Sending all messages to new client")
        for message in messages:
            await chat_manager.send_message_to(websocket, message)
    try:
        while True:
            # Receive the message from the client
            data = await websocket.receive_json()
            api_logger.info(f"Received \"{data}\"")

            if "type" in data and data["type"] == "close":
                chat_manager.disconnect(websocket, room_id)
            else:
                message = ChatMessage(
                    message_id=ObjectId(),
                    user_id=sender,
                    message=data["message"],
                    room_id=room_id
                )
                messages_data.add_message(message)

                # Send the message to all the clients
                await chat_manager.broadcast(message, room_id)

    except WebSocketDisconnect:
        # Remove the connection from the list of active connections
        api_logger.info("Client disconnected")
        chat_manager.disconnect(websocket, room_id)


@app.websocket("/get_rooms/{user_id}")
async def get_rooms(websocket: WebSocket, user_id: str):
    '''
        Function to get all the rooms of a user
    '''
    await websocket.accept()
    rooms = rooms_data.get_all_sender_rooms(user_id)
    await websocket.send_json(json_util.dumps(rooms))
    return rooms
