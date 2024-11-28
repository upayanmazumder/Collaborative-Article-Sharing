import React from 'react';
import { FaGithub, FaLink, FaDiscord, FaCloud, FaSignInAlt } from 'react-icons/fa';
import styles from './header.module.css';
import Link from 'next/link';

const Header = () => {
  return (
    <header className={styles.header}>
      <div className={styles.container}>
        <Link href="/" className={styles.logoContainer}>
          <img src="/cas.svg" alt="CAS Logo" className={styles.icon} />
          <h1 className={styles.title}>CAS</h1>
        </Link>
        <div className={styles.buttonContainer}>
          <a
            href="https://github.com/upayanmazumder/Collaborative-Article-Sharing"
            target="_blank"
            rel="noopener noreferrer"
            className={styles.button}
          >
            <FaGithub className={styles.iconStyle} />
            GitHub Repo
          </a>
          <a
            href="https://api.cas.upayan.dev"
            target="_blank"
            rel="noopener noreferrer"
            className={styles.button}
          >
            <FaCloud className={styles.iconStyle} />
            API Link
          </a>
          <a
            href="https://pypi.org/project/collaborative-article-sharing/"
            target="_blank"
            rel="noopener noreferrer"
            className={styles.button}
          >
            <FaLink className={styles.iconStyle} />
            Pypi Repository
          </a>
          <a
            href="https://discord.gg/wQTZcXpcaY"
            target="_blank"
            rel="noopener noreferrer"
            className={styles.button}
          >
            <FaDiscord className={styles.iconStyle} />
            Discord
          </a>
          <Link href="/auth" className={styles.button}>
            <FaSignInAlt className={styles.iconStyle} />
            Authenticate
          </Link>
        </div>
      </div>
    </header>
  );
};

export default Header;
