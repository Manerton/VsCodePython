# from database.db import execute_sql_command_without_res, execute_sql_command_with_res
from database.db import sync_session
from sqlalchemy import insert, update, delete, select
from mytypes.category import CategoryOrm
from DTO.category_dto import CategoryDTO
from DTO.category_dto import CategoryPostDTO


class CategoryRepositoryOrm:
    @staticmethod 
    # Возвращает все категории
    def get_all_categories():
        with sync_session() as session:
            query = select(CategoryOrm)
            res = session.execute(query)
            if res is None:
                return
            categories = res.scalars().all()
            categories_dto = [CategoryDTO.model_validate(row, from_attributes=True) for row in categories]
            return categories_dto
        
    @staticmethod
    # Возвращает контретную категорию по id
    def get_category_by_id(category_id: int) -> CategoryDTO:
        with sync_session() as session:
            query = select(CategoryOrm).filter_by(id=category_id)    
            res = session.execute(query).one_or_none()
            category = CategoryDTO.model_validate(res[0], from_attributes=True)
            return category
        
    @staticmethod
    # Возвращает контретную категорию по названию
    def get_category_by_name(category_name: str) -> CategoryDTO:
        with sync_session() as session:
            query = select(CategoryOrm).filter_by(name=category_name)
            res = session.execute(query).one_or_none()
            if res is None:
                return None
            category = CategoryDTO.model_validate(res[0], from_attributes=True)
            return category
        
    @staticmethod
    # Добавляет категорию в таблицу
    def insert_category(category: CategoryPostDTO):
        now_category = CategoryOrm(name=category.name)
        with sync_session() as session:
            session.add(now_category)
            session.commit()
            
    @staticmethod
    # Удаляет категорию из таблицы
    def delete_category(category_id: int):
        with sync_session() as session:
            query = delete(CategoryOrm).filter_by(id=category_id)
            session.execute(query)
            session.commit()
            