from boost_list import *
import unittest

class TestListMethods(unittest.TestCase):

    def test_sort_uniq(self):
        l1 = [1, 2, 3, 3, 3, 4, 4, 6]
        self.assertEqual(sort_uniq(l1), [1, 2, 3, 4, 6])

    def test_uniq(self):
        l1 = [1, 2, 3, 2, 4, 1, 4, 3]
        self.assertEqual(uniq(l1), [1, 2, 3, 4])

    def test_flatten(self):
        l1 = [[1, 2], [2, 4]]# gives : [1, 2, 2, 4]
        self.assertEqual(flatten(l1), [1, 2, 2, 4])
        l2 = [[1, [34, [3, 90, 4]]], [2, 4]]
        self.assertEqual(flatten(l2), [1, 34, 3, 90, 4, 2, 4])

    def test_successive_ints(self):
        l1 = [1, 2, 3, 4]
        self.assertEqual(successive_ints(l1), [[1, 2], [2, 3], [3, 4]])

    def test_occurrences(self):
        l1 = [11, 33, 11, 33, 3, 0, 5]
        d1 = occurrences(l1)
        d2 = {3:1, 33: 2, 11: 2, 0: 1, 5: 1}
        self.assertEqual(occurrences(l1), d2)

    def test_addition(self):
        l1 = addition_table(6)

    def test_switch(self):
        l1 = [11, 33, 11, 33, 3, 0, 5]
        d1 = {"Marie":"3", "Bidule":"4"}
        d2 = {'3': "Marie", '4': "Bidule"}
        self.assertEqual(switch(d1), d2)

    def test_same_elements(self):
        l1 = [1, 1, 2, 4, 5, 4, 3]
        l2 = [5, 1, 2, 3, 4, 1, 1, 2]
        self.assertTrue(same_elements(l1, l2))
        l3 = [1, 1, 2, 4, 5, 4, 6]
        l4 = [5, 1, 2, 3, 4, 1, 1, 2]
        self.assertFalse(same_elements(l3, l4))

    def test_is_anagram(self):
        l1 = "azerty"
        l2 = "ytreza"
        self.assertTrue(is_anagram(l1, l2))
        l1 = "azerty"
        l2 = "ytrezay"
        self.assertFalse(is_anagram(l1, l2))


# def test_mystery_number():
#     mystery_number(10)

# def test_dice_game():
#     dice_game(50)

if  __name__ == '__main__':
    unittest.main()

