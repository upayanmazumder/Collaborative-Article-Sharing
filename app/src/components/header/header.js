import React from 'react';
import { FaGithub, FaLink, FaDiscord, FaBox } from 'react-icons/fa'; // FaBox for PyPI
import styles from './header.module.css';

const Header = () => {
  return (
    <header className={styles.header}>
      <div className={styles.container}>
        <div className={styles.logoContainer}>
          {/* Image is served from '/cas.svg' */}
          <img src="/cas.svg" alt="CAS Logo" className={styles.icon} />
          <h1 className={styles.title}>CAS</h1>
        </div>
        <div className={styles.buttonContainer}>
          {/* Buttons for links */}
          <a href="https://github.com/upayanmazumder/Collaborative-Article-Sharing" target="_blank" rel="noopener noreferrer" className={styles.button}>
            <FaGithub className={styles.iconStyle} />
            GitHub Repo
          </a>
          <a href="https://api.cas.upayan.dev" target="_blank" rel="noopener noreferrer" className={styles.button}>
            <FaLink className={styles.iconStyle} />
            API Link
          </a>
          <a href="https://pypi.org/project/collaborative-article-sharing/" target="_blank" rel="noopener noreferrer" className={styles.button}>
            <FaBox className={styles.iconStyle} /> {/* FaBox for PyPI */}
            Pypi Repository
          </a>
          <a href="https://discord.gg/wQTZcXpcaY" target="_blank" rel="noopener noreferrer" className={styles.button}>
            <FaDiscord className={styles.iconStyle} />
            Discord
          </a>
        </div>
      </div>
    </header>
  );
};

export default Header;
