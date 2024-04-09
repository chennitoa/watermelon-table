import React, { useState } from 'react';
import Typography from '@mui/material/Typography';
import HeaderRAF from './HeaderRAF';
import { useLocation } from 'react-router-dom';
import Grid from '@mui/material/Grid';
import StarRating from './StarRating';

const UserProfile = () => {
    const location = useLocation();
    const userData = location.state.userData;

    // State to manage the user's rating
    const [userRating, setUserRating] = useState(0);

    // Function to handle when the user rates
    const handleRatingChange = (newRating) => {
        setUserRating(newRating);
    };

    return (
        <div>
            <HeaderRAF />
            <div style={{ padding: '20px' }}>
                <Typography variant="h4">User Profile</Typography>
                <Grid container spacing={3} style={{ marginTop: '20px' }}>
                    {/* Personal Information */}
                    <Grid item xs={12} sm={6}>
                        <Typography variant="h5">Personal Information</Typography>
                        <div style={{ marginTop: '10px' }}>
                            <Typography variant="subtitle1">First Name: {userData.firstName}</Typography>
                            <Typography variant="subtitle1">Last Name: {userData.lastName}</Typography>
                            <Typography variant="subtitle1">Username: {userData.username}</Typography>
                            <Typography variant="subtitle1">Email: {userData.email}</Typography>
                        </div>
                    </Grid>
                    {/* Optional Information */}
                    <Grid item xs={12} sm={6}>
                        <Typography variant="h5">Optional Information</Typography>
                        <div style={{ marginTop: '10px' }}>
                            <Typography variant="subtitle1">Profile Picture:</Typography>
                            <img src={userData.picture} alt="Profile" style={{ maxWidth: '30%', marginTop: '5px' }} />
                            <Typography variant="subtitle1">Interests:</Typography>
                            <ul style={{ listStyleType: 'none', paddingLeft: 0 }}>
                                <li><Typography variant="subtitle1">1. {userData.interest1}</Typography></li>
                                <li><Typography variant="subtitle1">2. {userData.interest2}</Typography></li>
                                <li><Typography variant="subtitle1">3. {userData.interest3}</Typography></li>
                            </ul>
                            <Typography variant="subtitle1">Gender: {userData.gender}</Typography>
                        </div>
                    </Grid>
                    {/* Rating */}
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
}

export default UserProfile;
