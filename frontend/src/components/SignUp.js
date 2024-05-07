import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Avatar from "@mui/material/Avatar";
import Button from "@mui/material/Button";
import CssBaseline from "@mui/material/CssBaseline";
import TextField from "@mui/material/TextField";
import Link from "@mui/material/Link";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import LockOutlinedIcon from "@mui/icons-material/LockOutlined";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import { createUser, updateProfile, login } from "../client";
import Alert from "@mui/material/Alert";

function GenderSelect() {
  return (
    <TextField
      select
      fullWidth
      name="gender"
      label="Gender"
      id="gender"
      SelectProps={{
        native: true,
      }}
    >
      <option value="N/A">N/A</option>
      <option value="male">Male</option>
      <option value="female">Female</option>
      <option value="non-binary">Non-binary</option>
    </TextField>
  );
}

function InterestsFields() {
  return (
    <React.Fragment>
      <TextField
        fullWidth
        name="interest1"
        label="Interest 1"
        id="interest1"
        autoComplete="off"
      />
      <TextField
        fullWidth
        name="interest2"
        label="Interest 2"
        id="interest2"
        autoComplete="off"
      />
      <TextField
        fullWidth
        name="interest3"
        label="Interest 3"
        id="interest3"
        autoComplete="off"
      />
    </React.Fragment>
  );
}

function ProfilePictureUpload({ setPreviewUrl }) {
  const [previewUrl, setLocalPreviewUrl] = useState(null); // State to store previewUrl locally

  const handleFileUpload = (event) => {
    const file = event.target.files[0];

    // Your file validation logic here...

    const reader = new FileReader();
    reader.onload = () => {
      const previewUrl = reader.result;
      setPreviewUrl(previewUrl); // Pass previewUrl to the parent component
      setLocalPreviewUrl(previewUrl); // Set previewUrl locally
    };
    reader.readAsDataURL(file);
  };

  return (
    <Box>
      <input
        accept="image/*"
        id="picture"
        type="file"
        onChange={handleFileUpload}
        style={{ display: 'none' }}
      />
      <label htmlFor="picture">
        <Button variant="contained" component="span">
          Upload Profile Picture
        </Button>
      </label>
      {previewUrl && (
        <img
          src={previewUrl}
          alt="Profile"
          style={{ maxWidth: "100%", marginTop: "1rem" }}
        />
      )}
    </Box>
  );
}

