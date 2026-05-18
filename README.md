# Lilly - AI Voice Assistant

A single-page React + Flask chat app with a dark sci-fi interface and a local demo backend.

## Project structure

```text
/client  -> React + Vite frontend
/server  -> Flask backend
```

## Setup

### 1. Backend

```powershell
cd server
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

The API runs at `http://127.0.0.1:5000`.

### 2. Frontend

Open a second terminal:

```powershell
cd client
npm install
npm run dev
```

Open the local URL printed by Vite, usually `http://127.0.0.1:5173`.

## Features

- Full-screen two-panel layout
- Animated Lilly avatar with orbiting particles
- React chat history with loading indicator
- Enter-to-send behavior
- Auto-scroll to the newest message
- Mobile layout that stacks avatar above chat
- No API key or `.env` file required
