# PromptAssist 

**Your Personal AI-Powered Prompt Manager**

[![Quick Demo](https://img.youtube.com/vi/oFcH-L0bwaI/maxresdefault.jpg)](https://youtu.be/oFcH-L0bwaI)

---

**Installation:** https://github.com/EricJujianZou/PromptAssist/releases/tag/v1.0.0

## What is PromptAssist?

PromptAssist is a Windows utility that runs in your system tray with two core abilities:

-   **Snippet Expansion:** Type a command (like `::emailstarter`) to replace it with longer text. Use for code boilerplate, common replies, or text you type often.
-   **LLM Augmentation:** Use the prefix `::Prompt([your-prompt-here)` to transform your prompt with added accuracy and context.

## Key Features

-   **System-Wide:** Works in code editors, browsers, and text fields.
-   **Lightweight:** Runs in system tray with minimal resources.
-   **Customizable:** Add, edit, and manage snippets through a dashboard.
-   **Secure:** Connects to self-hosted API backend for LLM prompts.
-   **No Installation:** Download and run the `.exe` file.

## Getting Started

1.  Download `PromptAssist.exe` from the [release page](https://github.com/EricJujianZou/PromptAssist/releases/tag/v1.0.0)
2.  Run the file
3.  The icon appears in your system tray

## How to Use

-   **Double-click** the tray icon to manage snippets
-   **Type a snippet command** (e.g., `::emailstarter`) to expand it
-   **Type an LLM command** (e.g., `::Prompt(explain Bayes' Theorem)`) to transform your prompt

## For Developers: Running from Source

The project has two parts:
1.  **Backend:** FastAPI server connecting to the language model
2.  **Client:** PySide6 GUI running in system tray

### Prerequisites

-   [Python 3.9+](https://www.python.org/downloads/)
-   [Git](https://git-scm.com/downloads/)
-   [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### Step 1: Clone the Repository

```shell
git clone https://github.com/EricJujianZou/PromptAssist.git
cd PromptAssist
```

### Step 2: Set Up Redis

1.  Start Docker Desktop
2.  Run Redis container:

    ```shell
    docker run -d -p 6379:6379 --name prompt-redis redis
    ```

### Step 3: Set Up the Backend

1.  Navigate to backend:
    ```shell
    cd backend_api
    ```

2.  Create and activate virtual environment:
    ```shell
    python -m venv venv
    .\venv\Scripts\activate  # Windows
    or if that doesn't work:
    .\venv\bin\activate.ps1
    ```

3.  Install dependencies:
    ```shell
    pip install -r requirements_backend.txt
    ```

4.  Configure environment:
    -   Create `.env` in `backend_api`
    -   Copy contents from `.env.example`
    -   Set values:
        -   `VERTEX_AI_PROJECT`: Your Google Cloud Project ID
        -   `VERTEX_AI_LOCATION`: Region (e.g., `us-central1`)
        -   `BACKEND_API_KEY`: Create a random secret key
        -   `REDIS_URL`: Use `redis://localhost`

5.  Authenticate with Google Cloud:
    ```shell
    gcloud auth application-default login
    ```

6.  Run the backend:
    ```shell
    uvicorn main:app --reload
    ```
    Server runs on `http://127.0.0.1:8000`. **Leave this terminal open.**

### Step 4: Set Up the Client

1.  Open a new terminal in project root

2.  Create virtual environment:
    ```shell
    python -m venv venv_client
    .\venv_client\Scripts\activate  # Windows
    ```

3.  Install dependencies:
    ```shell
    pip install -r documentation/requirements.txt
    ```

4.  Configure environment:
    -   Create `.env` in `src`
    -   Copy from `src/.env.example`
    -   Set values:
        -   `BACKEND_API_URL`: `http://127.0.0.1:8000`
        -   `BACKEND_API_KEY`: Same key from backend's `.env`

5.  Run the client:
    ```shell
    python run.py
    ```

The icon appears in your system tray, connected to your local backend and Redis.

## License

MIT License. See `LICENSE` file.
