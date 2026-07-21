from sqlalchemy import select
from sqlalchemy.orm import Session

from models.product import Product


class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, product: Product) -> None:
        self.session.add(product)
        self.session.flush()

    def get_all(self) -> list[Product]:
        stmt = select(Product)
        return list(self.session.scalars(stmt))

    def get_by_id(self, product_id: int) -> Product | None:
        stmt = select(Product).where(Product.id == product_id)
        return self.session.scalar(stmt)

    def get_by_reference(self, reference: str) -> Product | None:
        stmt = select(Product).where(Product.reference == reference)
        return self.session.scalar(stmt)

    def update(self, product: Product) -> None:
        self.session.merge(product)
        self.session.flush()

    def delete(self, product: Product) -> None:
        self.session.delete(product)
        self.session.flush()