import sys, os, unittest

sys.path.append('/Users/talmadgefarringer/Desktop/digital-wallet-master/insight_testsuite/')

import test

previous_payments_dict = {1: [[4,5,6]], 4: [[1, 10]], 5: [[1]], 6:[[1]], 10: [[4,11,23]], 11:[[10]], 23:[[10,50]], 50:[[23, 60]], 60:[[50]]}


###### I should have put these in a different file and then imported them. Leaving them in for now

def first_degree(series1, series2):
    ### take the first user and see if the second user is in their value list in the dictionary
    if previous_payments_dict.get(series1, None) is not None:
        if series2 in previous_payments_dict.get(series1, None)[0]:
            return 1
    else:
        pass



def second_degree(series1, series2):
    #### check if they are first degree friends
    if first_degree(series1, series2) is not None:
        return first_degree(series1, series2)
    else:
        pass

    if previous_payments_dict.get(series1, None) is not None and previous_payments_dict.get(series2, None) is not None:
        for x, y in [(x, y) for x in previous_payments_dict.get(series1, None)[0] for y in
                     previous_payments_dict.get(series2, None)]:
            if x in y or series2 == x or series1 in y:
                return 1
            else:
                pass
    else:
        pass

def fourth_degree(series1, series2):
    #### here we check to see if the children of 1 equal series2
    if previous_payments_dict.get(series1, None) is not None and previous_payments_dict.get(series2, None) is not None:
        if first_degree(series1, series2) is not None:
            return first_degree(series1, series2)
        else:
            pass

    ##### here we compare the children of 1 to the children of 2
    if previous_payments_dict.get(series1, None) is not None and previous_payments_dict.get(series2, None) is not None:
        for x, y in [(x, y) for x in previous_payments_dict.get(series1, None)[0] for y in
                     previous_payments_dict.get(series2, None)]:
            if x in y or series2 == x or series1 in y:
                return 1
            else:
                pass
    else:
        pass

    ##### for each child from #1, compare it's children to the children from of 2
    ####### this is 3rd degree
    if previous_payments_dict.get(series1, None) is not None and previous_payments_dict.get(series2, None) is not None:
        for x in previous_payments_dict.get(series1, None)[0]:
            for b, c in [(b, c) for b in previous_payments_dict.get(x, None)[0] for c in
                         previous_payments_dict.get(series2, None)]:
                if b in c or series2 == b or series1 in c:
                    return 1

            ##### for each grand-child from #1, compare it's children to the children from of 2
            for e in previous_payments_dict.get(x, None)[0]:
                if e != series1:
                    for f, g in [(f, g) for f in previous_payments_dict.get(e, None)[0] for g in
                                 previous_payments_dict.get(series2, None)]:
                        if f in g or series2 == f or series1 in g:
                            return 1




class TestStringMethods(unittest.TestCase):

    def test_dict(self):
        self.assertEqual(previous_payments_dict.get(1, None)[0], [4,5,6])

    def test_first_deg(self):
        self.assertEqual(first_degree(1, 4), 1)
        self.assertEqual(first_degree(1, 10), None)

    def test_second_deg(self):
        self.assertEqual(second_degree(1, 10), 1)
        self.assertEqual(second_degree(1, 5), 1)
        self.assertEqual(second_degree(1, 23), None)

    def test_fourth_deg(self):
        self.assertEqual(fourth_degree(1, 50), 1)
        self.assertEqual(fourth_degree(1, 5), 1)
        self.assertEqual(fourth_degree(1, 60), None)


if __name__ == '__main__':
    unittest.main()

