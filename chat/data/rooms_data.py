"""Module providing the RoomsData class to interact with the rooms data"""
import os
from ..models.room import Room
from ..logger.logger import Logger
from bson import ObjectId
from dotenv import load_dotenv
from pymongo.collection import Collection
from pymongo.mongo_client import MongoClient


class RoomsData:
    '''
    RoomsData class

    '''

    def __init__(self):
        load_dotenv()
        mongo_url = os.getenv("MONGO_URI")
        # use pymongo to connect to the database
        self.client = MongoClient(mongo_url)
        self.database = self.client["chat"]
        self.rooms_collection: Collection[Room] = self.database["rooms"]
        self.logger = Logger("RoomsData")
        # main_room = Room(name="General", description="General room")
        # self.add_room(main_room)

    def add_room(self, room_tup: list[str]) -> Room:
        '''
            Adds a room to the data base
        '''
        # use pymongo to insert the room to the database
        # ensure document is updated if it already exists
        self.logger.info("Searching for room in the database")
        try:
            if len(room_tup) != 2:
                self.logger.error("Invalid room")
                return None
            room_dict = self.rooms_collection.find_one({
                "room_tup": {
                    "$all": room_tup
                }
            })
            if not room_dict:
                room = Room(
                    room_id=ObjectId(),
                    room_tup=room_tup,
                    name=room_tup[0],
                    description="chat with " + room_tup[1]
                )
                self.rooms_collection.insert_one(
                    room.to_dict()
                )
                self.logger.info("Room added to the database")
            else:
                self.logger.info("Room found in the database")
                room = Room(room_id=room_dict["_id"],
                            room_tup=room_dict["room_tup"],
                            name=room_dict["name"],
                            description=room_dict["description"])
            return room.get_id()

        except Exception as error:
            self.logger.error(error)
            print("In error")
            return room.get_id()

    def get_all_sender_rooms(self, sender) -> list[Room]:
        '''
            Gets all rooms from the data base
        '''
        # use pymongo to get the room from the database
        try:
            self.logger.info("Getting all rooms of user id: " + sender + " from the database")
            rooms_cursor = self.rooms_collection.find({
                "room_tup": {
                    "$all": [sender]
                }
            })
            rooms = []
            for room_dict in rooms_cursor:
                room = Room(room_id=room_dict["_id"],
                            room_tup=room_dict["room_tup"],
                            name=room_dict["name"],
                            description=room_dict["description"])
                rooms.append(room.to_dict())
            return rooms
        except Exception as error:
            self.logger.error(error)
            return None
