from lark import Lark
import lark
from importlib import resources

_PACKAGE_NAME: str = __package__ if __package__ else ""
GRAMMAR_LARK = 'grammar.lark'


def __create_parser():
    assert isinstance(_PACKAGE_NAME, str), "Package name must be a string"
    assert isinstance(GRAMMAR_LARK, str), "Grammar file name must be a string"
    return Lark(resources.read_text(_PACKAGE_NAME, GRAMMAR_LARK),)


def parse_mdx(mdx: str) -> lark.Tree:
    """
    Parses the given MDX string and returns a Lark Tree.

    :param mdx: The MDX string to parse.
    :return: A Lark Tree representing the parsed MDX.
    """
    assert isinstance(mdx, str), "MDX must be a string"

    parser = __create_parser()
    try:
        return parser.parse(mdx)
    except lark.exceptions.UnexpectedToken as e:
        error_message = (
            "Unexpected token in MDX parsing, please check the syntax, or copy the following context to raise an issue at GitHub if mdx is valid.\n"
            f"Unexpected token '{e.token}' at line {e.line}, column {e.column}.\n"
            f"Input: {mdx}\n")
        raise Exception(f'{error_message}')
    except Exception as e:
        error_message = (
            "Unknown error occurred while parsing the MDX string, please check the syntax, or copy the following context to raise an issue at GitHub if mdx is valid.\n"
            f"Error: {str(e)}\n"
            f"Input: {mdx}\n")
        raise Exception(f'{error_message}') from e
