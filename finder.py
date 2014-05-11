from scipy.spatial import KDTree
class Finder(object):

    def __init__(self, list_of_tuples, distance):
        self.tree = KDTree(list_of_tuples)
        self.tuple_list = list_of_tuples
        self.tuples = {x: True for x in list_of_tuples}
        self.distance = distance
        self.removed = set([])

    def find_nearest(self, query):
        (_, idx) = self.tree.query(query)
        kdnearest = self.tuple_list[idx]

        if kdnearest not in self.removed:
            del self.tuples[kdnearest]
            self.removed.add(kdnearest)
            return

        min = 100000000
        argmin = None
        for k, _ in self.tuples.iteritems():
            distance = self.distance(k, query)
            if distance < min:
                min = distance
                argmin = k
        del self.tuples[argmin]
        self.removed.add(kdnearest)
        return argmin

if __name__ == '__main__':
    def dist(x, y):
        diffs = []
        for i in xrange(len(x)):
            diffs.append(x[i] - y[i])
        return sum(map(lambda x: x * x, diffs))
    tuples = [
        (1, 2, 3),
        (2, 2, 3),
        (3, 2, 3),
        (100, 2, 3),
        (400, 400, 400)]

    f = Finder(tuples, dist)
    print f.find_nearest((0, 0, 0)) == (1, 2, 3)
    print f.find_nearest((0, 0, 0)) == (2, 2, 3)
    print f.find_nearest((100, 1000, 0)) == (400, 400, 400)
