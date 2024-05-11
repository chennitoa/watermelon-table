import * as React from 'react';
import Button from '@mui/material/Button';
import Modal from '@mui/material/Modal';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import CardActions from '@mui/material/CardActions';
import { Link } from 'react-router-dom';
import { getCurrentUser } from '../client';
import Tooltip from '@mui/material/Tooltip';

export default function ListingCard({ listing }) {
  const [loggedIn, setLoggedIn] = React.useState(false);

  const currentDate = new Date(listing.date);
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

  React.useEffect(() => {
    const fetchData = async () => {
      try {
        const user = await getCurrentUser();
        setLoggedIn(!user["detail"]);
      } catch (error) {
        console.error("Failed to fetch user data:", error);
        // Optionally handle the error, e.g., show an error message
      }
    };

    fetchData();
  }, []);

  const [open, setOpen] = React.useState(false);

  const handleOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  return (
    <>
      <Card sx={{ minWidth: 300, maxHeight: 300, margin: 'auto', padding: "10px", cursor: "pointer" }} onClick={handleOpen}>
        <CardContent>
          <Typography gutterBottom variant="h5" component="div" sx={{ fontSize: '1.5rem', overflow: 'hidden', textOverflow: 'ellipsis', display: '-webkit-box', WebkitLineClamp: 1, WebkitBoxOrient: 'vertical'  }}>
            {listing.title}
          </Typography>
          <Divider />
          <Typography variant="body2" color="text.secondary" sx={{ fontSize: '1.2rem', overflow: 'hidden', textOverflow: 'ellipsis', display: '-webkit-box', WebkitLineClamp: 1, WebkitBoxOrient: 'vertical' }}>
            {listing.listing_description}
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ fontSize: '1.2rem', overflow: 'hidden', textOverflow: 'ellipsis', display: '-webkit-box', WebkitLineClamp: 1, WebkitBoxOrient: 'vertical' }}>
            Posted by: {listing.username}
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ fontSize: '1.2rem', overflow: 'hidden', textOverflow: 'ellipsis', display: '-webkit-box', WebkitLineClamp: 1, WebkitBoxOrient: 'vertical' }}>
            Address: {listing.street_address}
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ fontSize: '1.2rem', overflow: 'hidden', textOverflow: 'ellipsis', display: '-webkit-box', WebkitLineClamp: 1, WebkitBoxOrient: 'vertical' }}>
            Date Posted: {formattedDate}
          </Typography>
        </CardContent>
        <CardActions>
          <Button size="large">Message</Button>
        </CardActions>
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
              <Typography gutterBottom variant="h4" component="div" sx={{ fontSize: '2rem' }}>
                {listing.title}
              </Typography>
              <Divider />
              <Typography variant="body1" color="text.secondary" sx={{ fontSize: '1.5rem' }}>
                {listing.listing_description}
              </Typography>
              <Typography variant="body1" color="blue" sx={{ fontSize: '1.5rem' }}>
                Posted by: <Link to={`/profile/${listing.username}`} style={{ textDecoration: 'none', color: 'inherit' }}>{listing.username}</Link>
              </Typography>
              <Typography variant="body1" color="text.secondary" sx={{ fontSize: '1.5rem' }}>
                Address: {listing.street_address}
              </Typography>
              <Typography variant="body1" color="text.secondary" sx={{ fontSize: '1.5rem' }}>
                Date Posted: {formattedDate}
              </Typography>
            </CardContent>
            <CardActions sx={{justifyContent: "center"}}>
              {
                loggedIn ? (
                  <Button size="large" onClick={handleClose} disabled={!loggedIn}>Accept</Button>
                ) : (
                  <Tooltip title="Sign up or login to accept the listing">
                    <span>
                      <Button size="large" onClick={handleClose} disabled={!loggedIn}>Accept</Button>
                    </span>
                  </Tooltip>
                )
              }
              <Button size="large" onClick={handleClose}>Close</Button>
            </CardActions>
          </Card>
        </div>
      </Modal>
    </>
  );
}
