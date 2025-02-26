"use client";

import React, { useEffect } from "react";
import { onAuthStateChanged } from "firebase/auth";
import { auth } from "../../../../shared/firebase";

const Connect = () => {
  useEffect(() => {
    const authenticate = async () => {
      try {
        onAuthStateChanged(auth, async (user) => {
          if (user) {
            const email = user.email;
            const token = await user.getIdToken();
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
            window.location.href = "/auth/connect/failure";
          }
        });
      } catch (error) {
        console.error("Error fetching user details:", error);
        window.location.href = "/auth/connect/failure";
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
