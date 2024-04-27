import React, { useState, useEffect } from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import HeaderRAF from './HeaderRAF';
import SearchBar from './SearchBar';
import { getCurrentUser, createListing, getListing, getUserWithUserId } from '../client';

export default function ListingsPage() {
  const [showForm, setShowForm] = useState(false);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [listings, setListings] = useState([]);
  const [currentUsername, setUsername] = useState('');

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const user = await getCurrentUser(); 
        // console.log(profile.Profile);
        setUsername(user.result.username);
      } catch (error) {
        console.error('Failed to fetch profile:', error);
      }
    };

    fetchProfile();
  }, []);

  useEffect(() => {
    const fetchListingsAndUsernames = async () => {
      try {
        // Fetch listings
        const searchCriteria = {
          "listing_id": null,
          "username": null,
          "title": null,
          "description": null
        };
        const allListings = await getListing(searchCriteria);
        console.log("Listings:", allListings.results);
        setListings(allListings.results);
  
        // Fetch usernames for each listing
        const updatedListings = await Promise.all(allListings.results.map(async (listing) => {
          const userData = await getUserWithUserId(listing.user_id);
          return { ...listing, username: userData.result.username };
        }));
  
        console.log("Updated Listings:", updatedListings);
        setListings(updatedListings);
      } catch (error) {
        console.error('Failed to fetch data:', error);
      }
    };
  
    fetchListingsAndUsernames();
  }, []);
  
  

  const handleCreateListing = async () => {
    if (title.trim() !== '' && description.trim() !== '') {
      const newListing = {
        username: currentUsername,
        title, 
        description,
      };
      try {
        // Create the new listing
        await createListing(newListing);
        
        // Fetch the updated listings from the server
        const updatedListingsResponse = await getListing({
          "listing_id": null,
          "username": null,
          "title": null,
          "description": null
        });
        
        // Update the listings state with the updated listings fetched from the server
        setListings(updatedListingsResponse.results);

        // Fetch usernames for each listing
        const updatedListings = await Promise.all(updatedListingsResponse.results.map(async (listing) => {
          const userData = await getUserWithUserId(listing.user_id);
          return { ...listing, username: userData.result.username };
        }));
  
        console.log("Updated Listings:", updatedListings);
        setListings(updatedListings);
        
        // Reset form fields and hide the form
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
        {listings && listings.map((listing, index) => (
          <Box key={index} border={1} p={2} mt={1}>
            <div>Posted by: {listing.username}</div> {/* Displaying the username */}
            <div>Title: {listing.title}</div>
            <div>Description: {listing.listing_description}</div>
            <div>Date: {listing.date}</div> {/* Displaying date */}
          </Box>
        ))}
      </Box>
    </div>
  );
}