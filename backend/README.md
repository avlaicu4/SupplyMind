# SupplyMind Backend

FastAPI backend for the SupplyMind procurement assistant.

The AI assistant uses a hosted Claude model through the Anthropic API.

## Run the API

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API runs at:

```text
http://127.0.0.1:8000
```

Swagger docs:

```text
http://127.0.0.1:8000/docs
```

Local environment variables:

```bash
export ANTHROPIC_API_KEY="your_api_key_here"
export ANTHROPIC_MODEL="claude-haiku-4-5"
```

## Run the MCP server

The MCP server exposes procurement tools for AI agents:

- `list_low_stock_products`
- `get_reorder_recommendations`
- `list_supplier_options_for_product`
- `create_draft_purchase_order`

Run it with stdio transport:

```bash
cd backend
source venv/bin/activate
python -m app.mcp_server
```

For interactive testing with MCP Inspector:

```bash
cd backend
source venv/bin/activate
mcp dev app/mcp_server.py
```
