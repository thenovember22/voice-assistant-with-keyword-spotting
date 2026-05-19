# Maya - AI Voice Assistant

A single-page React + Flask voice assistant with wake-word flow, calculator support, and music commands.

## Local setup

### Backend

```powershell
cd server
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_real_groq_api_key_here
```

### Frontend

Open a second terminal:

```powershell
cd client
npm install
npm run dev
```

## Deploy on Render

This repo is a monorepo with two deployable apps:

```text
/server  -> Flask API
/client  -> React/Vite frontend
```

### 1. Push the project to GitHub

Render deploys from a linked Git repo, so commit and push the project first.

### 2. Create the Flask backend service

In Render:

1. Click `New` -> `Web Service`
2. Connect your GitHub repo
3. Set `Root Directory` to `server`
4. Use:
   - Runtime: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
5. Add environment variable:

```text
GROQ_API_KEY=your_real_groq_api_key_here
```

6. Deploy it

After deploy, copy the backend URL, for example:

```text
https://maya-backend.onrender.com
```

### 3. Create the frontend static site

In Render:

1. Click `New` -> `Static Site`
2. Connect the same repo
3. Set `Root Directory` to `client`
4. Use:
   - Build Command: `npm install && npm run build`
   - Publish Directory: `dist`
5. Add environment variable:

```text
VITE_API_BASE_URL=https://your-backend-name.onrender.com
```

6. Deploy it

Your public résumé link will be the frontend static-site URL.

## Notes

- Open the deployed frontend over HTTPS and click `Start Voice Mode` once so the browser can request microphone/audio permission.
- After that: say `Maya`, then commands like `what is the time`, `what is 12 times 5`, `play senorita`, or `goodbye`.
- If a command is not one of Maya's built-in actions, it is sent to Groq for a general answer.
- `client/.env.example` shows the production frontend environment variable you need on Render.
