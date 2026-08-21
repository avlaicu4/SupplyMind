from .models import ProductModel, SupplierModel, SupplierProductModel


def get_low_stock_products(db):
    return (
        db.query(ProductModel)
        .filter(ProductModel.current_stock < ProductModel.minimum_stock)
        .all()
    )


def find_supplier_by_id(db, supplier_id):
    return (
        db.query(SupplierModel)
        .filter(SupplierModel.id == supplier_id)
        .first()
    )


def get_supplier_options_for_product(db, product_id):
    supplier_products = (
        db.query(SupplierProductModel)
        .filter(SupplierProductModel.product_id == product_id)
        .all()
    )

    options = []

    for supplier_product in supplier_products:
        supplier = find_supplier_by_id(db, supplier_product.supplier_id)

        if supplier is not None:
            options.append(
                {
                    "supplier_id": supplier.id,
                    "supplier_name": supplier.name,
                    "reliability_rating": supplier.reliability_rating,
                    "unit_price": supplier_product.unit_price,
                    "delivery_days": supplier_product.delivery_days,
                }
            )

    return options


def choose_best_supplier(options):
    if not options:
        return None

    best_option = options[0]

    for option in options:
        current_score = calculate_supplier_score(option)
        best_score = calculate_supplier_score(best_option)

        if current_score > best_score:
            best_option = option

    return best_option


def calculate_supplier_score(option):
    reliability_score = option["reliability_rating"] * 10
    delivery_score = 30 - option["delivery_days"]
    price_score = 1000 / option["unit_price"]

    return reliability_score + delivery_score + price_score


def generate_reorder_recommendations(db):
    recommendations = []

    for product in get_low_stock_products(db):
        stock_gap = product.minimum_stock - product.current_stock
        weekly_demand = product.average_daily_sales * 7
        recommended_quantity = round(stock_gap + weekly_demand)

        supplier_options = get_supplier_options_for_product(db, product.id)
        best_supplier = choose_best_supplier(supplier_options)

        if best_supplier is None:
            supplier_reason = "No supplier is currently available for this product."
            recommended_supplier_id = None
            recommended_supplier_name = None
            estimated_unit_price = None
            estimated_delivery_days = None
        else:
            supplier_reason = (
                f"Recommended supplier is {best_supplier['supplier_name']} "
                f"with unit price {best_supplier['unit_price']}, "
                f"delivery in {best_supplier['delivery_days']} days, "
                f"and reliability rating {best_supplier['reliability_rating']}."
            )
            recommended_supplier_id = best_supplier["supplier_id"]
            recommended_supplier_name = best_supplier["supplier_name"]
            estimated_unit_price = best_supplier["unit_price"]
            estimated_delivery_days = best_supplier["delivery_days"]

        recommendations.append(
            {
                "product_id": product.id,
                "product_name": product.name,
                "current_stock": product.current_stock,
                "minimum_stock": product.minimum_stock,
                "recommended_quantity": recommended_quantity,
                "recommended_supplier_id": recommended_supplier_id,
                "recommended_supplier_name": recommended_supplier_name,
                "estimated_unit_price": estimated_unit_price,
                "estimated_delivery_days": estimated_delivery_days,
                "reason": (
                    f"{product.name} is below minimum stock. "
                    f"Current stock is {product.current_stock}, "
                    f"minimum stock is {product.minimum_stock}, "
                    f"and estimated weekly demand is {weekly_demand:.1f} units. "
                    f"{supplier_reason}"
                ),
            }
        )

    return recommendations