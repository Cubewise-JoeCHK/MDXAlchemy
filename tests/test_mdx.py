import os
from TM1Alchemy.mdx.parser import parse_mdx
import pytest
import lark


def walk_through_test_cases():
    case_folder = os.path.join(os.path.dirname(__file__), 'case')
    for case_file in os.listdir(case_folder):
        case_name = os.path.splitext(case_file)[0]
        with open(os.path.join(case_folder, case_file), 'r', encoding='utf-8') as f:
            content = f.read()
            yield case_name, content


def test_alchemist_parse_mdx():
    for case_name, content in walk_through_test_cases():
        assert content is not None, f"Content should not be None, please check the test case file {case_name}.md"
        assert isinstance(content, str), f"Content should be a string, please check the test case file {case_name}.md"
        assert parse_mdx(content)


def test_transform_to_mdx_builder():
    from TM1Alchemy.mdx.transformer import MDXTransformer
    for case_name, content in walk_through_test_cases():
        print(case_name)
        tree = parse_mdx(content)
        try:
            builder = MDXTransformer().transform(tree)
        except lark.exceptions.VisitError as e:
            if 'not supported by mdxpy' in str(e):
                continue
            raise e
