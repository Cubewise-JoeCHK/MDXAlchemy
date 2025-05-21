from .schema import Axis, AxisStatement, WhereStatement, Member
import lark 
from .const  import WHERE_STATEMENT, AXIS_STATEMENT, ON_ROWS, ON_COLUMNS, NON_EMPTY, SET, MEMBER
from ..utils import revert_tree

def retrieve_on_row_axis_statement(root_tree: lark.Tree) -> AxisStatement:
  tree = [child for child in root_tree.find_data(AXIS_STATEMENT) if [child for child in child.find_data(ON_ROWS)]]
  assert len(tree) == 1, "There should be only one on_rows statement"
  child = tree[0]
  axis = Axis.rows
  non_empty = bool([child for child in child.find_data(NON_EMPTY)])
  set_list = [revert_tree(child) for child in child.find_data(SET)]
  return AxisStatement(axis=axis, non_empty=non_empty, set_expressions=set_list)

def retrieve_on_column_axis_statement(root_tree: lark.Tree) -> AxisStatement:
  tree = [child for child in root_tree.find_data(AXIS_STATEMENT) if [child for child in child.find_data(ON_COLUMNS)]]
  assert len(tree) == 1, "There should be only one on_columns statement"
  child = tree[0]
  axis = Axis.columns
  non_empty = bool([child for child in child.find_data(NON_EMPTY)])
  set_list = [revert_tree(child) for child in child.find_data(SET)]
  return AxisStatement(axis=axis, non_empty=non_empty, set_expressions=set_list)

def retrieve_where_statement(root_tree: lark.Tree) -> WhereStatement:
  tree = [child for child in root_tree.find_data(WHERE_STATEMENT) if [child for child in child.find_data(MEMBER)]]
  assert len(tree) == 1, "There should be only one where statement"
  child = tree[0]
  members = []
  for member in child.find_data(MEMBER):
    members.append(Member.from_tree(member.children[0]))
  return WhereStatement(members=members)

def retrieve_cube_source(root_tree: lark.Tree):
  return next(next(next(root_tree.find_data('cube_source') ).find_data('name')).scan_values(lambda x: x.type == 'IDENTIFIER')).value

