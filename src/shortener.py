"""In-memory URL shortening and expansion."""

from urllib.parse import urlsplit

from src.base62 import decode, encode
from src.hash_table import HashTable


class URLShortener:
    def __init__(self):
        self._url_to_code = HashTable()
        self._code_to_url = HashTable()
        self._next_id = 0

    def shorten(self, url: str) -> str:
        self._validate_url(url)

        existing_code = self._url_to_code.get(url)
        if existing_code is not None:
            return existing_code

        code = encode(self._next_id)
        self._url_to_code.put(url, code)
        self._code_to_url.put(code, url)
        self._next_id += 1
        return code

    def expand(self, code: str) -> str | None:
        decode(code)
        return self._code_to_url.get(code)

    @staticmethod
    def _validate_url(url: str) -> None:
        if not isinstance(url, str):
            raise TypeError("url must be a string")
        if not url or not url.strip():
            raise ValueError("url must not be empty")
        if len(url) > 2048:
            raise ValueError("url must not exceed 2048 characters")

        try:
            parsed = urlsplit(url)
            hostname = parsed.hostname
            _ = parsed.port
        except ValueError as error:
            raise ValueError("url must be an absolute HTTP or HTTPS URL") from error

        if parsed.scheme.lower() not in ("http", "https") or not hostname:
            raise ValueError("url must be an absolute HTTP or HTTPS URL with a host")
        if any(character.isspace() for character in hostname):
            raise ValueError("url must contain a valid host")
