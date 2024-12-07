import React, { useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { fetchTokens, saveSession } from '../utils/auth';

const Login = ({ onLogin }) => {
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    const handleCallback = async () => {
      const params = new URLSearchParams(location.search);
      const code = params.get('code');

      if (code) {
        try {
          console.log('Authorization code:', code);

          // Fetch tokens using the authorization code
          const session = await fetchTokens(code);
          console.log('Session:', session);

          // Save session and update app state
          saveSession(session);
          onLogin(session);

          // Redirect to home page
          navigate('/');
        } catch (error) {
          console.error('Login failed:', error);
        }
      }
    };

    handleCallback();
  }, [location, onLogin, navigate]);

  const handleLogin = () => {
    const clientId = process.env.REACT_APP_COGNITO_CLIENT_ID;
    const redirectUri = process.env.REACT_APP_REDIRECT_URI;
    const hostedUI = process.env.REACT_APP_COGNITO_DOMAIN;

    console.log('Environment Variables:');
    console.log('Cognito Client ID:', clientId);
    console.log('Redirect URI:', redirectUri);
    console.log('Hosted UI Domain:', hostedUI);

    const loginUrl = `${hostedUI}/login?response_type=code&client_id=${clientId}&redirect_uri=${redirectUri}&scope=email+openid+profile&identity_provider=Google`;
    window.location.href = loginUrl;
  };

  return (
    <div style={{ padding: '1rem' }}>
      <h1>Login</h1>
      <button onClick={handleLogin}>Login with Google</button>
    </div>
  );
};

export default Login;
