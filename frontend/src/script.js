let socket;
export const connect_to_room = (sender, receiver, setServerMessages) => {
    // sender = "b129u31029";
    // receiver = "j1fenw4";
    
    socket = new WebSocket('ws://localhost:8001/connect-rooms/'+sender+"/"+receiver);
    socket.addEventListener('open', function (event) {
        console.log('WebSocket connection opened');
    });
    socket.addEventListener("message", (event) => {
        console.log("Message from server ", event.data.trim());
        try {
            var eventDataObject = JSON.parse(JSON.parse(event.data.trim()));
        } catch (error) {
            console.log("Error parsing JSON", error);
        }
        setServerMessages(prevMessages => [...prevMessages, eventDataObject.message]);
    });
    return true;
}

export const send_websocket_message = (message, sender, receiver) => {
    // const sender = "newUser1231";
    // const reciever = "newReceiever12312";
    if (!socket || socket.readyState !== WebSocket.OPEN) {
        console.log('WebSocket connection not open.');
        return false;
    }

    console.log("Sending message...")
    const msg = JSON.stringify({
            message: message
        })
    socket.send(msg)
    return true;
}
