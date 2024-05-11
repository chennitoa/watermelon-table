import React from 'react';
import { Box, Container, Stack, Typography, Button } from '@mui/material';

export default function Hero() {
  return (
    <Box
      id="hero"
      sx={{
        width: '100%',
        backgroundImage: 'linear-gradient(180deg, #CEE5FD, #FFF)',
        backgroundSize: '100% 20%',
        backgroundRepeat: 'no-repeat',
      }}
    >
      <Container
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          pt: { xs: 14, sm: 20 },
          // pb: { xs: 8, sm: 12 },
        }}
      >
        <Stack spacing={2} sx={{ width: { xs: '100%', sm: '70%' } }}>
          <Typography
            component="h1"
            variant="h1"
            sx={{
              display: 'flex',
              flexDirection: { xs: 'column', md: 'row' },
              alignSelf: 'center',
              textAlign: 'center',
            }}
          >
            Rent a&nbsp;
            <Typography
              component="span"
              variant="h1"
              color="primary.main"
            >
              Lackey
            </Typography>
          </Typography>
          <Typography variant="body1" textAlign="center" color="text.secondary">
            Feeling lonely? Wanting to do something with a lackey but you don't have any?<br />
            Use Rent a Lackey to do fun tasks with others so you feel better about yourself.
          </Typography>
          <Stack direction="row" spacing={1} alignSelf="center" pt={2}>
            <Button 
              variant="contained" 
              color="primary"
              component="a"
              href="/listings"
            >
              Find listings
            </Button>
          </Stack>
        </Stack>
      </Container>
    </Box>
  );
}
