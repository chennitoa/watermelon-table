import React, { useState, useEffect, useMemo } from 'react';
import {send_websocket_message, connect_to_room} from "../../script.js";
import { useParams, useLocation } from 'react-router-dom';
import { getUserWithUserId } from '../../client'
import Box from '@mui/material/Box';
import HeaderRAF from '../HeaderRAF';

const Chat = () => {
    const [message, setMessage] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const [serverMessages, setServerMessages] = useState([]);
    const location = useLocation();
    let receiverUsername = location.state.receiverUsername;
    const { senderId, receiverId } = useParams();

    useEffect(() => {
        const fetchProfile = async () => {
            try {
              const user = await getUserWithUserId();
            } catch (error) {
              console.error('Failed to fetch profile:', error);
            }
          };
        
        if (receiverUsername === null) {
            fetchProfile();
        }
        connect_to_room(senderId, receiverId, setServerMessages);
    }, []);

    const handleSendMessageFunction = (e) => {
        e.preventDefault();
        if (message.trim() !== "") {
            let success = send_websocket_message(message, senderId, receiverId);
            if (!success) {
                setErrorMessage('Failed to send message');
            } else {  
                setErrorMessage('');
            }
            setMessage('');
        }
    }

    const handleMessageChange = (event) => {
        setMessage(event.target.value);
    }
    
    const renderServerMessages = () => {
        // const receiverMessages = serverMessages.filter(message => message.user_id !== senderId);
        // return serverMessages.map((msg, index) => (
        //     <div key={index} className="message">
        //         {msg.message}
        //     </div>
        // ));
        return serverMessages.map((msg, index) => {
            const isCurrentUser = msg.user_id === senderId; // Change specificUserId to the ID you want to compare
            const messageClass = isCurrentUser ? "right-align" : "left-align";
            return (
                <div key={index} className={`message ${messageClass}`}>
                <span className="message-content">
                    {msg.message}
                </span>
            </div>
            );
        });
    };

    return (
        <React.Fragment>
            <Box display="flex" flexDirection="column" height="100%" sx={{backgroundColor: '#B3BFB8', minHeight: '100vh'}}>
            <HeaderRAF/>
                <style>
                    {`
                    .chat-container {
                        display: flex;
                        flex-direction: column;
                        justify-content: space-between;
                        height: 90vh;
                        max-height: 600px;
                        border-radius: 8px;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                        background-color: #fff;
                        padding: 20px;
                    }
                    #message-container {
                        flex: 1;
                        border: 1px solid #ccc;
                        border-radius: 8px;
                        overflow-y: auto;
                        padding: 10px;
                        margin-bottom: 10px;
                        display: inline-block;
                    }
                    .message {
                        margin-bottom: 5px;
                    }
                    
                    .right-align {
                        text-align: right;
                        color: #0066b2;
                    }
                    
                    .left-align {
                        text-align: left;
                        color: black;
                    }
                    
                    .message-content {
                        background-color: #f0f0f0;
                        border-radius: 8px;
                        padding: 5px;
                        display: inline-block; /* Adjusts the box to wrap around the text */
                    }
                    
                    .form-group {
                        display: flex;
                        align-items: center;
                        margin-bottom: 10px;
                    }
                    .form-group label {
                        margin-right: 10px;
                    }
                    .form-group input[type="text"] {
                        flex: 1;
                        padding: 8px;
                        border-radius: 5px;
                        border: 1px solid #ccc;
                    }
                    .form-group button {
                        padding: 8px 15px;
                        border: none;
                        border-radius: 5px;
                        background-color: #007bff;
                        color: #fff;
                        cursor: pointer;
                    }
                    `}
                </style>
                <title>Chat</title>
                {receiverUsername && <h1>&nbsp;{receiverUsername}</h1>}
                {errorMessage && ( <p className="error"> {errorMessage} </p> )}
                <div className="chat-container">
                    <div id="message-container">
                        {renderServerMessages()}
                    </div>
                    <form id="form" onSubmit={handleSendMessageFunction}>
                        <div className="form-group">
                            <label htmlFor="message-input">Message:</label>
                            <input type="text" value={message} onChange={handleMessageChange} id="message-input" />
                            <button type="button" id="send-button" onClick={handleSendMessageFunction}>Send</button>
                        </div>
                    </form>
                </div>
        </Box>
        </React.Fragment>
    )
}

export default Chat;