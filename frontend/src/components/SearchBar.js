import React, { useState } from 'react';
import { TextField, Button } from '@mui/material';

function SearchBar(
    props
) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');

  const handleSearch = () => {
    fetch(`http://localhost:8000/search/listings/?title=${title}&description=${description}`)
      .then(response => response.json())
      .then(data => {
        // Assuming a prop named onSearchResults is passed to SearchBar
        props.onSearchResults(data);
      })
      .catch(error => console.error('Error fetching search results:', error));
  };

  return (
    <div>
      <TextField label="Title" value={title} onChange={(e) => setTitle(e.target.value)} />
      <TextField label="Description" value={description} onChange={(e) => setDescription(e.target.value)} />
      <Button onClick={handleSearch}>Search</Button>
    </div>
  );
}

export default SearchBar;