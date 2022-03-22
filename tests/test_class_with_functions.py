import unittest
from unittest.mock import MagicMock, patch

from engine.class_with_functions import GenericClass, ExternalClass


class ClassWithFunctionsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.mapping = self.get_mapping()
        self.setup_external_class()
        self.generic_class = GenericClass(self.mapping, self.mocked_external_class)

    def get_mapping(self):
        self.key1 = "Key1"
        key2 = "Key2"
        self.value1 = "Value1"
        value2 = "Value2"
        return {self.key1: self.value1, key2: value2}

    def setup_external_class(self):
        self.mocked_external_class = MagicMock(ExternalClass)
        self.mocked_external_class.write = MagicMock()
        self.mocked_external_class.get_value_squared = MagicMock(return_value=4)

    def test_that_value_is_written_when_in_mapping(self):
        """The get value function works as intended, testing the write_mapped_value fn"""
        for key in self.mapping:
            with self.subTest(i=key):
                # Inside subtest so it can get reset
                self.generic_class.write_mapped_value(key)
                self.mocked_external_class.write.assert_called_once()
                self.mocked_external_class.write.assert_called_with(found_mapping=True,
                                                                    mapping=self.mapping[key])
                self.mocked_external_class.write = MagicMock()

    def test_that_value_not_written_when_not_in_mapping(self):
        self.generic_class.write_mapped_value("KeyNone")
        self.mocked_external_class.write.assert_called_once()
        self.mocked_external_class.write.assert_called_with()

    def test_will_throw_null_exception(self):
        # more generic
        # with self.assertRaises(Exception):
        with self.assertRaises(KeyError):
            with patch.dict(self.mapping, {}, clear=True):
                value = self.generic_class.get_value_with_no_default("RandomKey")

    def test_not_a_real_test(self):
        key = self.key1
        self.generic_class.write_mapped_value(key)
        self.mocked_external_class.write.assert_called_with(found_mapping=True,
                                                            mapping=self.mapping[key])
        with patch.dict(self.mapping, {key: "SomethingElse"}, clear=True):
            self.generic_class.write_mapped_value(key)
            self.mocked_external_class.write.assert_called_with(found_mapping=True,
                                                                mapping="SomethingElse")

    def test_mocked_value_squared(self):
        actual_external_class = ExternalClass()
        original_values = [1,2,3,4]
        squared_values = [1,4,9,16]

        for i in range(len(original_values)):
            self.assertEqual(squared_values[i], actual_external_class.get_value_squared(original_values[i]))
            self.assertEqual(4, self.mocked_external_class.get_value_squared(original_values[i]))


if __name__ == '__main__':
    unittest.main()
