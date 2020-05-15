from copy import copy

class MyArray(list):

    def add(self, x):
        self.append(x)

    def remove(self, i):
        self.pop(i)

    def get(self, i):
        return self[i]
    
    def clone(self):
        return copy(self)