import unittest
from unittest.mock import patch
from display_images import get_event
import config
import os

class TestGettingEvent(unittest.TestCase):
    
    @patch("display_images.input")
    def test_get_event(self, mocked_input):
        # Test cases where input is an event (wrong event name and correct event name)
        event = config.DB["Event"][0]
        mocked_input.side_effect = ["not_event", event]
        self.assertEqual(get_event(), os.path.join(config.images_path, event))
        
        # Test cases where input is empty event
        mocked_input.side_effect = [""]
        self.assertEqual(get_event(), os.path.join(config.images_path, ""))       
        
        # Test the case where input is "quit"
        mocked_input.side_effect = ["Q", "some_wrong_input", "Quit"]
        self.assertRaises(SystemExit, get_event)
        self.assertRaises(SystemExit, get_event)