class Note:
    id_note: str
    id_category: str 
    description: str
    
    def __init__(self, id_category: str, description: str) -> None:
        self.id_category = id_category
        self.description = description