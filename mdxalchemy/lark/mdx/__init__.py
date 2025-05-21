from lark import Lark 
from importlib import resources 
from .schema import  QueryStatement

import lark 
from .const  import GRAMMAR_LARK, QUERY_STATEMENT
from .analyzer import retrieve_cube_source, retrieve_on_row_axis_statement, retrieve_on_column_axis_statement, retrieve_where_statement, retrieve_cube_source

_PACKAGE_NAME: str = __package__ if __package__ else "" 

assert isinstance(_PACKAGE_NAME, str), "Package name must be a string"
assert isinstance(GRAMMAR_LARK, str), "Grammar file name must be a string"

parser = Lark(resources.read_text(_PACKAGE_NAME, GRAMMAR_LARK),)

def analyze(mdx: str) -> QueryStatement:
    tree = parser.parse(mdx)
    assert isinstance(tree, lark.Tree), "Parsed tree should be of type lark.Tree"
    assert len(tree.children) == 1, "Parsed tree should have one child"
    root_tree: lark.Tree = tree.children[0]
    query_statement = QueryStatement()
    assert root_tree.data == lark.Token('RULE', QUERY_STATEMENT), "Root tree should be of type query_statement"
    
    query_statement.columns = retrieve_on_column_axis_statement(root_tree)
    query_statement.rows = retrieve_on_row_axis_statement(root_tree)
    query_statement.where = retrieve_where_statement(root_tree)
    query_statement.cube = retrieve_cube_source(root_tree)
    return query_statement
