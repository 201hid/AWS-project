import React, { useState, useEffect } from "react";

const Login = ({ setUsername }) => {
  const [error, setError] = useState(null);

  const handleLogin = async () => {
    try {
      // Fetch the Google OAuth redirect URL from the backend
      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/auth/google`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error("Failed to get the Google OAuth URL.");
      }

      const data = await response.json();
      if (data.redirect_url) {
        // Redirect user to the Google OAuth URL
        window.location.href = data.redirect_url;
      } else {
        throw new Error("Invalid redirect URL received.");
      }
    } catch (err) {
      console.error("Error during login:", err);
      setError("Failed to initiate login. Please try again.");
    }
  };

  const handleCallback = async () => {
    // Parse the URL for the code parameter
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get("code");

    if (!code) {
      setError("Missing authorization code in the callback URL.");
      return;
    }

    try {
      // Send the authorization code to the backend
      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/auth/google/callback`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ code }),
      });

      if (!response.ok) {
        throw new Error("Failed to complete the login process.");
      }

      const data = await response.json();

      // Store the JWT token in localStorage
      if (data.token) {
        localStorage.setItem("jwtToken", data.token);
        setUsername(data.user.name);
      } else {
        throw new Error("Authentication token not received.");
      }
    } catch (err) {
      console.error("Error during callback handling:", err);
      setError("Login failed. Please try again.");
    }
  };

  // Automatically handle the callback if the "code" parameter exists in the URL
  useEffect(() => {
    if (window.location.search.includes("code")) {
      handleCallback();
    }
  }, []);

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h2>Welcome to the Authentication App</h2>
      <button onClick={handleLogin} style={{ padding: "10px 20px", fontSize: "16px" }}>
        Login with Google
      </button>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
};

export default Login;
