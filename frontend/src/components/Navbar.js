import React from "react";

const Navbar = ({ username }) => {
  const handleLogout = () => {
    localStorage.removeItem("jwtToken");
    window.location.reload();
  };

  return (
    <nav style={{ display: "flex", justifyContent: "space-between", padding: "10px 20px", backgroundColor: "#f5f5f5" }}>
      <div>
        <h2>AuthApp</h2>
      </div>
      <div>
        {username ? (
          <>
            <span style={{ marginRight: "20px" }}>Welcome, {username}</span>
            <button onClick={handleLogout}>Logout</button>
          </>
        ) : (
          <button onClick={() => (window.location.href = `${process.env.REACT_APP_API_BASE_URL}/auth/google`)}>
            Login
          </button>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
