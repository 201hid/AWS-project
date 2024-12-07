import React from "react";
import { clearSession } from "../utils/auth";

const Logout = ({ setUser }) => {
  const handleLogout = () => {
    console.log("Clearing session...");
    clearSession(); // Clear session from local storage
    setUser(null); // Update user state to null

    const clientId = process.env.REACT_APP_COGNITO_CLIENT_ID;
    const hostedUI = process.env.REACT_APP_COGNITO_DOMAIN;
    const logoutUri = encodeURIComponent(process.env.REACT_APP_REDIRECT_URI); // Encoded logout URI

    if (!clientId || !hostedUI || !logoutUri) {
      console.error("Missing environment variables for logout.");
      return;
    }

    const logoutUrl = `${hostedUI}/logout?client_id=${clientId}&logout_uri=${logoutUri}`;
    
    // Log the constructed logout URL for debugging
    console.log("Logout URL:", logoutUrl);

    // Redirect the user to the logout URL
    window.location.href = logoutUrl;
  };

  return (
    <button onClick={handleLogout}>
      Logout
    </button>
  );
};

export default Logout;
