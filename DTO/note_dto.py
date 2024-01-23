from pydantic import BaseModel

class NotePostDto(BaseModel):
    description: str
    category_id: int
    
class NoteDto(NotePostDto):
    id: int
    completed: bool
    
class NoteRelationship(NoteDto):
    category: "CategoryDTO"