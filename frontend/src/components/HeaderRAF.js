import React, { useState, useEffect } from "react";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Avatar from "@mui/material/Avatar";
import MessageIcon from "@mui/icons-material/Message";
import Tooltip from "@mui/material/Tooltip";
import { Link } from "react-router-dom";
import { getCurrentUser, getProfile } from "../client";

function HeaderRAF() {
  const [currentUsername, setUsername] = useState('');
  const [currentUserId, setUserId] = useState(0);
  const [profilePicture, setProfilePicture] = useState('');
  const [loggedIn, setLoggedIn] = useState(false);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const user = await getCurrentUser(); 
        console.log(user);
        if (user["detail"]) { // failed login
          setLoggedIn(false);
        }
        else {
          setLoggedIn(true);
          setUsername(user.username);
          setUserId(user.user_id);
          const data = await getProfile(user.username);
          setProfilePicture(data['result']['profile_picture']);
        }      
      } catch (error) {
        console.error('Failed to fetch profile:', error);
      }
    };

    fetchUser();
  }, []);

  console.log(loggedIn);

  const handleSignOut = () => {
    // Clear access token from localStorage
    console.log(localStorage.getItem('token'));
    localStorage.removeItem('token');
    const accessToken = localStorage.getItem('token');
    console.log(accessToken);
    // You may want to redirect the user to the sign-in page or perform other actions after signing out
  };

  return (
    <Box
      p={2}
      display="flex"
      justifyContent="space-between"
      alignItems="center"
      sx={{ backgroundColor: '#B3BFB8' }} // Background color set to light shade of orange
    >
      <Box sx={{ display: 'flex', alignItems: 'center' }}>
        {loggedIn ? (
          <Button component={Link} to={`/dms/${currentUserId}`} variant="contained" startIcon={<MessageIcon />}>
            My DMs
          </Button>
        ) : (
          <Tooltip title="Sign up or login to access DMs">
            <span>
              <Button disabled variant="contained">
                My DMs
              </Button>
            </span>
          </Tooltip>
        )}
        <Button component={Link} to="/listings" variant="contained">
          Listings
        </Button>
      </Box>
      <Typography
        variant="h1"
        sx={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          textAlign: "center",
          justifyContent: "center", // Center horizontally
          height: "100%", // Take up full height of parent container
        }}
      >
        <Typography
          component="h1"
          variant="h1"
          sx={{
            paddingLeft: "70px",
            display: "flex",
            flexDirection: { xs: "column", md: "row" },
            alignSelf: "center",
            textAlign: "center",
          }}
        >
          Rent a&nbsp;
          <Typography component="span" variant="h1" color="primary.main">
            Lackey
          </Typography>
        </Typography>
      </Typography>
      <Box sx={{ display: 'flex', alignItems: 'center' }}>
        {!loggedIn && <Button component={Link} to="/" variant="contained" >Home</Button>}
        {!loggedIn && <Button component={Link} to="/sign-in" variant="contained" >Sign In</Button>}
        {!loggedIn && <Button component={Link} to="/sign-up" variant="contained" >Sign Up</Button>}
    
        {loggedIn && <Button component={Link} to={`/profile/${currentUsername}`} variant="contained" startIcon={<Avatar src={profilePicture}/>}>{currentUsername}</Button>}
        {loggedIn && <Button onClick={handleSignOut} component={Link} to="/" variant="contained" >Sign Out</Button>}
        {/* delete the session/access token */}
      </Box>
    </Box>
  );
}

export default HeaderRAF;
