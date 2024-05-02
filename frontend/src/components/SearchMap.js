import React, { useRef, useState } from 'react';
import { useJsApiLoader, GoogleMap, Marker, Autocomplete } from '@react-google-maps/api';

const center = { lat: 48.8584, lng: 2.2945 };

function SearchMap() {
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
    <div style={{ height: '100vh', width: '100vw' }}>
      <GoogleMap
        center={destination || center}
        zoom={destination ? 15 : 10}
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
      </GoogleMap>
      <div style={{ position: 'absolute', top: 10, left: 10, zIndex: 999 }}>
        <Autocomplete
          onLoad={(autoComplete) => {
            autoComplete.setFields(['formatted_address', 'geometry']);
          }}
        >
          <input
            type="text"
            placeholder="Enter your destination"
            ref={destinationRef}
          />
        </Autocomplete>
        <button onClick={handleSearch}>Search</button>
      </div>
    </div>
  );
}

export default SearchMap;
