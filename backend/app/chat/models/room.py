""" Model class for chat rooms """
import json
from bson import ObjectId, json_util
from pydantic import BaseModel

class Room (BaseModel):
    '''
        Room dataclass for the chat
    '''
    class Config:
        arbitrary_types_allowed = True

    room_id: ObjectId
    room_tup: list[str]
    name: str
    description: str

    def to_dict(self):
        '''
            Converts the room to a dictionary
        '''
        return {
            '_id': self.room_id,
            'room_tup': self.room_tup,
            'name': self.name,
            'description': self.description,
        }
    
    def get_id(self):
        return self.room_id
    
    def __str__(self):
        return self.to_dict()
    
    def __eq__(self, other):
        return self.room_id == other.room_id
    
    def __hash__(self):
        return hash(self.room_id)