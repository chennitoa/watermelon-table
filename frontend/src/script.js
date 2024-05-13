let socket;
let room_socket;
export const connect_to_room = (sender, receiver, setServerMessages) => {
    socket = new WebSocket('ws://localhost:8001/connect-rooms/'+sender+"/"+receiver);
    
    socket.addEventListener('open', function (event) {
        console.log('WebSocket connection opened');
    });
    socket.addEventListener("message", (event) => {
        try {
            var eventDataObject = JSON.parse(JSON.parse(event.data.trim()));
        } catch (error) {
            console.log("Error parsing JSON", error);
        }
        const serverMessage = { user_id: eventDataObject.user_id, message: eventDataObject.message }
        setServerMessages(prevMessages => [...prevMessages, serverMessage]);
    });
    return true;
}

export const send_websocket_message = (message, sender, receiver) => {
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

export const get_rooms = (userId, setDirectMessages) => {
    room_socket = new WebSocket('ws://localhost:8001/get_rooms/'+userId);
    room_socket.addEventListener('open', function (event) {
        console.log('WebSocket connection opened');
    });

    room_socket.addEventListener("message", (event) => {
        console.log("Message from server ", event.data.trim());
        try {
            var eventDataObject = JSON.parse(JSON.parse(event.data.trim()));
        } catch (error) {
            console.log("Error parsing JSON", error);
        }
        const extractedRoomData = eventDataObject.map(obj => {
            return {
              room_tup: obj.room_tup,
            };
          });
        setDirectMessages(extractedRoomData);
    });

    return true;
}