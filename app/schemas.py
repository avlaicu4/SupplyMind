from pydantic import BaseModel
from datetime import datetime

class Product(BaseModel):
    id: int
    name: str
    category: str
    current_stock: int
    minimum_stock: int
    average_daily_sales: float


class Supplier(BaseModel):
    id: int
    name: str
    reliability_rating: float


class SupplierProduct(BaseModel):
    id: int
    supplier_id: int
    product_id: int
    unit_price: float
    delivery_days: int


class ReorderRecommendation(BaseModel):
    product_id: int
    product_name: str
    current_stock: int
    minimum_stock: int
    recommended_quantity: int
    reason: str


class ReorderRecommendation(BaseModel):
    product_id: int
    product_name: str
    current_stock: int
    minimum_stock: int
    recommended_quantity: int
    recommended_supplier_id: int | None
    recommended_supplier_name: str | None
    estimated_unit_price: float | None
    estimated_delivery_days: int | None
    reason: str


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    answer: str

class ProductCreate(BaseModel):
    name: str
    category: str
    current_stock: int
    minimum_stock: int
    average_daily_sales: float


class SupplierCreate(BaseModel):
    name: str
    reliability_rating: float

class SupplierProductCreate(BaseModel):
    supplier_id: int
    product_id: int
    unit_price: float
    delivery_days: int

class PurchaseOrder(BaseModel):
    id: int
    product_id: int
    supplier_id: int
    quantity: int
    status: str
    created_at: datetime


class PurchaseOrderCreate(BaseModel):
    product_id: int
    supplier_id: int
    quantity: int

class PurchaseOrderStatusUpdate(BaseModel):
    status: str