from comic import Comic


class Node:
    def __init__(self, data: Comic):
        self.data = data
        self.prev: Node | None = None
        self.next: Node | None = None

    def __str__(self):
        return str(self.data)
