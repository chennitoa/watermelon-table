import React from 'react';
import './App.css';
import SignInSide from './components/SignInSide.js';
import HomePage from './components/HomePage.js';
import SignUp from './components/SignUp.js';
import getLPTheme from './components/getLPTheme';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import UserProfile from './components/UserProfile.js';
import ListingsPage from './components/ListingsPage.js';
import Chat from './components/chat/Chat.js';

function App() {
  const mode = React.useState('light');
  const LPtheme = createTheme(getLPTheme(mode));

  return (
    <div>
      <ThemeProvider theme={LPtheme}>
        <Router>
          <Routes>
            <Route path="/sign-in" element={<SignInSide />} />
            <Route path="/sign-up" element={<SignUp />} />
            <Route path="/listings" element={<ListingsPage />} />
            <Route path="/" element={<HomePage />} />
            <Route path="/profile/:username" element={<UserProfile />} />
            <Route path="/chat" element={<Chat/>} />
          </Routes>
        </Router>
      </ThemeProvider>
    </div>
  );
}

export default App;
