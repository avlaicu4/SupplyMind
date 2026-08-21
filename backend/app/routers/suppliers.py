from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import SupplierModel
from ..schemas import Supplier, SupplierCreate


router = APIRouter(prefix="/suppliers", tags=["Suppliers"])


@router.get("", response_model=list[Supplier])
def get_suppliers(db: Session = Depends(get_db)):
    return db.query(SupplierModel).all()

@router.post("", response_model=Supplier)
def create_supplier(supplier: SupplierCreate, db: Session = Depends(get_db)):
    new_supplier = SupplierModel(
        name=supplier.name,
        reliability_rating=supplier.reliability_rating,
    )

    db.add(new_supplier)
    db.commit()
    db.refresh(new_supplier)

    return new_supplier

@router.delete("/{supplier_id}")
def delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier = (
        db.query(SupplierModel)
        .filter(SupplierModel.id == supplier_id)
        .first()
    )

    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")

    db.delete(supplier)
    db.commit()

    return {"message": "Supplier deleted successfully"}