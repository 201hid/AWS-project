import React, { useState, useEffect } from "react";
import { getUserInfo } from "../utils/auth";

const UserDetails = () => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const fetchUser = async () => {
      const userInfo = await getUserInfo();
      setUser(userInfo);
    };

    fetchUser();
  }, []);

  if (!user) {
    return <p>Loading...</p>;
  }

  return (
    <div>
      <h2>User Details</h2>
      <p>Name: {user.given_name} {user.family_name}</p>
      <p>Email: {user.email}</p>
      <p>Username: {user.username}</p>
    </div>
  );
};

export default UserDetails;
