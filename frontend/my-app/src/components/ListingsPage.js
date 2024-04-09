import React, { useState } from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import HeaderRAF from './HeaderRAF';
import SearchBar from './SearchBar';

export default function ListingsPage() {
  const [showForm, setShowForm] = useState(false);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [listings, setListings] = useState([]);

  const handleCreateListing = () => {
    if (title.trim() !== '' && description.trim() !== '') {
      const newListing = { 
        title, 
        description,
        timestamp: new Date().toLocaleString() // Adding timestamp
      };
      setListings([...listings, newListing]);
      setTitle('');
      setDescription('');
      setShowForm(false);
    } else {
      alert('Please provide both the title and description.');
    }
  };

    // Add handleSearchResults function
  const handleSearchResults = (results) => {
    setListings(results);
  };

  return (
    <div>
      <HeaderRAF />
      <SearchBar onSearchResults={handleSearchResults}/>
      {!showForm && (
        <Button variant="contained" color="primary" onClick={() => setShowForm(true)}>
          Create Listing
        </Button>
      )}
      {showForm && (
        <Box mt={2}>
          <TextField
            label="Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            fullWidth
          />
          <TextField
            label="Description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            fullWidth
            multiline
            rows={4}
            mt={2}
          />
          <Box mt={2}>
            <Button variant="contained" color="primary" onClick={handleCreateListing}>
              Add Listing
            </Button>
            <Button variant="contained" color="secondary" onClick={() => setShowForm(false)}>
              Cancel
            </Button>
          </Box>
        </Box>
      )}
      <Box mt={2}>
        {listings.map((listing, index) => (
          <Box key={index} border={1} p={2} mt={1}>
            <div>Title: {listing.title}</div>
            <div>Description: {listing.description}</div>
            <div>Timestamp: {listing.timestamp}</div> {/* Displaying timestamp */}
          </Box>
        ))}
      </Box>
    </div>
  );
}
