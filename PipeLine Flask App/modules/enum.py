import enum

class Size(enum.Enum):
    one = "Extra Small"
    two = "Small"
    three = "Medium"
    four = "Large"
    five = "Extra Large"

    @staticmethod
    def from_str(label):
        if label in ('Extra Small'):
            return Size.one
        elif label in ('Small'):
            return Size.two
        elif label in ('Medium'):
            return Size.three
        elif label in ('Large'):
            return Size.four
        elif label in ('Extra Large'):
            return Size.five
        else:
            raise NotImplementedError

class Status(enum.Enum):
    lost = "lost"
    found = "found"

    @staticmethod
    def from_str(label):
        if label in ('Small'):
            return Status.lost
        elif label in ('Small'):
            return Status.found
        else:
            raise NotImplementedError
