class MemoryCell:
    def __init__(self, access_count):
        self.access_count = access_count
        self.did_flip = False

    def get_access_count(self):
        return self.access_count

    def access(self):
        self.access_count += 1

    def flip(self):
        self.did_flip = True

    def refresh(self):
        self.did_flip = False
