import styles from "../../page.module.css";

import Signup from "../../../components/auth/signup/signup";

export default function Home() {
  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <Signup />
      </main>
    </div>
  );
}
