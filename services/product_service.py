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

                if not reference:
                    print("Reference cannot be empty.")
                    continue

                if repo.get_by_reference(reference):
                    print("Reference already exists.")
                    continue

                break

            name = input("Product Name (optional): ").strip() or None
            description = input("Description (optional): ").strip() or None

            while True:
                price_input = input("Unit Price (Excl. Tax): ").strip()

                try:
                    unit_price_excl_tax = Decimal(price_input)

                    if unit_price_excl_tax >= 0:
                        break

                    print("Price cannot be negative.")

                except InvalidOperation:
                    print("Invalid price.")

            while True:
                tax_input = input("Tax Rate (%): ").strip()

                try:
                    tax_rate = Decimal(tax_input)

                    if tax_rate >= 0:
                        break

                    print("Tax rate cannot be negative.")

                except InvalidOperation:
                    print("Invalid tax rate.")

            while True:
                try:
                    stock_quantity = int(input("Stock Quantity: "))

                    if stock_quantity >= 0:
                        break

                    print("Stock quantity cannot be negative.")

                except ValueError:
                    print("Invalid stock quantity.")

            product = Product(
                reference=reference,
                name=name,
                description=description,
                unit_price_excl_tax=unit_price_excl_tax,
                tax_rate=tax_rate,
                stock_quantity=stock_quantity,
            )

            repo.save(product)

            session.commit()

            print("Product created successfully.")

            return product

        except IntegrityError:
            session.rollback()
            print("Error: A product with this reference already exists.")

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