from pydantic import BaseModel


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