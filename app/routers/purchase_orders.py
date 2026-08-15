from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import ProductModel, PurchaseOrderModel, SupplierModel
from ..schemas import PurchaseOrder, PurchaseOrderCreate, PurchaseOrderStatusUpdate

router = APIRouter(prefix="/purchase-orders", tags=["Purchase Orders"])


@router.get("", response_model=list[PurchaseOrder])
def get_purchase_orders(db: Session = Depends(get_db)):
    return db.query(PurchaseOrderModel).all()


@router.post("", response_model=PurchaseOrder)
def create_purchase_order(
    purchase_order: PurchaseOrderCreate,
    db: Session = Depends(get_db),
):
    product = (
        db.query(ProductModel)
        .filter(ProductModel.id == purchase_order.product_id)
        .first()
    )

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    supplier = (
        db.query(SupplierModel)
        .filter(SupplierModel.id == purchase_order.supplier_id)
        .first()
    )

    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")

    new_purchase_order = PurchaseOrderModel(
        product_id=purchase_order.product_id,
        supplier_id=purchase_order.supplier_id,
        quantity=purchase_order.quantity,
        status="draft",
    )

    db.add(new_purchase_order)
    db.commit()
    db.refresh(new_purchase_order)

    return new_purchase_order

@router.patch("/{purchase_order_id}/status", response_model=PurchaseOrder)
def update_purchase_order_status(
    purchase_order_id: int,
    status_update: PurchaseOrderStatusUpdate,
    db: Session = Depends(get_db),
):
    allowed_statuses = ["draft", "submitted", "received", "cancelled"]

    if status_update.status not in allowed_statuses:
        raise HTTPException(status_code=400, detail="Invalid purchase order status")

    purchase_order = (
        db.query(PurchaseOrderModel)
        .filter(PurchaseOrderModel.id == purchase_order_id)
        .first()
    )

    if purchase_order is None:
        raise HTTPException(status_code=404, detail="Purchase order not found")

    purchase_order.status = status_update.status

    db.commit()
    db.refresh(purchase_order)

    return purchase_order