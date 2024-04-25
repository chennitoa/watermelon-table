import React from "react";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
function HeaderRAF() {
  return (
    <Box p={2}>
      <Typography
        variant="h1"
        sx={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          textAlign: "center",
        }}
      >
        <Typography
          component="h1"
          variant="h1"
          sx={{
            display: "flex",
            flexDirection: { xs: "column", md: "row" },
            alignSelf: "center",
            textAlign: "center",
          }}
        >
          Rent a&nbsp;
          <Typography component="span" variant="h1" color="primary.main">
            Lackey
          </Typography>
        </Typography>
      </Typography>
    </Box>
  );
}

export default HeaderRAF;
