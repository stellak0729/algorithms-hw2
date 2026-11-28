import unittest

from src.shortener import URLShortener


class URLShortenerTests(unittest.TestCase):
    def setUp(self):
        self.shortener = URLShortener()

    def test_new_urls_use_incrementing_base62_ids_and_can_be_expanded(self):
        first_url = "https://example.com/first"
        second_url = "http://example.org/second"

        first_code = self.shortener.shorten(first_url)
        second_code = self.shortener.shorten(second_url)

        self.assertEqual(first_code, "0")
        self.assertEqual(second_code, "1")
        self.assertEqual(self.shortener.expand(first_code), first_url)
        self.assertEqual(self.shortener.expand(second_code), second_url)

    def test_repeated_url_reuses_code_and_preserves_original_url(self):
        url = "https://example.com/a%2Fb?query=one#section"

        code = self.shortener.shorten(url)

        self.assertEqual(self.shortener.shorten(url), code)
        self.assertEqual(self.shortener.expand(code), url)

    def test_http_and_https_urls_are_accepted(self):
        self.assertEqual(
            self.shortener.expand(self.shortener.shorten("http://example.com")),
            "http://example.com",
        )
        self.assertEqual(
            self.shortener.expand(self.shortener.shorten("https://example.com")),
            "https://example.com",
        )

    def test_invalid_urls_are_rejected(self):
        invalid_urls = [
            "",
            "   ",
            "/relative/path",
            "ftp://example.com/file",
            "http:///missing-host",
            "https://",
            "x" * 2049,
        ]
        for url in invalid_urls:
            with self.subTest(url=url):
                with self.assertRaises((TypeError, ValueError)):
                    self.shortener.shorten(url)

    def test_maximum_length_url_is_accepted_and_unknown_code_is_missing(self):
        url = "https://example.com/" + ("a" * (2048 - len("https://example.com/")))

        code = self.shortener.shorten(url)

        self.assertEqual(len(url), 2048)
        self.assertEqual(self.shortener.expand(code), url)
        self.assertIsNone(self.shortener.expand("ZZZZ"))


if __name__ == "__main__":
    unittest.main()
