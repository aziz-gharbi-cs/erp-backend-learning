from sqlalchemy import select
from sqlalchemy.orm import Session

from models.invoice import Invoice


class InvoiceRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, invoice: Invoice) -> None:
        self.session.add(invoice)
        self.session.flush()

    def get_all(self) -> list[Invoice]:
        stmt = select(Invoice)
        return list(self.session.scalars(stmt))

    def get_by_id(self, invoice_id: int) -> Invoice | None:
        stmt = select(Invoice).where(Invoice.id == invoice_id)
        return self.session.scalar(stmt)

    def update(self, invoice: Invoice) -> None:
        self.session.merge(invoice)
        self.session.flush()

    def delete(self, invoice: Invoice) -> None:
        self.session.delete(invoice)
        self.session.flush()