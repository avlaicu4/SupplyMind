# SupplyMind Cloud Deployment

Deploy the app in two parts:

1. Backend: FastAPI service
2. Frontend: Vite React static site

## Backend

Recommended beginner options:

- Railway
- Render

The backend must run from the `backend` folder.

Build command:

```bash
pip install -r requirements.txt
```

Start command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Health check path:

```text
/health
```

Environment variables:

```text
CORS_ORIGINS=https://your-frontend-url.vercel.app
```

After deployment, copy the public backend URL. It should look like:

```text
https://your-backend-url.onrender.com
```

or:

```text
https://your-backend-url.up.railway.app
```

## Frontend

Recommended option:

- Vercel

The frontend must run from the `frontend` folder.

Build command:

```bash
npm run build
```

Output directory:

```text
dist
```

Environment variables:

```text
VITE_API_URL=https://your-backend-url.example.com
```

Use the real backend URL from Railway or Render.

## Important AI Note

The local Ollama model runs on your Mac, so a cloud backend cannot reach it automatically.

For a public cloud demo, choose one:

1. Keep AI chat as a local-only feature and deploy the rest of the app.
2. Replace Ollama with a hosted LLM API for the cloud version.
3. Deploy Ollama separately on a server with enough CPU/RAM.

For an interview MVP, option 1 is acceptable if you explain it clearly.
