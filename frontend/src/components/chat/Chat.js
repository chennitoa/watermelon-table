import React, { useState, useEffect } from 'react';
import {send_websocket_message, connect_to_room} from "../../script.js";

const Chat = (props) => {
    const [message, setMessage] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const [serverMessages, setServerMessages] = useState([]);

    useEffect(() => {
        connect_to_room(props.sender, props.receiver, setServerMessages);
    }, []);

    const handleSendMessageFunction = (e) => {
        e.preventDefault();
        if (message.trim() !== "") {
            let success = send_websocket_message(message, props.sender, props.receiver);
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
        return serverMessages.map((msg, index) => (
            <div key={index} className="message">
                {msg}
            </div>
        ));
    };

    return (
        <React.Fragment>
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
                }
                .message {
                    background-color: #f0f0f0;
                    border-radius: 8px;
                    padding: 5px;
                    margin-bottom: 5px;
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
            <h1>{props.username}</h1>
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
        </React.Fragment>
    )
}

export default Chat;
