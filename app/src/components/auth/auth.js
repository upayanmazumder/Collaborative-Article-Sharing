'use client';

import React, { useState, useEffect } from 'react';
import { onAuthStateChanged } from 'firebase/auth';
import { auth } from '../../../shared/firebase';
import Login from './login/login';
import Signup from './signup/signup';
import Logout from './logout/logout';
import styles from './auth.module.css';

const Auth = () => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser);
    });

    // Cleanup the subscription when the component is unmounted
    return () => unsubscribe();
  }, []);

  return (
    <div className={styles.authContainer}>
      {user ? (
        <div>
          <h2>Welcome, {user.email}</h2>
          <p>You are already signed in.</p>
          <Logout />
        </div>
      ) : (
        <div>
          <Login />
          <Signup />
        </div>
      )}
    </div>
  );
};

export default Auth;
