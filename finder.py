from scipy.spatial import KDTree
import time

class Finder(object):

    def __init__(self, list_of_tuples):
        self.tuples = {x: True for x in list_of_tuples}
        self.removed = set([])
        self.rebuild()

    def size(self):
        return len(self.tuples)

    def distance(self, x, y):
        diffs = []
        for i in xrange(len(x)):
            diffs.append(x[i] - y[i])
        return sum(map(lambda x: x * x, diffs))

    def find_threshold(self, query):
        thresh = 20
        for elem, _ in self.tuples.iteritems():
            if self.distance(query, elem) <= thresh:
                return self.remove(elem)

    def find_nearest(self, query):
        if len(self.removed) % 1234 == 0:
            self.rebuild_if_necessary()

        (_, idxes) = self.tree.query(query, 80)
        for idx in idxes:
            kdnearest = self.tuple_list[idx]
            if kdnearest not in self.removed:
                self.used_kd += 1
                return self.remove(kdnearest)

        min = 100000000
        argmin = None
        for k, _ in self.tuples.iteritems():
            distance = self.distance(k, query)
            if distance < min:
                min = distance
                argmin = k
        self.used_bruteforce += 1
        return self.remove(argmin)

    def remove(self, elem):
        del self.tuples[elem]
        self.removed.add(elem)
        return elem

    def rebuild_if_necessary(self):
        print ('kd, bruteforce', self.used_kd, self.used_bruteforce)
        if self.used_bruteforce > 2:
            start = time.time()
            self.rebuild()
            diff = time.time() - start
            print ('rebuilt in ', diff)

    def rebuild(self):
        self.tuple_list = self.tuples.keys()
        self.tree = KDTree(self.tuple_list)
        self.used_kd = 0
        self.used_bruteforce = 0

    def iterate(self):
        for k, _ in self.tuples.iteritems():
            yield k


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
