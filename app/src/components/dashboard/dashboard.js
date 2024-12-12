'use client';

import React, { useState, useEffect } from 'react';
import { onAuthStateChanged, signOut } from 'firebase/auth';
import { useRouter } from 'next/navigation';
import { auth } from '../../../shared/firebase';
import styles from './dashboard.module.css';

const Dashboard = () => {
  const [user, setUser] = useState(null);
  const router = useRouter();

  useEffect(() => {
    // Listen to authentication state changes
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      if (currentUser) {
        setUser(currentUser);
      } else {
        router.push('/auth'); // Redirect to auth page if no user is logged in
      }
    });

    return () => unsubscribe();
  }, [router]);

  const handleLogout = async () => {
    try {
      await signOut(auth);
      setUser(null);
      router.push('/auth'); // Redirect to auth page after logout
    } catch (error) {
      console.error('Logout failed:', error.message);
    }
  };

  return (
    <div className={styles.dashboardContainer}>
      {user ? (
        <div>
          <h2 className={styles.dashboardHeader}>Welcome to your Dashboard, {user.email}</h2>
          <div className={styles.dashboardContent}>
            <p className={styles.dashboardMessage}>
              Here you can manage your account, settings, and more.
            </p>
            <br />
            <button
              className={styles.logoutButton}
              onClick={handleLogout}
            >
              Logout
            </button>
          </div>
        </div>
      ) : (
        <div>
          <h2 className={styles.dashboardHeader}>Loading...</h2>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
