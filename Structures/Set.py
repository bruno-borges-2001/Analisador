class Set:

    def __init__(self, values: list = []):
        self.values = values.copy()
        self.size = len(self.values)

    def intersection(self, other):
        return [x for x in self.values if x in other.values]

    def sin(self, value):
        return value in self.values

    def index(self, value):
        return self.values.index(value)

    def append(self, value):
        if value not in self.values:
            self.values.append(value)
            self.size += 1

    def pop(self, index=0):
        self.size -= 1
        return self.values.pop(index)

    def copy(self):
        return Set(self.values.copy())

    def remove(self, value):
        if value in self.values:
            self.size -= 1
            return self.values.remove(value)
        else:
            raise Exception("Value is not in the set")

    def __add__(self, other):
        new_list = self.values.copy()
        for i in other.values:
            if i not in new_list:
                new_list.append(i)
        return Set(new_list)

    def __sub__(self, other):
        return Set([x for x in self.values if x not in other.values])

    def __str__(self):
        return str(self.values)

    def __iter__(self):
        return iter(self.values)

    def __eq__(self, other):
        try:
            self_aux = self.values.copy()
            other_aux = other.values.copy()

            for i in self.values:
                self_aux.remove(i)
                other_aux.remove(i)

            if len(self_aux) > 0 or len(other_aux) > 0:
                return False

            return True
        except:
            return False
