import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import User from './components/User';
import { getSession, saveSession, fetchTokens } from './utils/auth';

const App = () => {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    // Check if session exists in local storage
    const session = getSession();
    if (session) {
      setUser(session);
    } else {
      // Check if redirected with a code (OAuth2 callback)
      const params = new URLSearchParams(window.location.search);
      const code = params.get('code');

      if (code) {
        // Fetch tokens using the code and update the user state
        fetchTokens(code)
          .then((sessionData) => {
            saveSession(sessionData); // Save session in localStorage
            setUser(sessionData); // Update user state
            navigate('/'); // Navigate to the main page after login
          })
          .catch((error) => {
            console.error('Token fetch failed:', error);
          });
      }
    }
  }, [navigate]);

  return (
    <>
      <Navbar user={user} setUser={setUser} />
      <div style={{ padding: '1rem' }}>
        <h1>Main Page</h1>
        {user ? (
          <User user={user} />
        ) : (
          <div>
            <h2>User details not available.</h2>
          </div>
        )}
      </div>
    </>
  );
};

export default App;
