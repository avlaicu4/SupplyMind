from sqlalchemy import Column, Float, Integer, String, DateTime

from .database import Base
from datetime import datetime


class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    current_stock = Column(Integer, nullable=False)
    minimum_stock = Column(Integer, nullable=False)
    average_daily_sales = Column(Float, nullable=False)


class SupplierModel(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    reliability_rating = Column(Float, nullable=False)


class SupplierProductModel(Base):
    __tablename__ = "supplier_products"

    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, nullable=False)
    product_id = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    delivery_days = Column(Integer, nullable=False)

class PurchaseOrderModel(Base):
    __tablename__ = "purchase_orders"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, nullable=False)
    supplier_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(String, nullable=False, default="draft")
    created_at = Column(DateTime, default=datetime.utcnow)