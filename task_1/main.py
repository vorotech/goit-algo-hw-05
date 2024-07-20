"""Module containing the implementation of the HashTable class."""

class HashTable:
    """Class representing a hash table."""
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def hash_function(self, key):
        """Hash function that returns the index of the key."""
        return hash(key) % self.size

    def insert(self, key, value):
        """Inserts a key-value pair into the hash table."""
        key_hash = self.hash_function(key)
        key_value = [key, value]

        if self.table[key_hash] is None:
            self.table[key_hash] = list([key_value])
            return True
        else:
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    pair[1] = value
                    return True
            self.table[key_hash].append(key_value)
            return True

    def get(self, key):
        """Returns the value of the key."""
        key_hash = self.hash_function(key)
        if self.table[key_hash] is not None:
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    return pair[1]
        return None

    def delete(self, key):
        """Deletes the key-value pair from the hash table."""
        key_hash = self.hash_function(key)
        if self.table[key_hash] is not None:
            for i in range(len(self.table[key_hash])):
                if self.table[key_hash][i][0] == key:
                    self.table[key_hash].pop(i)
                    return True
        return False

def main():
    """Main function."""

    H = HashTable(5)
    H.insert("apple", 10)
    H.insert("orange", 20)
    H.insert("banana", 30)

    print(H.get("apple"))   # Виведе: 10
    print(H.get("orange"))  # Виведе: 20
    print(H.get("banana"))  # Виведе: 30

    H.delete("orange")
    print(H.get("orange"))  # Виведе: None

if __name__ == "__main__":
    main()
