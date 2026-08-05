from decimal import Decimal

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models.product import Product
from repositories.product_repository import ProductRepository


class ProductService:

    def __init__(self, session: Session):
        self.session = session
        self.repo = ProductRepository(session)

    def create_product(
        self,
        reference: str,
        name: str | None,
        description: str | None,
        unit_price_excl_tax: Decimal,
        tax_rate: Decimal,
        stock_quantity: int,
    ) -> Product:

        if self.repo.get_by_reference(reference):
            raise ValueError("Reference already exists.")

        if unit_price_excl_tax < 0:
            raise ValueError("Price cannot be negative.")

        if tax_rate < 0:
            raise ValueError("Tax rate cannot be negative.")

        if stock_quantity < 0:
            raise ValueError("Stock quantity cannot be negative.")

        product = Product(
            reference=reference,
            name=name,
            description=description,
            unit_price_excl_tax=unit_price_excl_tax,
            tax_rate=tax_rate,
            stock_quantity=stock_quantity,
        )

        try:
            self.repo.save(product)
            self.session.commit()
            return product

        except IntegrityError:
            self.session.rollback()
            raise

        except Exception:
            self.session.rollback()
            raise

    def list_products(self):
        return self.repo.get_all()

    def get_product(self, product_id: int) -> Product | None:
        return self.repo.get_by_id(product_id)

    def update_product(
        self,
        product_id: int,
        reference: str | None = None,
        name: str | None = None,
        description: str | None = None,
        unit_price_excl_tax: Decimal | None = None,
        tax_rate: Decimal | None = None,
        stock_quantity: int | None = None,
    ) -> Product:
        product = self.repo.get_by_id(product_id)
        if product is None:
            raise ValueError("Product not found.")

        if reference is not None:
            reference = reference.strip()
            if not reference:
                raise ValueError("Reference cannot be empty.")
            if reference != product.reference and self.repo.get_by_reference(reference):
                raise ValueError("Reference already exists.")
            product.reference = reference

        if name is not None:
            if not name.strip():
                raise ValueError("Name cannot be empty.")
            product.name = name.strip()

        if description is not None:
            product.description = description.strip() if description else None

        if unit_price_excl_tax is not None:
            if unit_price_excl_tax < 0:
                raise ValueError("Price cannot be negative.")
            product.unit_price_excl_tax = unit_price_excl_tax

        if tax_rate is not None:
            if tax_rate < 0:
                raise ValueError("Tax rate cannot be negative.")
            product.tax_rate = tax_rate

        if stock_quantity is not None:
            if stock_quantity < 0:
                raise ValueError("Stock quantity cannot be negative.")
            product.stock_quantity = stock_quantity

        try:
            self.repo.update(product)
            self.session.commit()
            return product
        except IntegrityError:
            self.session.rollback()
            raise
        except Exception:
            self.session.rollback()
            raise

    def delete_product(self, product_id: int) -> None:
        product = self.repo.get_by_id(product_id)
        if product is None:
            raise ValueError("Product not found.")

        try:
            self.repo.delete(product)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise