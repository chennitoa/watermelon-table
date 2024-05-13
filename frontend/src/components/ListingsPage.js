import React, { useState, useEffect, useRef } from 'react';
import Box from '@mui/material/Box';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Typography from '@mui/material/Typography';
import HeaderRAF from './HeaderRAF';
import SearchBar from './SearchBar';
import { getCurrentUser, createListing, getListing, getUserWithUserId } from '../client';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import ListingCard from './ListingCard';
import { Autocomplete } from '@react-google-maps/api';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Alert from '@mui/material/Alert';
import Tooltip from '@mui/material/Tooltip';

export default function ListingsPage() {
  const [tabValue, setTabValue] = useState(0);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [listings, setListings] = useState([]);
  const [currentUsername, setUsername] = useState('');
  const [currentUserId, setUserId] = useState(0);
  const [confirmationMessage, setConfirmationMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [loggedIn, setLoggedIn] = useState(false);
  const locationRef = useRef();

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const user = await getCurrentUser(); 
        console.log(user);
        if (user["detail"]) { // failed login
          setLoggedIn(false);
        }
        else {
          setLoggedIn(true);
          setUsername(user.username);
          setUserId(user.result.user_id);
        } 
        
      } catch (error) {
        console.error('Failed to fetch profile:', error);
      }
    };

    fetchProfile();
  }, []);

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

  useEffect(() => {
    const fetchListingsAndUsernames = async () => {
      try {
        const searchCriteria = {
          "listing_id": null,
          "username": null,
          "title": null,
          "description": null,
          "location": null,
          "distance": null,
          "rating": null,
        };
        const allListings = await getListing(searchCriteria);
        setListings(allListings.result);

        const updatedListings = await Promise.all(allListings.result.map(async (listing) => {
          const userData = await getUserWithUserId(listing.user_id);
          return { ...listing, username: userData.result.username };
        }));

        setListings(updatedListings);
      } catch (error) {
        console.error('Failed to fetch data:', error);
      }
    };

    fetchListingsAndUsernames();
  }, []);

  const handleCreateListing = async () => {
    let location = locationRef.current.value;
    if (location === '') {
      location = null;
    }
    if (title.trim() !== '' && description.trim() !== '') {
      const newListing = {
        username: currentUsername,
        title, 
        description,
        location
      };
      try {
        await createListing(newListing);
        const updatedListingsResponse = await getListing({
          "listing_id": null,
          "username": null,
          "title": null,
          "description": null,
          "location": null,
          "distance": null,
          "rating": null,
        });
        setListings(updatedListingsResponse.result);
        const updatedListings = await Promise.all(updatedListingsResponse.result.map(async (listing) => {
          const userData = await getUserWithUserId(listing.user_id);
          return { ...listing, username: userData.result.username };
        }));
        setListings(updatedListings);
        setTitle('');
        setDescription('');
        setConfirmationMessage('Listing has been created successfully.');
      } catch (error) {
        console.error('Failed to create listing:', error);
        setErrorMessage('Failed to create listing. Please try again.');
      }
    } else {
      setErrorMessage('Please provide both the title and description.');
    }
  };

  const handleSearchResults = (results) => {
    setListings(results);
  };

  return (
    <Box display="flex" flexDirection="column" height="100%" sx={{backgroundColor: '#B3BFB8', minHeight: '100vh'}}>
      <HeaderRAF />
      <Box display="flex" flexGrow={1} height="100%" sx={{backgroundColor: '#B3BFB8', height: '100%'}}>
        <Container>
          <Tabs value={tabValue} onChange={(event, newValue) => setTabValue(newValue)} centered sx={{ paddingRight: '35px' }}>
            <Tab label="Search & Listings" />
            {loggedIn ? (
              <Tab label="Create Listing" />
            ) : (
              <Tooltip title="Sign up or login to access create listing">
                <span>
                  <Tab label="Create Listing" disabled />
                </span>
              </Tooltip>
            )}
          </Tabs>
          <TabPanel value={tabValue} index={0}>
            <SearchBar onSearchResults={handleSearchResults}/>
            <Grid container spacing={3}>
              {listings && listings.map((listing, index) => (
                <Grid item xs={12} sm={6} md={4} key={index}>
                  <ListingCard listing={listing} currentUserId={currentUserId} />
                </Grid>
              ))}
            </Grid>
          </TabPanel>
          <TabPanel value={tabValue} index={1}>
            <Box display="flex" flexDirection="column" alignItems="center" height="100vh" sx={{ backgroundColor: '#B3BFB8' }}>
              <TextField
                label="Title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                sx={{ marginBottom: 2 }}
                className="custom-textfield"
              />
              <TextField
                label="Description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                multiline
                rows={4}
                sx={{ marginBottom: 2 }}
                className="custom-textfield"
              />
              <Autocomplete
                style={{ marginBottom: '16px' }} // Adjust margin bottom to match TextField
                onLoad={(autoComplete) => {
                  autoComplete.setFields(['formatted_address']);
                }}
              >
                <TextField 
                  label="Location"
                  placeholder="Enter location"
                  inputRef={locationRef}
                  className="custom-textfield"
                />
              </Autocomplete>
              <Box marginTop={3} display="flex" flexDirection="column" alignItems="center" height="100vh">
                <Button variant="contained" color="primary" onClick={handleCreateListing}>
                  Add Listing
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
        </Container>
      </Box>
    </Box>
  );
}

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
