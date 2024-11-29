'use client';

import React, { useState } from 'react';
import { createUserWithEmailAndPassword } from 'firebase/auth';
import { auth } from '../../../../shared/firebase';
import styles from '../auth.module.css';
import { useRouter } from 'next/navigation';  // Import the router to handle the redirection

const Signup = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const router = useRouter();  // Use router for redirection

  const handleSignup = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess(false);

    try {
      // Step 1: Send request to the API to sign up
      const response = await fetch('https://api.cas.upayan.dev/auth/signup', {
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
        return; // Exit if API call fails
      }

      // Step 2: If API call is successful, proceed with Firebase Authentication
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      console.log('User signed up with Firebase:', userCredential.user);

      setSuccess(true);
      console.log('User created successfully:', userCredential.user);

      // Only redirect after the user is signed up successfully
      router.push('/dashboard'); // Redirect to dashboard after signup
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

export default Signup;
