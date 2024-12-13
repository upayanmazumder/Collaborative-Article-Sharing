import styles from "../../../page.module.css";


export default function Home() {
  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <h1>Authentication Failed</h1>
        <p>Authentication failed as you are not logged in!</p>
        <a href='/auth'>Login here</a>
      </main>
    </div>
  );
}
