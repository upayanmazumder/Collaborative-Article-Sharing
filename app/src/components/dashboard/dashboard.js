'use client';

import { useEffect, useState } from 'react';
import styles from './dashboard.module.css';
import Image from 'next/image';

export default function Home() {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchArticles = async () => {
      try {
        const user = await firebase.auth().currentUser;

        if (user) {
          const idToken = await user.getIdToken();

          const response = await fetch('https://api.cas.upayan.dev/pull', {
            method: 'GET',
            headers: {
              Authorization: `Bearer ${idToken}`,
            },
          });

          if (!response.ok) {
            throw new Error('Failed to fetch articles');
          }

          const data = await response.json();
          if (data.success) {
            setArticles(data.articles);
          } else {
            setError('No articles found');
          }
        } else {
          setError('User is not signed in');
        }
      } catch (err) {
        setError(err.message || 'An error occurred while fetching articles');
      } finally {
        setLoading(false);
      }
    };

    fetchArticles();
  }, [setArticles, setError, setLoading]);

  return (
    <div className={styles.page}>
      <main className={styles.main}>
        {loading ? (
          <p>Loading articles...</p>
        ) : error ? (
          <p>Error: {error}</p>
        ) : articles.length === 0 ? (
          <p>No articles available</p>
        ) : (
          <div>
            <h2>Your Articles</h2>
            <ul>
              {articles.map((article, index) => (
                <li key={index}>{article}</li>
              ))}
            </ul>
          </div>
        )}
      </main>
    </div>
  );
}
