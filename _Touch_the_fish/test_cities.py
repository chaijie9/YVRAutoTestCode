import unittest

from Touch_the_fish.city_functions import get_city_formatted


class CityTestCase(unittest.TestCase):
    def test_cityA(self):
        get_cityA = get_city_formatted("Santiago", "Chile")
        self.assertEqual(get_cityA, "Santiago Chile")

    def test_cityB(self):
        get_cityB = get_city_formatted("Santiago", "Chile", "5000")
        self.assertEqual(get_cityB, "Santiago Chile Population=5000")


if __name__ == '__main__':
    unittest.main()

