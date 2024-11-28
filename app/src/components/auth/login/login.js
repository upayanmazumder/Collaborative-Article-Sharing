'use client';

import React, { useState } from 'react';
import { signInWithEmailAndPassword } from 'firebase/auth';
import { auth } from '../../../../shared/firebase';
import styles from '../auth.module.css';

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

export default Login;
