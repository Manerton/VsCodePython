from DTO.note_dto import NotePostDto
from database.db import sync_session
from sqlalchemy import select, update, delete
from mytypes.note import NoteOrm
from DTO.note_dto import NoteDto

class NoteRepositoryOrm:
    @staticmethod
    # Возвращает все записи по конкретной категории
    def get_notes_by_category_id(category_id: int) -> list[NoteDto]:
        with sync_session() as session:
            query = select(NoteOrm).filter_by(category_id=category_id)
            res = session.execute(query)
            notes = res.scalars().all()
            notes_dto = [NoteDto.model_validate(row, from_attributes=True) for row in notes]
            return notes_dto
        
    @staticmethod
    # Возвращает контретную запись по id
    def get_note_by_id(note_id: int) -> NoteDto:
        with sync_session() as session:
            query = select(NoteOrm).filter_by(id=note_id)
            res = session.execute(query).one_or_none()
            note_dto = NoteDto.model_validate(res[0], from_attributes=True)
            return note_dto
        
    @staticmethod 
    # Возвращает контретную запись по id
    def insert_note(note: NotePostDto):
        now_note = NoteOrm(category_id=note.category_id, description=note.description)
        print(now_note.completed)
        with sync_session() as session:
            session.add(now_note)
            session.commit()
            
    @staticmethod
    # Обновление записи в таблице
    def update_note(new_note: NotePostDto, note_id: int):
        now_note = NoteOrm(category_id=new_note.category_id, description=new_note.description)
        with sync_session() as session:
            stmt = update(NoteOrm).values(now_note).filter_by(id=note_id)
            session.execute(stmt)
            session.commit()
    
    @staticmethod
    # Обновление статус в таблице 
    def update_completed_note(note_id: int, new_completed: bool):
        with sync_session() as session:
            print(new_completed)
            stmt = update(NoteOrm).values(completed=new_completed).filter_by(id=note_id)
            session.execute(stmt)
            session.commit()

    @staticmethod
    # Удаление записи из таблицы
    def delete_note(note_id: int):
        with sync_session() as session:
            stmt = delete(NoteOrm).filter_by(id=note_id)
            session.execute(stmt)
            session.commit()


