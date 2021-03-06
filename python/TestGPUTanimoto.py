import unittest
import sys
sys.path.append('/home/vancemiller/github/bigchem/experiments')
from compare import new_method, old_method
import numpy as np

from gpu_tanimoto_popcount import GPUtanimoto


class TestGPUTanimoto(unittest.TestCase):

    def test_zeros(self):
        query = np.array([[0]], np.uint64)
        target = np.array([[0]], np.uint64)
        output = GPUtanimoto(query, target)
        expect = [(0, 1.0)]
        self.assertEqual(output, expect)

    def test_ones(self):
        query = np.array([[1]], np.uint64)
        target = np.array([[1]], np.uint64)
        output = GPUtanimoto(query, target)
        expect = [(0, 1.0)]
        self.assertEqual(output, expect)

    def test_double(self):
        query = np.array([[0, 1]], np.uint64)
        target = np.array([[0, 1], [1, 0]], np.uint64)
        output = GPUtanimoto(query, target)
        expect = [(0, 1.0), (1, 0.0)]
        self.assertEqual(output, expect)

    def test_empty(self):
        query = np.empty(shape=(1, 1))
        target = np.empty(shape=(1, 2))
        output = GPUtanimoto(query, target)
        expect = np.empty(shape=(1, 1))
        self.assertTrue((output - expect).any()) 

    # compare the results between the old and the new method
    def test_compare(self):
        old_out = old_method(0, 500, 0, 500)
        new_out = new_method(0, 5000, 0, 5000)
        similarity_bound = 0.0001
        #sys.exit(0)
        #print "Comparing", len(old_out), "results"
        for i in range(len(old_out)):
            errors_exist = False
            count = 0
            if (abs(old_out[i] - new_out[i][1]) > similarity_bound):
                count = count + 1
            #endif
        #endfor
        #if count > 0:
            #print count, "errors"
        #endif
        self.assertEqual(count, 0)

    # compare the time to calculate using the old and new method
    def test_time(self):
        old_out = old_method(0, 5000, 0, 5000)
        new_out = new_method(0, 5000, 0, 5000)
        self.assertNotEqual(old_out, new_out)

if __name__ == '__main__':
    unittest.main()
