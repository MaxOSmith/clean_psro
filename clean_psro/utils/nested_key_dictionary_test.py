from typing import Any, List, Sequence, Tuple

from absl.testing import absltest, parameterized

from clean_psro.utils.nested_key_dictionary import NestedKeyDictionary

_Keys = List[Any]
_Value = Any
_KeysValue = Tuple[_Keys, _Value]


class NestedKeyDictionaryTest(parameterized.TestCase):
    """Test suite for `NestedKeyDictionary`."""

    @parameterized.named_parameters(
        [
            {
                "testcase_name": "set_get",
                "writes": [
                    (["a"], 1),
                ],
                "reads": [
                    (["a"], 1),
                ],
            },
            {
                "testcase_name": "nested_set_get",
                "writes": [
                    (["a", "b"], 1),
                    (["a", "d"], 3),
                    (["c"], 2),
                    (["a", "d"], 4),
                ],
                "reads": [
                    (["a", "b"], 1),
                    (["c"], 2),
                    (["a", "d"], 4),
                    (["a", "b"], 1),
                    (["c"], 2),
                    (["a", "d"], 4),
                ],
            },
            {
                "testcase_name": "mixed_types",
                "writes": [([1, 2], 3), ([1, "a"], 5), (["b"], 10), (["c", 1, "d"], 42)],
                "reads": [
                    (["c", 1, "d"], 42),
                    ([1, "a"], 5),
                    (["b"], 10),
                    ([1, 2], 3),
                ],
            },
        ]
    )
    def test_set(self, writes: Sequence[_KeysValue], reads: Sequence[_KeysValue]):
        """Tests adding data into the dictionary.

        Args:
                writes: Writes into the dictionary.
                reads: Reads to test after all writes complete.
        """
        container = NestedKeyDictionary()
        for keys, value in writes:
            container.set(keys, value)
        for keys, value in reads:
            self.assertEqual(value, container.get(keys))

    @parameterized.named_parameters(
        [
            {
                "testcase_name": "set_pop",
                "writes": [
                    (["a"], 1),
                ],
                "pops": [
                    (["a"], 1),
                ],
            },
            {
                "testcase_name": "nested_set_pop",
                "writes": [
                    (["a", "b"], 1),
                    (["a", "d"], 3),
                    (["c"], 2),
                    (["a", "d"], 4),
                ],
                "pops": [
                    (["a", "b"], 1),
                    (["c"], 2),
                    (["a", "d"], 4),
                ],
            },
        ]
    )
    def test_pop(self, writes: Sequence[_KeysValue], pops: Sequence[_KeysValue]):
        """Tests popping data from the dictionary.

        Args:
                writes: Writes into the dictionary.
                pops: Pops to test after all writes complete.
        """
        container = NestedKeyDictionary()
        for keys, value in writes:
            container.set(keys, value)
        for keys, value in pops:
            self.assertEqual(value, container.pop(keys))


if __name__ == "__main__":
    absltest.main()
