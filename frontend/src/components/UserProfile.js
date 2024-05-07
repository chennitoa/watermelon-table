import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { getProfile, getUserWithUsername, updateProfile, getCurrentUser, getAllRatings, getUserRating, rateProfile } from "../client"; // Adjust the import path as necessary
import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Grid";
import Avatar from "@mui/material/Avatar";
import Paper from "@mui/material/Paper";
import Button from "@mui/material/Button";
import HeaderRAF from "./HeaderRAF";
import Box from "@mui/material/Box";
import Chip from "@mui/material/Chip";
import Divider from "@mui/material/Divider";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import TextField from "@mui/material/TextField";
import { MenuItem, Alert } from "@mui/material";
import RatingCard from "./RatingCard";
import { FaStar } from "react-icons/fa";

function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <Typography
      component="div"
      role="tabpanel"
      hidden={value !== index}
      id={`tabpanel-${index}`}
      aria-labelledby={`tab-${index}`}
      {...other}
    >
      {value === index && <Box p={3}>{children}</Box>}
    </Typography>
  );
}

const UserProfile = () => {
  const { username } = useParams(); // This assumes your route is defined as /profile/:username
  const [loggedInUser, setLoggedInUser] = useState("");
  const [realPreviewUrl, setPreviewUrl] = useState(""); // State to store previewUrl
  const [profileData, setProfileData] = useState(null);
  const [userData, setUserData] = useState(null);
  const [tabValue, setTabValue] = useState("profile");
  const [confirmationMessage, setConfirmationMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [allRatings, setAllRatings] = useState(null);
  const [userRating, setUserRating] = useState(null);
  const [postRating, setPostRating] = useState(1);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await getProfile(username);
        setProfileData(data["result"]);
        console.log(username);
        if (data["result"].profile_picture) {
            setPreviewUrl(data["result"].profile_picture); // Set the initial profile picture as default
        }
        const data2 = await getUserWithUsername(username);
        setUserData(data2["result"]);
        const user = await getCurrentUser();
        setLoggedInUser(user.username);
        const ratings = await getAllRatings(username);
        setAllRatings(ratings["result"]);
        console.log(ratings["result"]);
        const userrating = await getUserRating(username);
        setUserRating(userrating["result"]);
        
      } catch (error) {
        console.error("Failed to fetch user data:", error);
        // Optionally handle the error, e.g., show an error message
      }
    };

    fetchData();
  }, [username]);

  useEffect(() => {
    const confirmationTimeout = setTimeout(() => {
      setConfirmationMessage('');
    }, 5000);
  
    const errorTimeout = setTimeout(() => {
      setErrorMessage('');
    }, 5000);
  
    return () => {
      clearTimeout(confirmationTimeout);
      clearTimeout(errorTimeout);
    };
  }, [confirmationMessage, errorMessage]);

  if (!userData || !profileData) {
    return <div>Loading...</div>; // Or any other loading state representation
  }

  const isMyProfile = loggedInUser === username;
  const isOtherUser = !isMyProfile && loggedInUser !== "";

  const handleSubmit = async (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);

    const profileData = {
      username: username,
      description: data.get("description"),
      profile_picture: realPreviewUrl,
      interest1: data.get("interest1"),
      interest2: data.get("interest2"),
      interest3: data.get("interest3"),
      gender: data.get("gender"),
    };

    console.log(profileData);

    try {

        const profileResponse = await updateProfile(profileData);
        console.log('Profile updated:', profileResponse);
        const data = await getProfile(username);
        setProfileData(data["result"]);
        if (data["result"].profile_picture) {
            setPreviewUrl(data["result"].profile_picture); // Set the initial profile picture as default
        }
        setConfirmationMessage('Profile has been updated successfully.');
    } catch (error) {
        console.error('Failed to create profile:', error);
        setErrorMessage('Failed to update profile. Please try again.');
        // Handle errors (e.g., show error message to user)
    }
  };

  const handlePostRating = async () => {
    const newRating = {
        "rater_name": loggedInUser,
        "rated_name": username,
        "rating": postRating
    };

    try {
        await rateProfile(newRating);

        const ratings = await getAllRatings(username);
        setAllRatings(ratings["result"]);
        const userrating = await getUserRating(username);
        setUserRating(userrating["result"]);

        setConfirmationMessage('Profile has been rated successfully.');
      } catch (error) {
        console.error('Failed to rate profile:', error);
        setErrorMessage('Failed to rate profile. Please try again.');
      }
  }

  const tabData = [
    { id: "profile", label: "Profile" },
    { id: "editProfile", label: "Edit Profile", disabled: isOtherUser },
    { id: "ratings", label: "Ratings" },
    { id: "rateProfile", label: "Rate Profile", disabled: isMyProfile }
  ]

  function GenderSelect() {
    const [selectedGender, setSelectedGender] = useState(profileData.gender);

    const handleChange = (event) => {
      const selectedValue = event.target.value;
      setSelectedGender(selectedValue); // Update the state with the new selected value
      console.log("Selected Gender:", selectedValue);
    };

    return (
      <TextField
        select
        fullWidth
        name="gender"
        label="Gender"
        id="gender"
        value={selectedGender}
        onChange={handleChange}
        sx={{ marginBottom: 2 }}
        className="custom-textfield"
      >
        <MenuItem value="N/A" sx={{ '&:hover': { backgroundColor: "#B3BFB8" } }}>N/A</MenuItem>
        <MenuItem value="male" sx={{ '&:hover': { backgroundColor: "#B3BFB8" } }}>Male</MenuItem>
        <MenuItem value="female" sx={{ '&:hover': { backgroundColor: "#B3BFB8" } }}>Female</MenuItem>
        <MenuItem value="non-binary" sx={{ '&:hover': { backgroundColor: "#B3BFB8" } }}>Non-binary</MenuItem>
      </TextField>
    );
  }

  function InterestsFields() {
    return (
      <React.Fragment>
        <TextField
          fullWidth
          name="interest1"
          label="Interest 1"
          id="interest1"
          autoComplete="off"
          defaultValue={profileData.interest1}
          sx={{ marginBottom: 2 }}
          className="custom-textfield"
        />
        <TextField
          fullWidth
          name="interest2"
          label="Interest 2"
          id="interest2"
          autoComplete="off"
          defaultValue={profileData.interest2}
          sx={{ marginBottom: 2 }}
          className="custom-textfield"
        />
        <TextField
          fullWidth
          name="interest3"
          label="Interest 3"
          id="interest3"
          autoComplete="off"
          defaultValue={profileData.interest3}
          sx={{ marginBottom: 2 }}
          className="custom-textfield"
        />
      </React.Fragment>
    );
  }

  function ProfilePictureUpload({ setPreviewUrl }) {
    // const [previewUrl, setLocalPreviewUrl] = useState(null); // State to store previewUrl locally

    const handleFileUpload = (event) => {
      const file = event.target.files[0];
      if (!file) {
        return; // Exit if no file is selected
      }

      // Your file validation logic here...

      const reader = new FileReader();
      reader.onload = () => {
        const previewUrl = reader.result;
        setPreviewUrl(previewUrl); // Pass previewUrl to the parent component
        // setLocalPreviewUrl(previewUrl); // Set previewUrl locally
      };
      reader.readAsDataURL(file);
    };

    return (
      <Box>
        <input
          accept="image/*"
          id="picture"
          type="file"
          onChange={handleFileUpload}
          style={{ display: "none" }}
        />
        <label htmlFor="picture">
          <Button variant="contained" component="span">
            Upload Profile Picture
          </Button>
        </label>
        {realPreviewUrl && (
          <img
            src={realPreviewUrl}
            alt="Profile"
            style={{ maxWidth: "100%", marginTop: "1rem" }}
          />
        )}
      </Box>
    );
  }

  return (
    <div>
      <HeaderRAF />
      <Grid
        container
        spacing={3}
        justifyContent="center"
        sx={{ backgroundColor: "#B3BFB8", minHeight: "100vh" }}
      >
        <Grid item xs={12} sm={8} md={6}>
          <Tabs
            value={tabValue}
            onChange={(event, newValue) => setTabValue(newValue)}
            centered
            sx={{ paddingRight: "10px" }}
          >
            {tabData.map(tab => (
              !tab.disabled && (
              <Tab
                key={tab.id}
                label={tab.label}
                value={tab.id}
                sx={{textDecoration: tab.disabled ? "line-through" : "none"}}
              />)
            ))}
          </Tabs>
          <TabPanel value={tabValue} index="profile">
            <Paper
              elevation={3}
              style={{ padding: "20px", textAlign: "center" }}
            >
              <Avatar
                alt="Profile Picture"
                src={profileData.profile_picture}
                sx={{ width: 150, height: 150, margin: "auto" }}
              />
              <Typography variant="h6" gutterBottom>
                {userData.username}
              </Typography>
              <Typography variant="body1">
                {userData.first_name} {userData.last_name}
              </Typography>
              <Divider style={{ margin: "20px 0" }} />
              <Typography variant="h6" gutterBottom>
                Who am I?
              </Typography>
              <Box
                sx={{
                  display: "flex",
                  justifyContent: "center",
                  flexWrap: "wrap",
                  gap: "8px",
                }}
              >
                {profileData.profile_description && (
                  <Typography variant="body1">
                    {profileData.profile_description}
                  </Typography>
                )}
              </Box>
              <Divider style={{ margin: "20px 0" }} />
              <Typography variant="h6" gutterBottom>
                Interests
              </Typography>
              <Box
                sx={{
                  display: "flex",
                  justifyContent: "center",
                  flexWrap: "wrap",
                  gap: "8px",
                }}
              >
                {profileData.interest1 && (
                  <Chip label={profileData.interest1} />
                )}
                {profileData.interest2 && (
                  <Chip label={profileData.interest2} />
                )}
                {profileData.interest3 && (
                  <Chip label={profileData.interest3} />
                )}
              </Box>
              <Divider style={{ margin: "20px 0" }} />
              {profileData.gender && (
                <Typography variant="body1" gutterBottom>
                  <strong>Gender:</strong> {profileData.gender}
                </Typography>
              )}
            </Paper>
          </TabPanel>
          <TabPanel value={tabValue} index="editProfile">
            <Box
              display="flex"
              flexDirection="column"
              alignItems="center"
              height="100%"
              sx={{ backgroundColor: "#B3BFB8", minHeight: "100vh" }}
              component="form"
              noValidate
              onSubmit={handleSubmit}
            >
              <TextField
                fullWidth
                name="description"
                label="Profile Description"
                id="description"
                autoComplete="off"
                defaultValue={profileData.profile_description}
                sx={{ marginBottom: 2 }}
                className="custom-textfield"
              />
              <Divider style={{ margin: "20px 0" }} />
              <ProfilePictureUpload setPreviewUrl={setPreviewUrl} />
              <Divider style={{ margin: "20px 0" }} />
              <InterestsFields />
              <Divider style={{ margin: "20px 0" }} />
              <GenderSelect />
              <Button
                type="submit"
                fullWidth
                variant="contained"
                sx={{ mt: 3, mb: 2 }}
              >
                Update Profile
              </Button>
              {confirmationMessage && (
                  <Alert severity="success" sx={{ mt: 2 }}>
                    {confirmationMessage}
                  </Alert>
                )}
                {errorMessage && (
                  <Alert severity="error" sx={{ mt: 2 }}>
                    {errorMessage}
                  </Alert>
                )}
            </Box>
          </TabPanel>
          <TabPanel value={tabValue} index="ratings">
            <Box textAlign="center">
                {userRating && (
                    <Typography variant="h4" gutterBottom> 
                        User Rating: {userRating.rating.toFixed(1)}<FaStar style={{ color: 'gold' }} />/5 out of {userRating.total_ratings} total ratings
                    </Typography>
                )}
            </Box>
            <Grid container spacing={2} justifyContent="center">
                <Box textAlign="center">
                    {!allRatings && <Typography variant="h4" gutterBottom>No ratings found for {username}.</Typography>}
                </Box>
                {allRatings && allRatings.map((rating, index) => (
                <Grid item key={index} xs={12} sm={6} md={4}>
                    <RatingCard rating={rating} />
                </Grid>
                ))}
            </Grid>
          </TabPanel>
          <TabPanel value={tabValue} index="rateProfile">
            <Box display="flex" flexDirection="column" alignItems="center" height="100vh" sx={{ backgroundColor: '#B3BFB8' }}>
                <TextField
                    select
                    name="rating"
                    label="Rating"
                    id="rating"
                    value={postRating}
                    onChange={(e) => setPostRating(e.target.value)}
                    sx={{ marginBottom: 2 }}
                    className="custom-textfield"
                >
                    <MenuItem value="1" sx={{ '&:hover': { backgroundColor: "#B3BFB8" } }}>1</MenuItem>
                    <MenuItem value="2" sx={{ '&:hover': { backgroundColor: "#B3BFB8" } }}>2</MenuItem>
                    <MenuItem value="3" sx={{ '&:hover': { backgroundColor: "#B3BFB8" } }}>3</MenuItem>
                    <MenuItem value="4" sx={{ '&:hover': { backgroundColor: "#B3BFB8" } }}>4</MenuItem>
                    <MenuItem value="5" sx={{ '&:hover': { backgroundColor: "#B3BFB8" } }}>5</MenuItem>
                </TextField>
                <Box marginTop={3} display="flex" flexDirection="column" alignItems="center" height="100vh">
                    <Button variant="contained" color="primary" onClick={handlePostRating}>
                        Add Rating
                    </Button>
                    {confirmationMessage && (
                    <Alert severity="success" sx={{ mt: 2 }}>
                        {confirmationMessage}
                    </Alert>
                    )}
                    {errorMessage && (
                    <Alert severity="error" sx={{ mt: 2 }}>
                        {errorMessage}
                    </Alert>
                    )}
                </Box>
            </Box>
          </TabPanel>
        </Grid>
      </Grid>
    </div>
  );
};

export default UserProfile;
