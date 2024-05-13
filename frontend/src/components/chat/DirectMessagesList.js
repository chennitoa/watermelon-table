import React, { useState, useEffect } from 'react';
import { get_rooms } from "../../script.js";
import { useParams } from 'react-router-dom';
import DirectMessageBox from './DirectMessageBox'; // Import the DirectMessageBox component
import HeaderRAF from "../HeaderRAF";
import Box from "@mui/material/Box";


const DirectMessagesList = () => {
    const [directMessages, setDirectMessages] = useState({});
    const { userId } = useParams();

    useEffect(() => {
        const fetch_rooms = (userId, setDirectMessages) => { 
            try {
                get_rooms(userId, setDirectMessages);
            } catch (error) {
                console.error('Failed to fetch direct messages:', error);
            }
        }
        fetch_rooms(userId, setDirectMessages);
    }, [userId]);

    return (
        <React.Fragment>
        <Box display="flex" flexDirection="column" height="100%" sx={{backgroundColor: '#B3BFB8', minHeight: '100vh'}}>
            <HeaderRAF/>
            <title>DMs</title>
            <h1>&nbsp;&nbsp;Chats</h1>
            <div className="chat-container">
                <div id="message-container">
                    {directMessages && directMessages.length > 0 ? (
                        directMessages.map((msg, index) => {
                            const otherUserId = msg.room_tup.filter(id => id !== userId);
                            return (
                                <DirectMessageBox
                                    key={index}
                                    currUserId={userId}
                                    otherUserId={otherUserId}
                                />
                            );
                        })
                    ) : (
                        <div>&nbsp;&nbsp;&nbsp;&nbsp;<font size="+15">No messages</font></div>
                    )}
                </div>
            </div>
        </Box>
        </React.Fragment>

    )
}

export default DirectMessagesList;

