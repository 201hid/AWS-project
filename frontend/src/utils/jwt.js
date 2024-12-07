export const storeToken = (key, token) => {
    localStorage.setItem(key, token);
  };
  
  export const getToken = (key) => {
    return localStorage.getItem(key);
  };
  
  export const clearTokens = () => {
    localStorage.removeItem("id_token");
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
  };
  
  export const decodeToken = (token) => {
    const payload = token.split(".")[1];
    return JSON.parse(atob(payload));
  };
  
  export default { storeToken, getToken, clearTokens, decodeToken };
  