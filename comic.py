class Comic:
    def __init__(self, id: int, title: str, image: str, date: str, isbn: str, description: str, characters: list, creators: list):
        self.id = id
        self.title = title
        self.image = image
        self.date = date
        self.isbn = isbn
        self.description = description
        self.characters = characters
        self.creators = creators