function SignUp() {
  const [formValid, setFormValid] = useState(false);
  const [previewUrl, setPreviewUrl] = useState(""); // State to store previewUrl
  const [usernameError, setUsernameError] = useState(""); // State to store username error message
  const [emailError, setEmailError] = useState(""); // State to store email error message
  const [passwordError, setPasswordError] = useState(""); // State to store password error message
  const [showPassword, setShowPassword] = useState(false); // State to toggle show/hide password
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate(); // Get history object

  useEffect(() => {
    const errorTimeout = setTimeout(() => {
      setErrorMessage('');
    }, 5000);
  
    return () => {
      clearTimeout(errorTimeout);
    };
  }, [errorMessage]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);

    // Updated userData object to match the new API request format
    const userData = {
        username: data.get('username'),  
        email: data.get('email'),
        first_name: data.get('first_name'),
        last_name: data.get('last_name'),
        password: data.get('password'),
    };

    const profileData = {
        username: data.get('username'),
        description: data.get('description'),
        profile_picture: previewUrl,
        interest1: data.get('interest1'),
        interest2: data.get('interest2'),
        interest3: data.get('interest3'),
        gender: data.get('gender'),
    };

    try {
        // const doesUserExist = await getUserWithUsername(userData.username);
        // if (doesUserExist["result"]["email"] === userData.email) {
        //   setErrorMessage('Username or email has been taken. Please try again.');
        // }
        // else {
        //   setErrorMessage('');
        // }
          
        const userResponse = await createUser(userData);
        console.log('User created:', userResponse);

        const result = await login(data.get('username'), data.get('password'));
        console.log()
        localStorage.setItem('token', result.access_token);

        const profileResponse = await updateProfile(profileData);
        console.log('Profile updated:', profileResponse);

        navigate(`/profile/${userData.username}`);
    } catch (error) {
        console.error('Failed to create profile:', error);
        // Handle errors (e.g., show error message to user)
    }
  };
  

  const handleInputChange = (event) => {
    const formFields = event.currentTarget.querySelectorAll("[required]");
    let isValid = true;

    formFields.forEach((field) => {
      const value = field.value.trim();

      if (!value) {
        isValid = false;
      } else {
        switch (field.name) {
          case 'username':
            const usernameRegex = /^[a-zA-Z0-9_.]{6,}$/;
            if (!usernameRegex.test(value)) {
              isValid = false;
              setUsernameError("Username must be at least 6 characters long and can only contain letters, numbers, underscores, and periods.");
            }
            else {
              setUsernameError("");
            }
            break;
          case 'email':
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
              isValid = false;
              setEmailError("Invalid email format.");
            } else {
              setEmailError("");
            }
            break;
          case 'password':
            const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
            if (!passwordRegex.test(value)) {
              isValid = false;
              setPasswordError("Password must be at least 8 characters long and include at least one uppercase letter, one lowercase letter, one number, and one special character.");
            } else {
              setPasswordError("");
            }
            break;
          default:
            break;
        }
      }
    });

    setFormValid(isValid);
  };

  const handleTogglePasswordVisibility = () => {
    setShowPassword((prevShowPassword) => !prevShowPassword);
  };

  return (
    <ThemeProvider theme={createTheme()}>
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Box
          sx={{
            marginTop: 8,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <Avatar sx={{ m: 1, bgcolor: "secondary.main" }}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h1" variant="h5">
            Rent a Lackey - Sign up
          </Typography>
          <Box
            component="form"
            noValidate
            onSubmit={handleSubmit}
            sx={{ mt: 3 }}
            onChange={handleInputChange}
          >
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <TextField
                  autoComplete="given-name"
                  name="first_name"
                  required
                  fullWidth
                  id="first_name"
                  label="First Name"
                  autoFocus
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  required
                  fullWidth
                  id="last_name"
                  label="Last Name"
                  name="last_name"
                  autoComplete="family-name"
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  error={!!usernameError}
                  helperText={usernameError}
                  required
                  fullWidth
                  id="username"
                  label="Username"
                  name="username"
                  autoComplete="username"
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  error={!!emailError}
                  helperText={emailError}
                  required
                  fullWidth
                  id="email"
                  label="Email Address"
                  name="email"
                  autoComplete="email"
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  error={!!passwordError}
                  helperText={passwordError}
                  required
                  fullWidth
                  name="password"
                  label="Password"
                  type={showPassword ? 'text' : 'password'}
                  id="password"
                  autoComplete="new-password"
                />
                <Button
                  onClick={handleTogglePasswordVisibility}
                  variant="outlined"
                  size="small"
                  sx={{ mt: 1 }}
                >
                  {showPassword ? 'Hide' : 'Show'} Password
                </Button>
              </Grid>
              <Grid item xs={12}>
                <ProfilePictureUpload setPreviewUrl={setPreviewUrl} />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  name="description"
                  label="Profile Description"
                  id="description"
                  autoComplete="off"
                />
              </Grid>
              <Grid item xs={12}>
                <InterestsFields />
              </Grid>
              <Grid item xs={12}>
                <GenderSelect />
              </Grid>
            </Grid>
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
              disabled={!formValid}
            >
              Sign Up
            </Button>
            {errorMessage && (
              <Alert severity="error" sx={{ mt: 2 }}>
                {errorMessage}
              </Alert>
            )}
            <Grid container justifyContent="flex-end">
              <Grid item>
                <Link href="/sign-in" variant="body2">
                  Already have an account? Sign in
                </Link>
              </Grid>
            </Grid>
          </Box>
        </Box>
      </Container>
    </ThemeProvider>
  );
}

export default SignUp;