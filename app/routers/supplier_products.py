from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import ProductModel, SupplierModel, SupplierProductModel
from ..schemas import SupplierProduct, SupplierProductCreate

router = APIRouter(prefix="/supplier-products", tags=["Supplier Products"])


@router.get("", response_model=list[SupplierProduct])
def get_supplier_products(db: Session = Depends(get_db)):
    return db.query(SupplierProductModel).all()


@router.post("", response_model=SupplierProduct)
def create_supplier_product(
    supplier_product: SupplierProductCreate,
    db: Session = Depends(get_db),
):
    supplier = (
        db.query(SupplierModel)
        .filter(SupplierModel.id == supplier_product.supplier_id)
        .first()
    )

    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")

    product = (
        db.query(ProductModel)
        .filter(ProductModel.id == supplier_product.product_id)
        .first()
    )

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    new_supplier_product = SupplierProductModel(
        supplier_id=supplier_product.supplier_id,
        product_id=supplier_product.product_id,
        unit_price=supplier_product.unit_price,
        delivery_days=supplier_product.delivery_days,
    )

    db.add(new_supplier_product)
    db.commit()
    db.refresh(new_supplier_product)

    return new_supplier_product