from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import ProductModel
from ..schemas import Product, ProductCreate

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=list[Product])
def get_products(db: Session = Depends(get_db)):
    return db.query(ProductModel).all()


@router.get("/low-stock", response_model=list[Product])
def get_low_stock(db: Session = Depends(get_db)):
    return (
        db.query(ProductModel)
        .filter(ProductModel.current_stock < ProductModel.minimum_stock)
        .all()
    )

@router.post("", response_model=Product)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = ProductModel(
        name=product.name,
        category=product.category,
        current_stock=product.current_stock,
        minimum_stock=product.minimum_stock,
        average_daily_sales=product.average_daily_sales,
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product