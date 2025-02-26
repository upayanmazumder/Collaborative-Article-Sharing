'use client';

import React, { useState, useEffect } from 'react';
import { onAuthStateChanged, signInWithEmailAndPassword, createUserWithEmailAndPassword } from 'firebase/auth';
import { useRouter } from 'next/navigation';
import { auth } from '../../../shared/firebase';
import styles from './auth.module.css';
import { NEXT_PUBLIC_API_URL } from '../../../shared/api';

const Auth = () => {
  const [user, setUser] = useState(null);
  const [showLogin, setShowLogin] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser);

      if (currentUser) {
        router.push('/dashboard');
      }
    });

    return () => unsubscribe();
  }, [router]);

  const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState(false);

    const handleLogin = async (e) => {
      e.preventDefault();
      setError('');
      setSuccess(false);

      try {
        const userCredential = await signInWithEmailAndPassword(auth, email, password);
        console.log('User logged in:', userCredential.user);
        setSuccess(true);
      } catch (err) {
        console.error('Error logging in:', err);
        setError(err.message);
      }
    };

    return (
      <div>
        <form className={styles.authForm} onSubmit={handleLogin}>
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button type="submit">Login</button>
        </form>
        {success && <p className={`${styles.authMessage} ${styles.success}`}>Login successful!</p>}
        {error && <p className={`${styles.authMessage} ${styles.error}`}>{error}</p>}
      </div>
    );
  };

  const Signup = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState(false);

    const handleSignup = async (e) => {
      e.preventDefault();
      setError('');
      setSuccess(false);

      try {
        const response = await fetch(`${NEXT_PUBLIC_API_URL}/auth/signup`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            email: email,
            password: password,
          }),
        });

        const data = await response.json();
        console.log('API Response:', data);

        if (!response.ok) {
          setError(data.error || 'Failed to sign up in API');
          return;
        }

        const userCredential = await createUserWithEmailAndPassword(auth, email, password);
        console.log('User signed up with Firebase:', userCredential.user);

        setSuccess(true);
        console.log('User created successfully:', userCredential.user);

        router.push('/dashboard');
      } catch (err) {
        console.error('Error signing up:', err);
        setError(err.message || 'Something went wrong');
      }
    };

    return (
      <div>
        <form className={styles.authForm} onSubmit={handleSignup}>
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button type="submit">Sign Up</button>
        </form>
        {success && <p className={`${styles.authMessage} ${styles.success}`}>Sign up successful!</p>}
        {error && <p className={`${styles.authMessage} ${styles.error}`}>{error}</p>}
      </div>
    );
  };

  return (
    <div className={styles.authContainer}>
      {user ? (
        <div>
          <h2 className={styles.authHeader}>Welcome, {user.email}</h2>
          <p className={styles.authMessage}>You are already signed in.</p>
          <br />
        </div>
      ) : (
        <div>
          <h2 className={styles.authHeader}>{showLogin ? 'Login' : 'Signup'}</h2>
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
