products = [
    {
        "id": 1,
        "name": "Office Laptop",
        "category": "Electronics",
        "current_stock": 8,
        "minimum_stock": 10,
        "average_daily_sales": 1.2,
    },
    {
        "id": 2,
        "name": "Wireless Mouse",
        "category": "Accessories",
        "current_stock": 45,
        "minimum_stock": 20,
        "average_daily_sales": 3.5,
    },
    {
        "id": 3,
        "name": "USB-C Docking Station",
        "category": "Accessories",
        "current_stock": 5,
        "minimum_stock": 12,
        "average_daily_sales": 0.8,
    },
]

suppliers = [
    {
        "id": 1,
        "name": "TechSupply Europe",
        "reliability_rating": 4.8,
    },
    {
        "id": 2,
        "name": "OfficeGear Direct",
        "reliability_rating": 4.3,
    },
]

supplier_products = [
    {
        "id": 1,
        "supplier_id": 1,
        "product_id": 1,
        "unit_price": 850.0,
        "delivery_days": 5,
    },
    {
        "id": 2,
        "supplier_id": 2,
        "product_id": 1,
        "unit_price": 820.0,
        "delivery_days": 8,
    },
    {
        "id": 3,
        "supplier_id": 1,
        "product_id": 3,
        "unit_price": 120.0,
        "delivery_days": 4,
    },
]