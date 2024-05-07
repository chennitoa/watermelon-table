import React, { useRef, useState } from 'react';
import { useJsApiLoader, GoogleMap, Marker, Autocomplete } from '@react-google-maps/api';
import { TextField, Button } from '@mui/material';

function SearchMap({ location }) {
  const { isLoaded } = useJsApiLoader({
    googleMapsApiKey: process.env.REACT_APP_GOOGLE_MAPS_API_KEY,
    libraries: ['places'],
  });

  // eslint-disable-next-line
  const [map, setMap] = useState(null);
  const [destination, setDestination] = useState(null);
  const destinationRef = useRef();

  if (!isLoaded) {
    return <div>Loading...</div>; // or any loading indicator
  }

  const handleSearch = async () => {
    const destinationValue = destinationRef.current.value;
    if (destinationValue) {
      try {
        const response = await fetch(`https://maps.googleapis.com/maps/api/geocode/json?address=${encodeURIComponent(destinationValue)}&key=${process.env.REACT_APP_GOOGLE_MAPS_API_KEY}`);
        const data = await response.json();
        if (data.results.length > 0) {
          const { lat, lng } = data.results[0].geometry.location;
          setDestination({ lat, lng });
        } else {
          console.error("No results found for the entered address.");
        }
      } catch (error) {
        console.error("Error occurred while fetching data:", error);
      }
    }
  };

  return (
    <div style={{ height: '50vh', width: '100%' }}>
      <GoogleMap
        center={location || { lat: 37.0902, lng: -95.7129 }} // Use provided location or default center
        zoom={destination ? 15 : 4}
        mapContainerStyle={{ height: '100%', width: '100%' }}
        options={{
          zoomControl: false,
          streetViewControl: false,
          mapTypeControl: false,
          fullscreenControl: false,
        }}
        onLoad={(map) => setMap(map)}
      >
        {destination && <Marker position={destination} />}
        {/* Autocomplete positioned inside the map */}
        <div style={{ position: 'absolute', top: 10, left: 10, zIndex: 999 }}>
          <Autocomplete
            onLoad={(autoComplete) => {
              autoComplete.setFields(['formatted_address', 'geometry']);
            }}
          >
            <TextField 
              label="Location"
              placeholder="Enter location"
              inputRef={destinationRef}
              sx={{ backgroundColor: 'rgba(255, 255, 255, 0.8)' }}
            />
          </Autocomplete>
          <Button onClick={handleSearch}>Search</Button>
        </div>
      </GoogleMap>
    </div>
  );
}

export default SearchMap;
