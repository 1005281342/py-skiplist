from math import log

try:
    from numpy.random import geometric
except ImportError:
    import random

    def geometric(p):
        n = 1
        while random.randint(1, int(1 / p)) == 1:
            n += 1
        return n


class NIL(object):
    """Sentinel object that always compares greater than another object"""
    __slots__ = ()

    def __cmp__(self, other):
        return 1

    def __str__(self):
        return 'NIL'


class _Skipnode(object):
    __slots__ = ('data', 'next')

    def __init__(self, data, nxt):
        self.data = data
        self.next = nxt


nil = _Skipnode(NIL(), [])


class Skiplist(object):
    """Class for randomized indexed skip list. The default
    distribution of node heights is geometric."""

    def __init__(self, p=0.5, distribution=geometric):

        self._p = p
        self._max_levels = 1
        self._size = 0
        self.head = _Skipnode('HEAD', [nil] * self._max_levels)
        self.distribution = distribution

    def __len__(self):
        return self._size

    def __str__(self):
        return 'skiplist({})'.format([node.data for node in self])

    def __getitem__(self, data):
        '''Returns item with given index'''
        return self.find(data)

    def __iter__(self):
        'Iterate over values in sorted order'
        node = self.head.next[0]
        while node is not nil:
            yield node  # .data
            node = node.next[0]

    def _find_update(self, data):
        update = [None] * self._max_levels
        node = self.head
        for level in reversed(range(self._max_levels)):
            while node.next[level].data < data:
                node = node.next[level]
            update[level] = node
        return update

    def find(self, data):
        """Find node with given data"""
        n = len(self)
        l = int(log(1.0 / self._p, n)) if self._size >= 16 else self._max_levels
        node = self.head
        for level in reversed(range(l)):
            while node.next[level].data <= data:
                if data == node.next[level].data:
                    return node.next[level].data
                node = node.next[level]
        raise KeyError('Not found')

    def insert(self, data):
        """Inserts data into appropriate position."""

        # find position to insert
        update = self._find_update(data)
        node_height = self.distribution(self._p)
        new_node = _Skipnode(data, [None] * node_height)

        #if node's height is greater than number of levels
        #then add new levels, if not do nothing
        for level in range(self._max_levels, node_height):
            update.append(self.head)
            self.head.next.append(nil)

        #insert node to each level <= node's height after
        #corresponding node in 'update' list
        for level in range(node_height):
            prev_node = update[level]
            new_node.next[level] = prev_node.next[level]
            prev_node.next[level] = new_node
        self._size += 1
        self._max_levels = max(self._max_levels, node_height)

    def remove(self, data):
        """Removes node with given data. Raises KeyError if data is not in list."""

        update = self._find_update(data)
        if data != update[0].next[0].data:
            raise KeyError('Not found')

        node = update[0].next[0]
        node_height = len(node.next)
        for level in range(node_height):
            prevnode = update[level]
            prevnode.next[level] = prevnode.next[level].next[level]

        while self._max_levels > 1 and self.head.next[level] == nil:
            self._max_levels -= 1
        del node
        self._size -= 1

