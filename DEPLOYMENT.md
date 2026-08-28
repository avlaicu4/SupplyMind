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
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-5.6-luna
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

## Hosted AI

The AI assistant uses the OpenAI API from the backend.

Create an API key in the OpenAI dashboard and add it only to the backend cloud service:

```text
OPENAI_API_KEY=your_openai_api_key_here
```

Do not add the OpenAI API key to Vercel or frontend code.
