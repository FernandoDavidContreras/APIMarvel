from node import Node
from comic import Comic


class Lista:
    def __init__(self, limit: int | None = None):
        self.size = 0
        self.max = limit
        self.head: Node | None = None
        self.tail: Node | None = None

    def __getitem__(self, index):
        current = self.head
        count = 0

        while current is not None:
            if count == index:
                return current.data
            else:
                current = current.next
                count += 1

        raise IndexError("Index out of range")

    def preprend(self, data):
        new_node = Node(data)
        new_node.next = self.head
        new_node.prev = self.tail
        if self.tail:
            self.tail.next = new_node
        self.head = new_node
        if self.tail is None:
            self.tail = new_node
        self.size += 1

    def append(self, data):
        if self.is_empty():
            self.preprend(data)
        else:
            new_node = Node(data)
            new_node.prev = self.tail
            new_node.next = self.head
            self.tail.next = new_node
            self.tail = new_node
            self.head.prev = self.tail
            self.size += 1

    def is_empty(self):
        return self.head is None

    def transversal(self):
        if self.is_empty():
            return "Lista vacía"
        current = self.head
        result = ""
        while current is not None:
            result += str(current)
            current = current.next
            if current is not self.head:
                result += " --> "
        return result

    def shift(self):
        if self.head is None:
            raise Exception("Subdesvordamiento de pila")
        else:
            current = self.head
            self.head = current.next
            self.head.prev = self.tail
            self.tail.next = self.head
            current.next = None
            current.prev = None
            self.size -= 1
            return current.data

    def pop(self):
        if self.tail is None:
            raise Exception("Subdesbordamiento de lista")
        elif self.head is self.tail:
            return self.shift()
        else:
            current = self.tail
            self.tail = current.prev
            self.tail.next = self.head
            self.head.prev = self.tail
            current.prev = None
            current.next = None
            self.size -= 1
            return current.data

    def search_by_ID_comic(self, data: int):
        current = self.head
        while current is not None:
            if isinstance(current.data, Comic) and current.data.id == data:
                return current
            else:
                current = current.next
                if current is self.head:
                    return None
        return None

    def search_by_position(self, data: int):
        current = self.head
        current_data = 0
        while current is not None:
            if current_data == data:
                return current
            else:
                current = current.next
                current_data += 1
                if current is self.head:
                    return None
        return None

    def search_by_node_position(self, ref: Node):
        current = self.head
        current_data = 0
        while current is not None:
            if current == ref:
                return current_data
            else:
                current = current.next
                current_data += 1
                if current is self.head:
                    return None
        return None

    def deleate_by_ID_comic(self, data: int):
        current = self.head
        while current is not None:
            if isinstance(current.data, Comic) and current.data.id == data:
                if current is self.head:
                    return self.shift()
                elif current is self.tail:
                    return self.pop()
                else:
                    current.prev.next = current.next
                    current.next.prev = current.prev
                    current.next = None
                    current.prev = None
                    self.size -= 1
                    return current.data
            else:
                current = current.next
                if current is self.head:
                    return None
        return None

    def __str__(self):
        return self.transversal()

