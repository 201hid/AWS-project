import React from 'react';
import { clearSession } from '../utils/auth';

const Navbar = ({ user, setUser }) => {
  // Handle login
  const handleLogin = () => {
    const clientId = process.env.REACT_APP_COGNITO_CLIENT_ID;
    const redirectUri = process.env.REACT_APP_REDIRECT_URI;
    const hostedUI = process.env.REACT_APP_COGNITO_DOMAIN;

    if (!clientId || !redirectUri || !hostedUI) {
      console.error('Missing environment variables for login.');
      return;
    }

    const loginUrl = `${hostedUI}/login?response_type=code&client_id=${clientId}&redirect_uri=${redirectUri}&scope=email+openid+profile&identity_provider=Google`;
    window.location.href = loginUrl;
  };

  // Handle logout
  const handleLogout = () => {
    console.log("Clearing session...");
    clearSession(); // Clear session from local storage
    setUser(null); // Update user state to null

    const clientId = process.env.REACT_APP_COGNITO_CLIENT_ID;
    const hostedUI = process.env.REACT_APP_COGNITO_DOMAIN;
    const logoutUri = encodeURIComponent(process.env.REACT_APP_LOGOUT_URI); // Use the logout URI from .env

    if (!clientId || !hostedUI || !logoutUri) {
      console.error('Missing environment variables for logout.');
      return;
    }

    const logoutUrl = `${hostedUI}/logout?client_id=${clientId}&logout_uri=${logoutUri}`;
    
    // Log the constructed logout URL for debugging
    console.log("Logout URL:", logoutUrl);

    // Redirect the user to the logout URL
    window.location.href = logoutUrl;
  };

  return (
    <nav style={{ padding: '1rem', borderBottom: '1px solid #ddd' }}>
      <span>
        {user ? `Hi, ${user.username || user.email}` : 'Hi, Anonymous User'}
      </span>
      <button
        onClick={user ? handleLogout : handleLogin}
        style={{ marginLeft: '1rem' }}
      >
        {user ? 'Logout' : 'Login'}
      </button>
    </nav>
  );
};

export default Navbar;
