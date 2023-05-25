from organise_images import *
import unittest
from unittest.mock import patch
from organise_images import change_info

class TestExtractMetadata(unittest.TestCase):
    def test_get_coordinates(self):
        self.assertEqual(get_coords("Bern"), (46.9484742, 7.4521749, "Bern"), "Coordinates don't match") # city
        self.assertEqual(get_coords("Japan"), (36.5748441, 139.2394179, "Japan"), "Coordinates don't match") # country
        self.assertEqual(get_coords("Hochschulstrasse 4, Bern"), (46.9503097, 7.4382509, 'Hochschulstrasse 4, Bern'), "Coordinates don't match")  # street
        self.assertEqual(get_coords("1"), None, "Coordinates don't match") # wrong imput

class TestChangeInfo(unittest.TestCase):
    @patch("organise_images.input")
    def test_change_info(self, mocked_input):
        # Test the case where input is "q" or "quit"
        mocked_input.side_effect = ["Q", "Quit"]
        self.assertRaises(SystemExit, change_info)
        self.assertRaises(SystemExit, change_info)

