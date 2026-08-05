from decimal import Decimal, InvalidOperation

from sqlalchemy.exc import IntegrityError

from database.database import SessionLocal
from models.product import Product
from repositories.product_repository import ProductRepository


def create_product():
    with SessionLocal() as session:
        repo = ProductRepository(session)

        try:
            while True:
                reference = input("Reference: ").strip()
                if reference:
                    break
                print("Reference cannot be empty.")

            while True:
                name = input("Product Name: ").strip()
                if name:
                    break
                print("Product name cannot be empty.")

            description = input("Description (optional): ").strip() or None

            while True:
                unit_price_input = input("Unit Price: ").strip()

                try:
                    unit_price = Decimal(unit_price_input)

                    if unit_price >= 0:
                        break

                    print("Unit price cannot be negative.")

                except InvalidOperation:
                    print("Invalid unit price.")

            while True:
                tax_rate_input = input("Tax Rate (optional, default 0): ").strip()

                if not tax_rate_input:
                    tax_rate = Decimal("0.00")
                    break

                try:
                    tax_rate = Decimal(tax_rate_input)

                    if tax_rate >= 0:
                        break

                    print("Tax rate cannot be negative.")

                except InvalidOperation:
                    print("Invalid tax rate.")

            while True:
                stock_input = input("Stock Quantity: ").strip()

                try:
                    stock_quantity = int(stock_input)

                    if stock_quantity >= 0:
                        break

                    print("Stock quantity cannot be negative.")

                except ValueError:
                    print("Invalid stock quantity.")

            product = Product(
                reference=reference,
                name=name,
                description=description,
                unit_price_excl_tax=unit_price,
                tax_rate=tax_rate,
                stock_quantity=stock_quantity,
            )

            repo.save(product)
            session.commit()

            print(product)
            return product

        except IntegrityError:
            session.rollback()
            print("Error: A product with the same unique information already exists.")

        except Exception:
            session.rollback()
            raise


def list_products():
    with SessionLocal() as session:
        repo = ProductRepository(session)
        products = repo.get_all()

    if not products:
        print("No products found.")
        return

    for product in products:
        print(product)