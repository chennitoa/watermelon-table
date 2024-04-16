import React, { useState, useEffect } from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import HeaderRAF from './HeaderRAF';
import SearchBar from './SearchBar';
import { getCurrentProfile, createListing, getAllListings } from '../client';

export default function ListingsPage() {
  const [showForm, setShowForm] = useState(false);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [listings, setListings] = useState([]);
  const [currentUserId, setUserId] = useState(0);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const profile = await getCurrentProfile(); 
        // console.log(profile.Profile);
        setUserId(profile.Profile.user_id);
        console.log(currentUserId);
      } catch (error) {
        console.error('Failed to fetch profile:', error);
      }
    };

    fetchProfile();
  }, []);

  useEffect(() => {
    const fetchListings = async () => {
      try {
        const allListings = await getAllListings();
        setListings(allListings);
      } catch (error) {
        console.error('Failed to fetch listings:', error);
      }
    };

    fetchListings();
  }, []); // Empty dependency array to run only once on component mount

  const handleCreateListing = async () => {
    // login, get current profile, get the user id from the profile
    // include it in the listing when posting it
    if (title.trim() !== '' && description.trim() !== '') {
      const newListing = {
        user_id: currentUserId,
        title, 
        description,
        date: new Date().toISOString() // Adding timestamp
      };
      try {
        await createListing(newListing);
        setListings([...listings, newListing]); // Assuming the response contains the new listing
        setTitle('');
        setDescription('');
        setShowForm(false);
      } catch (error) {
        console.error('Failed to create listing:', error);
        alert('Failed to create listing. Please try again.');
      }
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
            <div>Posted by: {listing.username}</div> {/* Displaying the username */}
            <div>Title: {listing.title}</div>
            <div>Description: {listing.description}</div>
            <div>Date: {listing.date}</div> {/* Displaying date */}
          </Box>
        ))}
      </Box>
    </div>
  );
}
