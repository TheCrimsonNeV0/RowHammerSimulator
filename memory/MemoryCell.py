class MemoryCell:
    def __init__(self, access_count=0):
        self.left_access_count = 0
        self.right_access_count = 0
        self.adjacent_access_count = 0

        self.left_blast_radius_impacts = []
        self.right_blast_radius_impacts = []

        self.access_count = access_count
        self.did_flip = False

        self.refresh_count = 0

    def get_access_count(self):
        return self.access_count

    def get_adjacent_access_count(self):
        return self.adjacent_access_count

    def access(self):
        self.access_count += 1

    def flip(self):
        self.did_flip = True

    def refresh(self):
        self.reset_adjacent_access_counts()
        self.refresh_count += 1

    def increment_left_adjacent_access_count(self):
        self.left_access_count += 1
        self.adjacent_access_count += 1

    def increment_right_adjacent_access_count(self):
        self.right_access_count += 1
        self.adjacent_access_count += 1

    def increment_left_blast_radius_impact(self, index):
        if len(self.left_blast_radius_impacts) <= index:
            self.left_blast_radius_impacts.extend([0] * (index + 1 - len(self.left_blast_radius_impacts)))
        self.left_blast_radius_impacts[index] += 1

    def increment_right_blast_radius_impact(self, index):
        if len(self.right_blast_radius_impacts) <= index:
            self.right_blast_radius_impacts.extend([0] * (index + 1 - len(self.right_blast_radius_impacts)))
        self.right_blast_radius_impacts[index] += 1

    def get_left_blast_radius_impacts(self):
        return self.left_blast_radius_impacts

    def get_right_blast_radius_impacts(self):
        return self.right_blast_radius_impacts

    def reset_adjacent_access_counts(self):
        self.left_access_count = 0
        self.right_access_count = 0

    def reset_left_adjacent_access_count(self):
        self.left_access_count = 0

    def reset_right_adjacent_access_count(self):
        self.right_access_count = 0
