import React, { useState } from 'react';
import { FaStar } from 'react-icons/fa';

const RatingCard = () => {
  const [rating, setRating] = useState(0); // Initial rating is 0
  
  // Function to handle when a star is clicked
  const handleStarClick = (starIndex) => {
    setRating(starIndex + 1); // +1 because starIndex starts from 0
  };

  return (
    <div>
      {[...Array(5)].map((star, i) => {
        const starIndex = i;
        return (
          <FaStar
            key={i}
            onClick={() => handleStarClick(starIndex)}
            color={starIndex < rating ? '#ffc107' : '#e4e5e9'}
            size={30}
            style={{ cursor: 'pointer' }}
          />
        );
      })}
      <p>Current Rating: {rating} out of 5</p>
    </div>
  );
};

export default RatingCard;