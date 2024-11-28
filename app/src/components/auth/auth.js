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
  const [showLogin, setShowLogin] = useState(true); // Control which form to display

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser);
    });

    return () => unsubscribe();
  }, []);

  return (
    <div className={styles.authContainer}>
      {user ? (
        <div>
          <h2 className={styles.authHeader}>Welcome, {user.email}</h2>
          <p className={styles.authMessage}>
            You are already signed in.
          </p>
          <br />
          <Logout />
        </div>
      ) : (
        <div>
          <h2 className={styles.authHeader}>
            {showLogin ? 'Login' : 'Signup'}
          </h2>
          <div className={styles.toggleContainer}>
            <button
              className={`${styles.button} ${showLogin ? styles.active : ''}`}
              onClick={() => setShowLogin(true)}
            >
              Login
            </button>
            <button
              className={`${styles.button} ${!showLogin ? styles.active : ''}`}
              onClick={() => setShowLogin(false)}
            >
              Signup
            </button>
          </div>
          <div className={styles.authForm}>
            {showLogin ? <Login /> : <Signup />}
          </div>
        </div>
      )}
    </div>
  );
};

export default Auth;
