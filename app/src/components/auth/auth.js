'use client';

import React, { useState, useEffect } from 'react';
import { onAuthStateChanged, signOut } from 'firebase/auth';
import { useRouter } from 'next/navigation';
import { auth } from '../../../shared/firebase';
import Login from './login/login';
import Signup from './signup/signup';
import Logout from './logout/logout';
import styles from './auth.module.css';

const Auth = () => {
  const [user, setUser] = useState(null);
  const [showLogin, setShowLogin] = useState(true); // Control which form to display
  const router = useRouter();

  useEffect(() => {
    // Listen to authentication state changes
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser);

      // Redirect to dashboard if logged in
      if (currentUser) {
        router.push('/dashboard');
      }
    });

    return () => unsubscribe();
  }, [router]);

  const handleLogout = async () => {
    try {
      await signOut(auth);
      setUser(null);
      setShowLogin(true); // Reset to Login view
      router.push('/auth'); // Redirect to auth page
    } catch (error) {
      console.error('Logout failed:', error.message);
    }
  };

  return (
    <div className={styles.authContainer}>
      {user ? (
        <div>
          <h2 className={styles.authHeader}>Welcome, {user.email}</h2>
          <p className={styles.authMessage}>
            You are already signed in.
          </p>
          <br />
          <Logout onLogout={handleLogout} />
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
