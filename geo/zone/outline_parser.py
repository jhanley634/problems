# Copyright 2023 John Hanley. MIT licensed.
class OutlineParser:
    def __init__(self, lines):
        self.lines = lines

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self.lines.pop(0)
        except IndexError:
            raise StopIteration
