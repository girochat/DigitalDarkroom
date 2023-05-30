import unittest
from unittest.mock import patch
from display_images import get_event
import config
import os

class TestGettingEvent(unittest.TestCase):
    
    @patch("display_images.input")
    def test_get_event(self, mocked_input):
        # Test cases where input is "yes" (wrong event name and correct event name)
        event = config.DB["Event"][0]
        mocked_input.side_effect = ["Y", "not_event", "Y", event]
        self.assertEqual(get_event(), os.path.join(config.images_path, event))
        
        # Test the case where input is "no"
        mocked_input.side_effect = ["N"]
        self.assertEqual(get_event(), config.images_path)
        
        # Test the case where input is "quit"
        mocked_input.side_effect = ["Q", "some_wrong_input", "Quit"]
        self.assertRaises(SystemExit, get_event)
        self.assertRaises(SystemExit, get_event)