import React from 'react';

const User = ({ user }) => {
  return (
    <div>
      <h2>User Details</h2>
      <p>
        <strong>Username:</strong> {user.username || 'Not available'}
      </p>
      <p>
        <strong>Email:</strong> {user.email || 'Not available'}
      </p>
      <p>
        <strong>JWT Token:</strong> {user.token || 'Not available'}
      </p>
    </div>
  );
};

export default User;
