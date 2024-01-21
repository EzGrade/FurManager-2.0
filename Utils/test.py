import setup

setup.setup_django()
import unittest
from Utils.functions import Text


class TestStringMethods(unittest.TestCase):
    def test_furaffinity(self):
        self.assertEqual(Text.process_caption_links("https://www.furaffinity.net/view/53026822/"),
                         "[Furaffinity](https://www.furaffinity.net/view/53026822/)")

    def test_e621(self):
        self.assertEqual(Text.process_caption_links("https://e621.net/posts/2632337"),
                         "[e621](https://e621.net/posts/2632337)")

    def test_combined(self):
        self.assertEqual(
            Text.process_caption_links("https://www.furaffinity.net/view/53026822/\nhttps://e621.net/posts/2632337"),
            "[Furaffinity](https://www.furaffinity.net/view/53026822/)\n[e621](https://e621.net/posts/2632337)")

    def test_combined_with_text(self):
        self.assertEqual(Text.process_caption_links(
            "https://www.furaffinity.net/view/53026822/ - https://e621.net/posts/2632337\n1234"),
                         "[Furaffinity](https://www.furaffinity.net/view/53026822/) - [e621](https://e621.net/posts/2632337)\n1234")


if __name__ == '__main__':
    unittest.main()
