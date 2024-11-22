import unittest
from lark import Lark, exceptions
import xml.etree.ElementTree as ET
import lxml.etree
import lxml.html
from io import StringIO

from main import SimpleTransformer, dict_to_xml, generate_xml, parse_text, grammar

class TestConfigParser(unittest.TestCase):

    def setUp(self):
        self.config_parser = Lark(grammar)

    def test_parse_simple_constant(self):
        input_text = "set a = 10"
        expected_output = {"constants": [[{"set": {"name": "a", "value": 10}}]]}
        parsed_data = parse_text(self.config_parser, input_text)
        self.assertEqual(parsed_data, expected_output)

    def test_parse_array(self):
        input_text = "set arr = (1, 2, 3)"
        expected_output = {"constants": [[{"set": {"name": "arr", "value": {"array": [1, 2, 3]}}}]]}
        parsed_data = parse_text(self.config_parser, input_text)
        self.assertEqual(parsed_data, expected_output)

    def test_parse_dict(self):
        input_text = "set dict = {a = 1, b = 2}"
        expected_output = {"constants": [[{"set": {"name": "dict", "value": {"dict": [{"name": "a", "value": 1}, {"name": "b", "value": 2}]}}}]]}
        parsed_data = parse_text(self.config_parser, input_text)
        self.assertEqual(parsed_data, expected_output)

    def test_parse_clone_value(self):
        input_text = "set a = 10\nset b = $a"
        expected_output = {"constants": [[{"set": {"name": "a", "value": 10}}, {"set": {"name": "b", "value": 10}}]]}
        parsed_data = parse_text(self.config_parser, input_text)
        self.assertEqual(parsed_data, expected_output)

    def test_parse_comment(self):
        input_text = "set a = 10\n*>\nset b = 20"
        expected_output = {"constants": [[{"set": {"name": "a", "value": 10}}, None, {"set": {"name": "b", "value": 20}}]]}
        parsed_data = parse_text(self.config_parser, input_text)
        self.assertEqual(parsed_data, expected_output)

    def test_syntax_error(self):
        input_text = "set a ="
        with self.assertRaises(Exception) as context:
            parse_text(self.config_parser, input_text)
        self.assertTrue("Ошибка синтаксиса" in str(context.exception))


if __name__ == "__main__":
    unittest.main()
