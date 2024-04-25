import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getProfile, getUser } from '../client'; // Adjust the import path as necessary
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';
import HeaderRAF from './HeaderRAF';
import StarRating from './StarRating';

const UserProfile = () => {
    const { username } = useParams(); // This assumes your route is defined as /profile/:username
    const [profileData, setProfileData] = useState(null);
    const [userData, setUserData] = useState(null);
    const [userRating, setUserRating] = useState(0);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const data = await getProfile(username);
                setProfileData(data['result']);
                const data2 = await getUser(username);
                setUserData(data2['result']);

            } catch (error) {
                console.error('Failed to fetch user data:', error);
                // Optionally handle the error, e.g., show an error message
            }
        };

        fetchData();
    }, [username]);

    const handleRatingChange = (newRating) => {
        setUserRating(newRating);
    };

    if (!userData || !profileData) {
        return <div>Loading...</div>; // Or any other loading state representation
    }

    return (
        <div>
            <HeaderRAF />
            <div style={{ padding: '20px' }}>
                <Typography variant="h4">User Profile</Typography>
                <Grid container spacing={3} style={{ marginTop: '20px' }}>
                    <Grid item xs={12} sm={6}>
                        <Typography variant="h5">Personal Information</Typography>
                        <div style={{ marginTop: '10px' }}>
                            <Typography variant="subtitle1">First Name: {userData.first_name}</Typography>
                            <Typography variant="subtitle1">Last Name: {userData.last_name}</Typography>
                            <Typography variant="subtitle1">Username: {userData.username}</Typography>
                            <Typography variant="subtitle1">Email: {userData.email}</Typography>
                        </div>
                    </Grid>
                    <Grid item xs={12} sm={6}>
                        <Typography variant="h5">Optional Information</Typography>
                        <div style={{ marginTop: '10px' }}>
                            <Typography variant="subtitle1">Profile Picture:</Typography>
                            <img src={profileData.profile_picture} alt="Profile" style={{ maxWidth: '30%', marginTop: '5px' }} />
                            <Typography variant="subtitle1">Interests:</Typography>
                            <ul style={{ listStyleType: 'none', paddingLeft: 0 }}>
                                <li><Typography variant="subtitle1">1. {profileData.interest1}</Typography></li>
                                <li><Typography variant="subtitle1">2. {profileData.interest2}</Typography></li>
                                <li><Typography variant="subtitle1">3. {profileData.interest3}</Typography></li>
                            </ul>
                            <Typography variant="subtitle1">Gender: {profileData.gender}</Typography>
                        </div>
                    </Grid>
                    <Grid item xs={12}>
                        <Typography variant="h5">Rating</Typography>
                        <div style={{ marginTop: '10px' }}>
                            <StarRating value={userRating} onRatingChange={handleRatingChange} />
                        </div>
                    </Grid>
                </Grid>
            </div>
        </div>
    );
};

export default UserProfile;