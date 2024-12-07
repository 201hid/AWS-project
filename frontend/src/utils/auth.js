export const saveSession = (session) => {
    localStorage.setItem('session', JSON.stringify(session));
  };
  
  export const getSession = () => {
    const session = localStorage.getItem('session');
    return session ? JSON.parse(session) : null;
  };
  
  export const clearSession = () => {
    localStorage.removeItem('session');
  };
  
  export const fetchTokens = async (code) => {
    const clientId = process.env.REACT_APP_COGNITO_CLIENT_ID;
    const clientSecret = process.env.REACT_APP_COGNITO_CLIENT_SECRET;
    const redirectUri = process.env.REACT_APP_REDIRECT_URI;
    const tokenUrl = `${process.env.REACT_APP_COGNITO_DOMAIN}/oauth2/token`;
  
    const body = new URLSearchParams({
      grant_type: 'authorization_code',
      client_id: clientId,
      client_secret: clientSecret,
      redirect_uri: redirectUri,
      code,
    });
  
    const response = await fetch(tokenUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: body.toString(),
    });
  
    if (!response.ok) {
      throw new Error('Failed to fetch tokens');
    }
  
    const data = await response.json();
    const userDetails = parseJwt(data.id_token);
  
    return {
      token: data.access_token,
      username: userDetails['cognito:username'] || 'Not available',
      email: userDetails.email || 'Not available',
    };
  };
  
  export const parseJwt = (token) => {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );
    return JSON.parse(jsonPayload);
  };
  