import time

class Finder(object):

    def __init__(self, list_of_tuples):
        self.tuples = {x: True for x in list_of_tuples}
        self.tuple_list = list_of_tuples
        self.removed = set([])

    def size(self):
        return len(self.tuples)

    def distance(self, x, y):
        diffs = []
        for i in xrange(len(x)):
            diffs.append(x[i] - y[i])
        return sum(map(lambda x: x * x, diffs))

    def find_nearest(self, query):
        threshold = 20
        min = 100000000
        argmin = None
        for tuple in self.tuple_list:
            distance = self.distance(tuple, query)
            if distance < threshold and tuple not in self.removed:
                return self.remove(tuple)
            if distance < min:
                min = distance
                argmin = tuple

        self.used_bruteforce += 1
        return self.remove(argmin)

    def remove(self, element):
        del self.tuples[element]
        self.removed.add(element)
        return element

if __name__ == '__main__':
    tuples = [
        (1, 2, 3),
        (2, 2, 3),
        (3, 2, 3),
        (100, 2, 3),
        (400, 400, 400)]

    f = Finder(tuples)
    print f.find_nearest((0, 0, 0)) == (1, 2, 3)
    print f.find_nearest((0, 0, 0)) == (2, 2, 3)
    print f.find_nearest((100, 1000, 0)) == (400, 400, 400)
