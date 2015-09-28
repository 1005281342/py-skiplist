import unittest

from skiplist import Skiplist, NIL
from iterators import LevelNodeIterator


class DataStructTestCase(unittest.TestCase):
    def test_nil_always_false(self):
        self.assertFalse(NIL())


class SkipListTestCase(unittest.TestCase):

    def test_insert(self):
        sl = Skiplist()
        sl.insert(1, 1)
        e = sl[1]
        self.assertEqual(e, 1)

    def test_update(self):
        sl = Skiplist()
        sl['foo'] = 'bar'
        self.assertEqual(sl['foo'], 'bar')
        sl['foo'] = 'baz'
        self.assertEqual(sl['foo'], 'baz')

    def test_remove(self):
        sl = Skiplist()
        sl['what'] = 'that'
        self.assertTrue(sl['what'])
        del sl['what']
        self.assertRaises(KeyError, lambda: sl['what'])
        self.assertRaises(KeyError, lambda: sl.remove('not here'))

    def test_init(self):
        sl = Skiplist(a=1, b=2)
        self.assertEqual(sl['a'], 1)
        self.assertEqual(sl['b'], 2)
        self.assertEqual(len(sl), 2)

    def test_str(self):
        sl = Skiplist()
        self.assertEqual('skiplist([])', str(sl))
        sl['1'] = 1
        self.assertEqual('skiplist([\'1\'])', str(sl))


class LevelIteratorTestCase(unittest.TestCase):
    def test_iterator_default(self):
        s = Skiplist(foo=1, bar=2)
        self.assertListEqual(sorted(['foo', 'bar']), sorted(node.key for node in LevelNodeIterator(s)))


if __name__ == '__main__':
    unittest.main()
