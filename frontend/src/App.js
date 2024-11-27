import React, { useState, useEffect } from "react";
import "./App.css";
import Navbar from "./components/Navbar";
import Home from "./components/Home";
import Login from "./components/Login";

function App() {
  const [username, setUsername] = useState(null);

  useEffect(() => {
    // Fetch user information if logged in
    const fetchUser = async () => {
      const token = localStorage.getItem("jwtToken");
      if (token) {
        try {
          const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/auth/me`, {
            headers: { Authorization: `Bearer ${token}` },
          });
          if (response.ok) {
            const data = await response.json();
            setUsername(data.name);
          } else {
            console.error("Failed to fetch user information:", response.statusText);
            localStorage.removeItem("jwtToken"); // Clear token if invalid
          }
        } catch (error) {
          console.error("Error fetching user:", error);
          localStorage.removeItem("jwtToken"); // Clear token on error
        }
      }
    };

    fetchUser();
  }, []);

  return (
    <div className="App">
      <Navbar username={username} />
      {username ? <Home /> : <Login setUsername={setUsername} />}
    </div>
  );
}

export default App;
