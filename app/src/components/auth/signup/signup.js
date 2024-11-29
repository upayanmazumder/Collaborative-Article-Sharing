'use client';

import React, { useState } from 'react';
import { createUserWithEmailAndPassword } from 'firebase/auth';
import { auth } from '../../../../shared/firebase';
import styles from '../auth.module.css';

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
      // Step 1: Create user with Firebase Auth
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      console.log('User signed up:', userCredential.user);
      
      // Step 2: Send request to your API to update Firebase database
      const response = await fetch('https://api.cas.upayan.dev/auth/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: userCredential.user.email,
          password: password,  // You may choose not to send password if not required
        }),
      });

      const data = await response.json();
      
      if (response.ok) {
        setSuccess(true);
        console.log('User data updated in Firebase:', data);
      } else {
        setError(data.error || 'Failed to update user data');
      }
    } catch (err) {
      console.error('Error signing up:', err);
      setError(err.message);
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
