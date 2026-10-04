# SupplyMind

SupplyMind is a full-stack procurement and inventory planning application for small businesses. It helps a business monitor stock levels, identify low-stock products, compare suppliers, generate reorder recommendations, and create draft purchase orders.

SupplyMind is a personal learning project for exploring how to connect LLMs to real business data. It combines a Python backend, a React frontend, a hosted Claude AI assistant, and MCP tools for agent integrations.

## Live Demo

Frontend:

```text
https://supply-mind-ten.vercel.app
```

Backend:

```text
https://supplymind-api-l0pi.onrender.com
```

Backend API docs:

```text
https://supplymind-api-l0pi.onrender.com/docs
```

## Features

- Inventory dashboard with product stock status
- Low-stock detection based on current and minimum stock
- Supplier overview with reliability ratings
- AI-generated reorder recommendations
- Draft purchase order creation
- AI assistant powered by Claude through the Anthropic API
- MCP server exposing procurement tools for AI agents
- Cloud deployment with Render and Vercel

## Tech Stack

Frontend:

- React
- Vite
- CSS
- Lucide React icons

Backend:

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Anthropic Claude API
- MCP Python SDK

Deployment:

- Render for the FastAPI backend
- Vercel for the React frontend
- GitHub for source control and automatic deployments

## Architecture

```text
React frontend
    |
    | HTTP requests
    v
FastAPI backend
    |
    | SQLAlchemy
    v
SQLite database

FastAPI backend
    |
    | Anthropic SDK
    v
Claude hosted AI API

MCP clients / AI agents
    |
    | MCP tools
    v
SupplyMind MCP server
    |
    v
Backend business logic
```

## AI Assistant

The AI assistant is exposed in the React dashboard through the `AI Assistant` panel. The frontend sends the user's question to the backend endpoint:

```text
POST /ai/chat
```

The backend collects current reorder recommendations from the inventory service and sends them to Claude with a system prompt that prevents the assistant from inventing products, suppliers, prices, or delivery times.

The API key is stored only in the backend environment:

```text
ANTHROPIC_API_KEY
ANTHROPIC_MODEL
```

The frontend never receives or stores the Claude API key.

## MCP Tools

SupplyMind also includes an MCP server for agent-style tool usage.

Available MCP tools:

- `list_low_stock_products`
- `get_reorder_recommendations`
- `list_supplier_options_for_product`
- `create_draft_purchase_order`

The MCP server is implemented in:

```text
backend/app/mcp_server.py
```

Run it locally:

```bash
cd backend
source venv/bin/activate
python -m app.mcp_server
```

Run it with MCP Inspector:

```bash
cd backend
source venv/bin/activate
mcp dev app/mcp_server.py
```

## Local Setup

Clone the repository:

```bash
git clone https://github.com/avlaicu4/SupplyMind.git
cd SupplyMind
```

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY="your_anthropic_api_key_here"
export ANTHROPIC_MODEL="claude-haiku-4-5"
uvicorn app.main:app --reload
```

The backend runs at:

```text
http://127.0.0.1:8000
```

### Frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend runs at:

```text
http://localhost:5173
```

For local development, the frontend uses:

```text
http://127.0.0.1:8000
```

as the default backend URL.

## Cloud Deployment

The app is deployed in two parts:

- Backend on Render
- Frontend on Vercel

Frontend environment variable:

```text
VITE_API_URL=https://supplymind-api-l0pi.onrender.com
```

Backend environment variables:

```text
CORS_ORIGINS=https://supply-mind-ten.vercel.app
ANTHROPIC_API_KEY=your_anthropic_api_key_here
ANTHROPIC_MODEL=claude-haiku-4-5
```

More deployment details are available in:

```text
DEPLOYMENT.md
```

## Main API Endpoints

```text
GET  /
GET  /health
GET  /products
POST /products
GET  /suppliers
POST /suppliers
GET  /ai/recommendations
POST /ai/chat
GET  /purchase-orders
POST /purchase-orders
PATCH /purchase-orders/{purchase_order_id}/status
```

## Design Highlights

- The project separates frontend, backend, AI integration, and MCP tooling.
- The React frontend does not call the AI provider directly, which keeps secrets out of browser code.
- The FastAPI backend owns all business logic and validates purchase order creation.
- The AI assistant uses backend-generated inventory context instead of unrestricted prompting.
- MCP tools expose the same procurement capabilities to external AI agents.
- The cloud deployment uses environment variables for provider URLs, CORS, and API keys.

## Future Improvements

- Add authentication for business users
- Replace SQLite with PostgreSQL for production
- Add supplier-product management screens in the frontend
- Add charts for stock risk and reorder value
- Add automated tests for backend services and API routes
- Add streaming AI responses in the chat panel
