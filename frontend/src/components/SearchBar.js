import React, { useState, useRef } from 'react';
import { TextField, Button } from '@mui/material';
import { getListing, getUserWithUserId } from '../client';
import { Autocomplete, GoogleMap, useJsApiLoader, Marker } from '@react-google-maps/api';
import Box from '@mui/material/Box';

function SearchBar(props) {
  const [title, setTitle] = useState(null);
  const [description, setDescription] = useState(null);
  const [searchUsername, setSearchUsername] = useState(null);
  const [distance, setDistance] = useState(null);
  const [location, setLocation] = useState(null);
  const [rating, setRating] = useState(null);
  const locationRef = useRef();
  const center = { lat: 37.0902, lng: -95.7129 };

  const { isLoaded } = useJsApiLoader({
    googleMapsApiKey: process.env.REACT_APP_GOOGLE_MAPS_API_KEY,
    libraries: ['places'],
  });

  const handleSearch = async () => {
    try {
      let locationValue = locationRef.current.value;
      if (locationValue === '')
        locationValue = null;

      const searchCriteria = {
        "listing_id": null,
        "username": searchUsername,
        "title": title,
        "description": description,
        "location": locationValue,
        "distance": distance,
        "rating": rating
      };
      console.log(searchCriteria);

      const searchResults = await getListing(searchCriteria);
      const updatedResults = await Promise.all(searchResults.result.map(async (listing) => {
        const userData = await getUserWithUserId(listing.user_id);
        return { ...listing, username: userData.result.username };
      }));
      console.log(updatedResults);
      props.onSearchResults(updatedResults);

      if (locationValue) {
        const response = await fetch(`https://maps.googleapis.com/maps/api/geocode/json?address=${encodeURIComponent(locationValue)}&key=${process.env.REACT_APP_GOOGLE_MAPS_API_KEY}`);
        const data = await response.json();
        if (data.results.length > 0) {
          const { lat, lng } = data.results[0].geometry.location;
          setLocation({ lat, lng });
        } 
      }
      else if (!locationValue) {
        setLocation(null)
      }
    }
    catch (error) {
      console.error('Failed to fetch listings:', error);
    }
  };

  const handleUsernameChange = (e) => {
    setSearchUsername(e.target.value || null); // Set to null if empty
  };
  
  const handleTitleChange = (e) => {
    setTitle(e.target.value || null); // Set to null if empty
  };
  
  const handleDescriptionChange = (e) => {
    setDescription(e.target.value || null); // Set to null if empty
  };
  
  const handleDistanceChange = (e) => {
    // Ensure only digits are entered
    const regex = /^[0-9]*$/;
    if (regex.test(e.target.value) || e.target.value === '') {
      setDistance(e.target.value || null); // Set to null if empty
    }
  };

  const handleRatingChange = (e) => {
    // Ensure only digits are entered
    const regex = /^[0-9]*$/;
    if (regex.test(e.target.value) || e.target.value === '') {
      setRating(e.target.value || null); // Set to null if empty
    }
  };
  

  return (
    <div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', alignItems: 'center' }}>
        {/* move the tooltips on the search bar to be bigger and above the text box */}
        <TextField label="Username" value={searchUsername} onChange={handleUsernameChange} className="custom-textfield"/>
        <TextField label="Title" value={title} onChange={handleTitleChange} className="custom-textfield"/>
        <TextField label="Description" value={description} onChange={handleDescriptionChange} className="custom-textfield"/>
        <TextField label="Minimum Rating" value={rating} onChange={handleRatingChange} className="custom-textfield"/>
        {isLoaded && (
          <Autocomplete
            onLoad={(autoComplete) => {
              autoComplete.setFields(['formatted_address']);
            }}
          >
            <TextField 
              label="Location"
              placeholder="Enter location"
              inputRef={locationRef}
              className="custom-textfield"
              style={{ width: '100%' }}
            />
          </Autocomplete>
        )}
        <TextField label="Distance from location (miles)" value={distance} onChange={handleDistanceChange} className="custom-textfield"/>
      </div>
      <div style={{ display: 'flex', justifyContent: 'center', marginTop: '20px' }}>
        <Button onClick={handleSearch} variant="outlined">Search</Button>
      </div>
      <Box mb={4} mt={3}>
        <div style={{ height: '400px', width: '100%' }}>
          {isLoaded && (
            <GoogleMap
              center={location || center}
              zoom={location ? 15 : 4}
              mapContainerStyle={{ height: '100%', width: '100%' }}
              options={{
                streetViewControl: false,
                mapTypeControl: false,
                fullscreenControl: false,
              }}
            >
              {location && <Marker position={location} />}
            </GoogleMap>
          )}
        </div>
      </Box>
    </div>
  );
}

export default SearchBar;
