// import React, { useEffect, useContext } from "react";
// import { useNavigate } from "react-router-dom";
// import { UserContext } from "../App";
// import { handleCallback } from "../utils/auth";

// const Callback = () => {
//   const navigate = useNavigate();
//   const { setIsLoggedIn, setUser } = useContext(UserContext);

//   useEffect(() => {
//     handleCallback()
//       .then((userDetails) => {
//         setIsLoggedIn(true);
//         setUser(userDetails);
//         navigate("/");
//       })
//       .catch(() => {
//         setIsLoggedIn(false);
//         navigate("/");
//       });
//   }, [navigate, setIsLoggedIn, setUser]);

//   return <div>Processing Login...</div>;
// };

// export default Callback;
