import sys
from lark import Lark, Transformer, exceptions
import xml.etree.ElementTree as ET
import lxml.etree
import lxml.html

CONSTS = {}

grammar = """ 
    start: constants
    constants: (constant | comment)*

    constant: "set" NAME "=" value

    value: NUMBER | array | dict | clone_value

    clone_value: "$" NAME
    array: "(" [value ("," value)*] ")"
    dict: "{" [pair ("," pair)*] "}"
    pair: NAME "=" value
    comment: "*>" /[^\\r\\n]+/? 

    NAME: /[a-zA-Z][_a-zA-Z0-9]*/
    NUMBER: /[0-9]+([.][0-9]+)?/

    %import common.WS
    %ignore WS
"""

class SimpleTransformer(Transformer):
    def start(self, items):
        return {"constants": items}

    def constants(self, items):
        return items

    def constant(self, items):
        name = items[0]
        value = items[1]
        CONSTS[name] = value
        return {"set": {"name": name, "value": value}}

    def value(self, items):
        return items[0]

    def clone_value(self, items):
        name = items[0]
        if name not in CONSTS:
            raise Exception(f"Неизвестная константа: {name}")
        return CONSTS[name]

    def array(self, items):
        return {"array": items}

    def dict(self, items):
        return {"dict": items}

    def pair(self, items):
        return {"name": items[0], "value": items[1]}

    def comment(self, items):
        return {"comment": items[0]} if items else None

    def NUMBER(self, token):
        return float(token) if '.' in token else int(token)

    def NAME(self, token):
        return token.value


def dict_to_xml(tag, content):
    elem = ET.Element(tag)
    if isinstance(content, dict):
        for key, value in content.items():
            child = dict_to_xml(key, value)
            elem.append(child)
    elif isinstance(content, list):
        for item in content:
            child = dict_to_xml("item", item)
            elem.append(child)
    else:
        elem.text = str(content)
    return elem


def generate_xml(data):
    root = dict_to_xml("constants", data["constants"])
    return root


def parse_text(config_parser, sInputText):
    try:
        parsed_tree = config_parser.parse(sInputText)
        transformer = SimpleTransformer()
        return transformer.transform(parsed_tree)
    except exceptions.UnexpectedInput as e:
        raise Exception(f"Ошибка синтаксиса: {e}")
    except exceptions.LarkError as e:
        raise Exception(f"Общая ошибка парсинга: {e}")


def main():
    if len(sys.argv) != 3:
        print("python script.py <путь_к_входному_файлу> <путь_к_выходному_файлу>", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        with open(input_file, "r", encoding="utf-8") as file:
            input_text = file.read()
    except FileNotFoundError:
        print(f"Файл {input_file} не найден.", file=sys.stderr)
        sys.exit(1)

    config_parser = Lark(grammar)
    try:
        parsed_data = parse_text(config_parser, input_text)
        xml_tree = ET.ElementTree(generate_xml(parsed_data))
        xml_str = ET.tostring(xml_tree.getroot(), encoding='utf-8')
        xml_tree_pretty = lxml.etree.fromstring(xml_str)

        with open(output_file, "wb") as file:
            file.write(lxml.etree.tostring(xml_tree_pretty, pretty_print=True, encoding='utf-8'))

        print(f"Результат успешно записан в {output_file}")

    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
