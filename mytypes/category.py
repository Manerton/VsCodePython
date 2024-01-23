from database.db import Base, id_pk, str_256
from sqlalchemy.orm import Mapped, relationship

class CategoryOrm(Base):
    __tablename__ = "categories"
    
    id: Mapped[id_pk]
    name: Mapped[str_256]
    
    notes: Mapped[list["NoteOrm"]] = relationship(
        back_populates="category"
    )
    
    def __init__(self, name: str) -> None:
        self.name = name
