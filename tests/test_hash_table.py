import ast
import unittest
from pathlib import Path

from src.hash_table import HashTable


class HashTableTests(unittest.TestCase):
    @staticmethod
    def bucket_index(key, capacity):
        index = 0
        for character in key:
            index = (index * 31 + ord(character)) % capacity
        return index

    def test_missing_key_and_value_update(self):
        table = HashTable()

        self.assertIsNone(table.get("missing"))
        table.put("url", "first")
        table.put("url", "updated")

        self.assertEqual(table.get("url"), "updated")

    def test_colliding_keys_remain_retrievable(self):
        table = HashTable(initial_capacity=4)
        expected = {"first": "one", "second": "two"}
        capacity = table.capacity

        self.assertEqual(
            self.bucket_index("first", capacity),
            self.bucket_index("second", capacity),
        )

        for key, value in expected.items():
            table.put(key, value)

        for key, value in expected.items():
            with self.subTest(key=key):
                self.assertEqual(table.get(key), value)

    def test_resize_preserves_existing_entries(self):
        table = HashTable(initial_capacity=4)
        for index in range(3):
            table.put(f"key-{index}", f"value-{index}")

        original_capacity = table.capacity
        table.put("key-3", "value-3")

        self.assertGreater(table.capacity, original_capacity)
        for index in range(4):
            with self.subTest(index=index):
                self.assertEqual(table.get(f"key-{index}"), f"value-{index}")

    def test_hash_table_does_not_call_builtin_dict_set_or_hash(self):
        source_path = Path(__file__).resolve().parents[1] / "src" / "hash_table.py"
        tree = ast.parse(source_path.read_text(encoding="utf-8"))
        forbidden_calls = {
            node.func.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id in {"dict", "set", "hash"}
        }

        self.assertEqual(forbidden_calls, set())


if __name__ == "__main__":
    unittest.main()
