import React, { useState, useEffect } from 'react';
import { getUserWithUserId, getProfile} from '../../client';
import Avatar from "@mui/material/Avatar";
import { useNavigate } from 'react-router-dom';

const DirectMessageBox = ({ currUserId, otherUserId }) => {
    const [otherUsername, setOtherUsername] = useState("");
    const [profilePicture, setProfilePicture] = useState("");
    const navigate = useNavigate();

    useEffect(() => {
        const fetchProfile = async () => {
            try {
                const user = await getUserWithUserId(otherUserId);
                setOtherUsername(user.result.username);

                const data = await getProfile(user.result.username);
                if (data.result.profile_picture !== "") {
                    setProfilePicture(data["result"].profile_picture);
                }
            } catch (error) {
                console.error('Failed to fetch profile:', error);
            }
        };
        fetchProfile();
    }, [otherUserId]);

    const handleMessage = () => {
        if (currUserId === otherUserId) {
            return;
        }
        navigate(`/chat/${currUserId}/${otherUserId}`, { state: { receiverUsername: otherUsername }});
    }

    return (

        <div style={styles.container}>
            <div style={styles.messageBox} onClick={handleMessage}>
                {<Avatar src={profilePicture} alt="Profile Picture" sx={styles.profilePicture} />}
                <div style={styles.username}>{otherUsername}</div>
                {/* Add additional message content here */}
            </div>
        </div>
    );
};

const styles = {
    container: {
        display: 'flex',
        justifyContent: 'flex-start',
        padding: '10px',
    },
    messageBox: {
        backgroundColor: 'rgba(0, 132, 255, 0.7)',
        color: 'white',
        padding: '20px',
        borderRadius: '30px',
        boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.1)',
        width: '80%',
        maxWidth: '500px',
        cursor: 'pointer',
        transition: 'background-color 0.3s',
        display: 'flex',
        alignItems: 'center', // Center align items vertically
    },
    profilePicture: {
        marginRight: '10px',
        width: '50px', // Adjust size as needed
        height: '50px', // Adjust size as needed
        borderRadius: '50%', // Make it round
        maxWidth: "100%", 
        marginTop: "1rem"
    },
    username: {
        fontWeight: 'bold',
        marginBottom: '10px',
    },
};

export default DirectMessageBox;
