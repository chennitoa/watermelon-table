import React from 'react';
import { FaStar } from 'react-icons/fa';
import { Card, CardActions, CardContent, Typography, Divider, Modal, Button } from '@mui/material';

export default function RatingCard({ rating }) {
  const currentDate = new Date(rating.rated_date);
  const pacificTimeZoneOffset = -7 * 60 * 60 * 1000; // PST is 8 hours behind UTC
  const dateInPST = new Date(currentDate.getTime() + pacificTimeZoneOffset);

  // Format the date using toLocaleString() with options
  const formattedDate = dateInPST.toLocaleString('en-US', {
    timeZone: 'America/Los_Angeles', // Set the time zone to PST
    month: 'numeric',
    day: 'numeric',
    year: 'numeric',
    hour: 'numeric',
    minute: 'numeric',
  });

  const [open, setOpen] = React.useState(false);

  const handleOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  return (
    <>
      <Card sx={{ maxWidth: 300, maxHeight: 300, margin: 'auto', padding: "10px", cursor: "pointer" }} onClick={handleOpen}>
        <CardContent>
          <Typography gutterBottom variant="h5" component="div" sx={{ fontSize: '1.5rem', overflow: 'hidden', textOverflow: 'ellipsis', display: '-webkit-box', WebkitLineClamp: 1, WebkitBoxOrient: 'vertical' }}>
            {rating.rating}
            <FaStar style={{ color: 'gold' }} />
          </Typography>
          <Divider />
          <Typography variant="body2" color="text.secondary" sx={{ fontSize: '1.2rem', overflow: 'hidden', textOverflow: 'ellipsis', display: '-webkit-box', WebkitLineClamp: 1, WebkitBoxOrient: 'vertical' }}>
            Posted by: {rating.rater_name}
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ fontSize: '1.2rem', overflow: 'hidden', textOverflow: 'ellipsis', display: '-webkit-box', WebkitLineClamp: 1, WebkitBoxOrient: 'vertical' }}>
            Date Posted: {formattedDate}
          </Typography>
        </CardContent>
      </Card>
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
        // style={{ display: 'flex', justifyContent: 'center', alignItems: 'center'}}
      >
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
          <Card sx={{ minWidth: 400, maxWidth: 1250, margin: 'auto', padding: "10px" }}>
            <CardContent>
            <Typography gutterBottom variant="h5" component="div" sx={{ fontSize: '1.5rem', overflow: 'hidden', textOverflow: 'ellipsis', display: '-webkit-box', WebkitLineClamp: 1, WebkitBoxOrient: 'vertical' }}>
              {rating.rating}
              <FaStar style={{ color: 'gold' }} />
            </Typography>
            <Divider />
            <Typography variant="body2" color="text.secondary" sx={{ fontSize: '1.2rem', overflow: 'hidden', textOverflow: 'ellipsis', display: '-webkit-box', WebkitLineClamp: 1, WebkitBoxOrient: 'vertical' }}>
              Posted by: {rating.rater_name}
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ fontSize: '1.2rem', overflow: 'hidden', textOverflow: 'ellipsis', display: '-webkit-box', WebkitLineClamp: 1, WebkitBoxOrient: 'vertical' }}>
              Date Posted: {formattedDate}
            </Typography>
          </CardContent>
          <CardActions sx={{justifyContent: "center"}}>
            <Button size="large" onClick={handleClose}>Close</Button>
          </CardActions>
          </Card>
        </div>
      </Modal>
    </>
  );
};
