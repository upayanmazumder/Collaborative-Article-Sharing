"use client"

import React, { useEffect } from "react";
import { getAuth } from "firebase/auth";

const Connect = () => {
  useEffect(() => {
    const authenticate = async () => {
      try {
        const auth = getAuth();
        const user = auth.currentUser;

        if (user) {
          // Get the user's email and ID token
          const email = user.email;
          const token = await user.getIdToken();

          // Redirect to the provided redirect URI
          const params = new URLSearchParams(window.location.search);
          const redirectUri = params.get("redirect_uri");

          if (redirectUri) {
            const redirectUrl = `${redirectUri}?email=${encodeURIComponent(
              email
            )}&token=${encodeURIComponent(token)}`;
            window.location.href = redirectUrl;
          } else {
            console.error("Missing redirect URI.");
          }
        } else {
          console.error("No user is signed in.");
        }
      } catch (error) {
        console.error("Error fetching user details:", error);
      }
    };

    authenticate();
  }, []);

  return (
    <div>
      <h1>Connecting...</h1>
      <p>Please wait while we authenticate you.</p>
    </div>
  );
};

export default Connect;