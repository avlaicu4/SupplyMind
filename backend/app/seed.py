from .data import products, suppliers, supplier_products
from .models import ProductModel, SupplierModel, SupplierProductModel


def seed_database(db):
    existing_product = db.query(ProductModel).first()

    if existing_product is not None:
        return

    for product in products:
        db.add(ProductModel(**product))

    for supplier in suppliers:
        db.add(SupplierModel(**supplier))

    for supplier_product in supplier_products:
        db.add(SupplierProductModel(**supplier_product))

    db.commit()