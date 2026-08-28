import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import ai, products, purchase_orders, supplier_products, suppliers
from .models import Base
from .database import SessionLocal, engine
from .seed import seed_database

default_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

cloud_origins = os.getenv("CORS_ORIGINS", "")
allowed_origins = default_origins + [
    origin.strip()
    for origin in cloud_origins.split(",")
    if origin.strip()
]

app = FastAPI(title="ProcureAI API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)
db = SessionLocal()
seed_database(db)
db.close()
app.include_router(supplier_products.router)
app.include_router(purchase_orders.router)

@app.get("/")
def home():
    return {"message": "ProcureAI backend is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(products.router)
app.include_router(suppliers.router)
app.include_router(ai.router)
