from contextlib import contextmanager
from typing import Any

from mcp.server import MCPServer

from app.database import Base, SessionLocal, engine
from app.inventory_services import (
    generate_reorder_recommendations,
    get_low_stock_products,
    get_supplier_options_for_product,
)
from app.models import ProductModel, PurchaseOrderModel, SupplierModel
from app.seed import seed_database

mcp = MCPServer(
    "SupplyMind MCP",
    instructions=(
        "Use these procurement tools to inspect inventory risk, compare suppliers, "
        "generate reorder recommendations, and create draft purchase orders."
    ),
)


def initialize_database() -> None:
    Base.metadata.create_all(bind=engine)

    with database_session() as db:
        seed_database(db)


@contextmanager
def database_session():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def product_to_dict(product: ProductModel) -> dict[str, Any]:
    return {
        "id": product.id,
        "name": product.name,
        "category": product.category,
        "current_stock": product.current_stock,
        "minimum_stock": product.minimum_stock,
        "average_daily_sales": product.average_daily_sales,
    }


def supplier_to_dict(supplier: SupplierModel) -> dict[str, Any]:
    return {
        "id": supplier.id,
        "name": supplier.name,
        "reliability_rating": supplier.reliability_rating,
    }


def purchase_order_to_dict(order: PurchaseOrderModel) -> dict[str, Any]:
    return {
        "id": order.id,
        "product_id": order.product_id,
        "supplier_id": order.supplier_id,
        "quantity": order.quantity,
        "status": order.status,
        "created_at": order.created_at.isoformat(),
    }


@mcp.tool()
def list_low_stock_products() -> list[dict[str, Any]]:
    """Return products where current stock is below the minimum stock threshold."""
    with database_session() as db:
        products = get_low_stock_products(db)
        return [product_to_dict(product) for product in products]


@mcp.tool()
def get_reorder_recommendations() -> list[dict[str, Any]]:
    """Generate AI-agent-ready reorder recommendations from inventory and supplier data."""
    with database_session() as db:
        return generate_reorder_recommendations(db)


@mcp.tool()
def list_supplier_options_for_product(product_id: int) -> dict[str, Any]:
    """Return supplier options, pricing, delivery time, and reliability for a product."""
    with database_session() as db:
        product = db.query(ProductModel).filter(ProductModel.id == product_id).first()

        if product is None:
            return {
                "ok": False,
                "message": f"Product with id {product_id} was not found.",
                "supplier_options": [],
            }

        return {
            "ok": True,
            "product": product_to_dict(product),
            "supplier_options": get_supplier_options_for_product(db, product_id),
        }


@mcp.tool()
def create_draft_purchase_order(
    product_id: int,
    supplier_id: int,
    quantity: int,
) -> dict[str, Any]:
    """Create a draft purchase order after validating the product, supplier, and quantity."""
    if quantity <= 0:
        return {
            "ok": False,
            "message": "Quantity must be greater than zero.",
        }

    with database_session() as db:
        product = db.query(ProductModel).filter(ProductModel.id == product_id).first()

        if product is None:
            return {
                "ok": False,
                "message": f"Product with id {product_id} was not found.",
            }

        supplier = db.query(SupplierModel).filter(SupplierModel.id == supplier_id).first()

        if supplier is None:
            return {
                "ok": False,
                "message": f"Supplier with id {supplier_id} was not found.",
            }

        purchase_order = PurchaseOrderModel(
            product_id=product_id,
            supplier_id=supplier_id,
            quantity=quantity,
            status="draft",
        )

        db.add(purchase_order)
        db.commit()
        db.refresh(purchase_order)

        return {
            "ok": True,
            "message": "Draft purchase order created.",
            "purchase_order": purchase_order_to_dict(purchase_order),
            "product": product_to_dict(product),
            "supplier": supplier_to_dict(supplier),
        }


initialize_database()


if __name__ == "__main__":
    mcp.run(transport="stdio")
