class Note:
    id_note: int
    id_category: int 
    description: str
    
    def __init__(self, id_category: int, description: str) -> None:
        self.id_category = id_category
        self.description = description