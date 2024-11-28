'use client';

import React, { useState } from 'react';
import { signOut } from 'firebase/auth';
import { auth } from '../../../../shared/firebase';
import styles from '../auth.module.css';

const Logout = () => {
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleLogout = async () => {
    setError('');
    setSuccess(false);

    try {
      await signOut(auth);
      console.log('User logged out');
      setSuccess(true);
    } catch (err) {
      console.error('Error logging out:', err);
      setError(err.message);
    }
  };

  return (
    <div>
      <form className={styles.authForm}>
        <button onClick={handleLogout}>Logout</button>
      </form>
      {success && <p className={`${styles.authMessage} ${styles.success}`}>Logout successful!</p>}
      {error && <p className={`${styles.authMessage} ${styles.error}`}>{error}</p>}
    </div>
  );
};

export default Logout;