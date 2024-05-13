"""
    Model class for chat messages
"""
from pydantic import BaseModel
from bson import ObjectId


class ChatMessage(BaseModel):
    '''
        Chat message dataclass
    '''
    class Config:
        arbitrary_types_allowed = True

    message_id: ObjectId
    user_id: str
    message: str
    room_id: ObjectId

    def to_dict(self) -> dict:
        '''
            Converts the dataclass to a dictionary
        '''
        return {
            '_id': self.message_id,
            'message': self.message,
            'user_id': self.user_id,
            'room_id': self.room_id
        }
