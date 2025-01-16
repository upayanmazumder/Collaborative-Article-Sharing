import styles from "./page.module.css";

export default function Home() {
  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <h1>Welcome to the CAS Homepage</h1>
        <p>To get started, install the Collaborative Article Sharing package:</p>
        <pre>
          <code>pip install collaborative-article-sharing</code>
        </pre>
        <p>Then run the following command:</p>
        <pre>
          <code>cas</code>
        </pre>
      </main>
    </div>
  );
}
