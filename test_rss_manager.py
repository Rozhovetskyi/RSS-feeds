import unittest
import os
import xml.etree.ElementTree as ET
from rss_manager import add_item, create_initial_feed, get_feed_path, ensure_feeds_dir

class TestRSSManager(unittest.TestCase):
    def setUp(self):
        self.test_topic = "UnitTestTopic"
        ensure_feeds_dir()

    def tearDown(self):
        path = get_feed_path(self.test_topic)
        if os.path.exists(path):
            os.remove(path)

    def test_create_and_add(self):
        tree = create_initial_feed(self.test_topic)
        add_item(tree, "Title 1", "http://link1", "Summary 1")

        root = tree.getroot()
        items = root.findall("./channel/item")
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].find("title").text, "Title 1")

    def test_deduplication(self):
        tree = create_initial_feed(self.test_topic)
        add_item(tree, "Title 1", "http://link1", "Summary 1")
        add_item(tree, "Title 2", "http://link1", "Summary 2") # Duplicate link

        root = tree.getroot()
        items = root.findall("./channel/item")
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].find("title").text, "Title 1")

    def test_limit(self):
        tree = create_initial_feed(self.test_topic)
        for i in range(10):
            add_item(tree, f"Title {i}", f"http://link{i}", f"Summary {i}")

        root = tree.getroot()
        items = root.findall("./channel/item")
        self.assertEqual(len(items), 7)
        # The last added item (Title 9) should be at the top
        self.assertEqual(items[0].find("title").text, "Title 9")

if __name__ == '__main__':
    unittest.main()
