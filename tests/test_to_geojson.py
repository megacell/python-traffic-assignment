__author__ = "Jerome Thai"
__email__ = "jerome.thai@berkeley.edu"

import unittest
from visualization.to_geojson import geojson_link
import numpy as np
from process_data import process_links


class TestToGeojson(unittest.TestCase):

    def test_geojson_link(self):
        # links = np.array([[34.1424478,-118.227151,34.143128,-118.2268528,80.3,3.6],
        #     [34.149884,-118.2327192,34.1504116,-118.2336735,105.6,4.7],
        #     [34.1496437,-118.2322303,34.1498846,-118.2327192,52.4,2.3]])
        # geojson_link(links, ['length', 'fftt'])
        pass


if __name__ == '__main__':
    unittest.main()