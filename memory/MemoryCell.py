class MemoryCell:
    def __init__(self, access_count):
        self.left_access_count = 0
        self.right_access_count = 0
        self.adjacent_access_count = 0

        self.access_count = access_count
        self.did_flip = False

        self.flip_count = 0
        self.refresh_count = 0

    def get_access_count(self):
        return self.access_count

    def get_adjacent_access_count(self):
        return self.adjacent_access_count

    def access(self):
        self.access_count += 1

    def flip(self):
        self.did_flip = True
        self.flip_count += 1

    def refresh(self):
        self.did_flip = False
        self.refresh_count += 1

    def increment_left_adjacent_access_count(self):
        self.left_access_count += 1
        self.adjacent_access_count += 1

    def increment_right_adjacent_access_count(self):
        self.right_access_count += 1
        self.adjacent_access_count += 1

    def reset_adjacent_counts(self):
        self.left_access_count = 0
        self.right_access_count = 0

    def reset_left_adjacent_access_count(self):
        self.left_access_count = 0

    def reset_right_adjacent_access_count(self):
        self.right_access_count = 0
