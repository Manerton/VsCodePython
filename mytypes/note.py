from database.db import Base, id_pk, str_256
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

class NoteOrm(Base):
    __tablename__ = "notes"
    
    id: Mapped[id_pk]
    description: Mapped[str_256]
    completed: Mapped[bool]
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE")
    )
    
    category: Mapped["CategoryOrm"] = relationship(
        back_populates="notes"
    )
    
    def __init__(self, category_id: int, description: str) -> None:
        self.category_id = category_id
        self.description = description
        self.completed = False
