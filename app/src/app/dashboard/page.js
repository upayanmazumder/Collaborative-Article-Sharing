import { useEffect, useState } from "react";
import styles from "../page.module.css";
import Dashboard from "../../components/dashboard/dashboard";

export default function Home() {
  const [articles, setArticles] = useState<string[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Get Firebase ID token for authentication
    const fetchArticles = async () => {
      try {
        // Assuming Firebase is initialized and Firebase Auth is available
        const user = await firebase.auth().currentUser;
        
        if (user) {
          const idToken = await user.getIdToken();

          // Fetch articles from the API
          const response = await fetch("https://api.cas.upayan.dev/pull", {
            method: "GET",
            headers: {
              Authorization: `Bearer ${idToken}`,
            },
          });

          if (!response.ok) {
            throw new Error("Failed to fetch articles");
          }

          const data = await response.json();
          if (data.success) {
            setArticles(data.articles);
          } else {
            setError("No articles found");
          }
        } else {
          setError("User is not signed in");
        }
      } catch (err) {
        setError(err.message || "An error occurred while fetching articles");
      } finally {
        setLoading(false);
      }
    };

    fetchArticles();
  }, []);

  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <Dashboard />
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
