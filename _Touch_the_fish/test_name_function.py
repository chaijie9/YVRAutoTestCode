import unittest

from Touch_the_fish.name_function import get_formatted


class NameTestCase(unittest.TestCase):
    """ 测试name_function.py """

    def test_first_last_name(self):
        """ 能够正确的处理 Janis Joplin 这样的姓名吗？"""
        formatted_name = get_formatted("janis", "joplin")
        self.assertEqual(formatted_name, "Janis Joplin")

    def test_first_last_middle_name(self):
        """能正确处理 Wolfgang Amadeus Mozart"""
        formatted_name = get_formatted("wolfgang", "mozart", "amadeus")
        self.assertEqual(formatted_name, "Wolfgang Amadeus Mozart")


if __name__ == '__main__':
    unittest.main()

