# Collaborative-Article-Sharing

<img src='https://cas.upayan.dev/favicon.ico' height=50px>

A collaborative article-sharing system designed for seamless content exchange and engagement.

## Links

[![Site Button](https://img.shields.io/badge/Site-cas.upayan.dev-brightblue?style=for-the-badge&logo=github&logoColor=white)](https://cas.upayan.dev)  
[![API Button](https://img.shields.io/badge/API-api.cas.upayan.dev-brightgreen?style=for-the-badge&logo=github&logoColor=white)](https://api.cas.upayan.dev)  
[![PyPI Button](https://img.shields.io/badge/PyPI-CAS-orange?style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/collaborative-article-sharing/)  
[![Discord Button](https://img.shields.io/badge/Discord-Join%20Community-blue?style=for-the-badge&logo=discord&logoColor=white)](https://discord.com/invite/wQTZcXpcaY)

---

## CLI Tool

Install the CLI tool with:

```bash
pip install collaborative-article-sharing
```

### Commands

For detailed instructions on using the CLI, refer to its [README file](./CLI/README.md).

---

## Ports

| Service            | Port |
|--------------------|------|
| APP                | 3000 |
| API                | 4000 |
| CLI Authentication | 8000 |

---

## Developer Guide

### Environment Setup

1. Fill the `.env` file in the root directory and the `app` directory with the required environment variables. 

### Package Installation

- For the **APP** folder, navigate to the `app` directory and run:

  ```bash
  npm install
  ```

- For the **API** and **CLI** folders, navigate to their directories and run:

  ```bash
  pip install -r requirements.txt
  ```

### Running the Project

- To start the **APP**, navigate to the `app` directory and run:

  ```bash
  npm run dev
  ```

- To start the **API**, navigate to the `api` directory and run:

  ```bash
  python main.py
  ```

- To run the **CLI**, refer to its [README file](./CLI/README.md).
