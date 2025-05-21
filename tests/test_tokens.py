import lark 

TEST_CASE = """
SELECT 
  NON EMPTY 
   {[M Bus ETA].[M Bus ETA].Members}  
  ON COLUMNS , 
  NON EMPTY 
   {[KMB Stop].[KMB Stop].Members}  
  ON ROWS 
FROM [Bus ETA] 
WHERE 
  (
   [Bus Route].[Bus Route].[74D],
   [Bus Bound].[Bus Bound].[I],
   [Bus Service].[Bus Service].[All Service]
  )
"""
  


def test_parser(): 
  from mdxalchemy.lark.mdx import parser

  tree = parser.parse(TEST_CASE)
  assert isinstance(tree, lark.Tree), "Parsed tree should be of type lark.Tree"
  assert len(tree.children) == 1, "Parsed tree should have one child"

def test_analyzer(): 
  from mdxalchemy.lark.mdx import analyze
  from mdxalchemy.lark.mdx.schema import QueryStatement, AxisStatement, WhereStatement, Member

  query_statement = analyze(TEST_CASE)
  assert isinstance(query_statement, QueryStatement), "Query statement should be of type QueryStatement"
  assert isinstance(query_statement.rows, AxisStatement), "Rows should be of type AxisStatement"
  assert isinstance(query_statement.columns, AxisStatement), "Columns should be of type AxisStatement"
  assert isinstance(query_statement.where, WhereStatement), "Where should be of type WhereStatement"

  assert query_statement.rows.axis == 'rows', "Axis should be 'rows'"
  assert query_statement.columns.axis == 'columns', "Axis should be 'columns'"
  assert query_statement.rows.non_empty == True, "Rows should be non-empty"
  assert query_statement.columns.non_empty == True, "Columns should be non-empty"
  assert len(query_statement.rows.set_expressions) == 1, "Rows should have one set expression"
  assert len(query_statement.columns.set_expressions) == 1, "Columns should have one set expression"
  assert len(query_statement.where.members) == 3, "Where should have three members"
  
def test_retrieve_cube_source():
  from mdxalchemy.lark.mdx import retrieve_cube_source
  from mdxalchemy.lark.mdx import parser 
  tree = parser.parse(TEST_CASE)
  assert isinstance(tree, lark.Tree), "Parsed tree should be of type lark.Tree"
  assert len(tree.children) == 1, "Parsed tree should have one child"
  root_tree: lark.Tree = tree.children[0]
  cube_source = retrieve_cube_source(root_tree)
  assert cube_source == 'Bus ETA', "Cube source should be 'Bus ETA'"
  