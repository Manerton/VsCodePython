from pydantic import BaseModel

class CategoryPostDTO(BaseModel):
    name: str
    
class CategoryDTO(CategoryPostDTO):
    id: int
    
class CategoryRelationship(CategoryDTO):
    notes: list["NoteDto"]