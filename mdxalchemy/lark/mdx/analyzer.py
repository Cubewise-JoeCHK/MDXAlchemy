from .schema import Axis, AxisStatement, WhereStatement, Member, SetExpression
import lark
from .const import IDENTIFIER, WHERE_STATEMENT, NON_EMPTY, SET, MEMBER, ROW_SELECT_STATEMENT, COLUMN_AXIS_STATEMENT


def retrieve_on_row_axis_statement(root_tree: lark.Tree) -> AxisStatement:

    select_statement = next(root_tree.find_data(ROW_SELECT_STATEMENT))
    if not select_statement:
        return AxisStatement(axis=Axis.rows,
                             non_empty=False,
                             set_expressions=[])
    non_empty = bool(_find_non_empty(select_statement))
    set_list = [
        SetExpression.analyze(child)
        for child in select_statement.find_data(SET)
    ]
    return AxisStatement(axis=Axis.rows,
                         non_empty=non_empty,
                         set_expressions=set_list)


def retrieve_on_column_axis_statement(root_tree: lark.Tree) -> AxisStatement:
    select_statement = next(root_tree.find_data(COLUMN_AXIS_STATEMENT))
    if not select_statement:
        return AxisStatement(axis=Axis.columns,
                             non_empty=False,
                             set_expressions=[])
    non_empty = bool(_find_non_empty(select_statement))
    set_list = [
        SetExpression.analyze(child)
        for child in select_statement.find_data(SET)
    ]
    return AxisStatement(axis=Axis.columns,
                         non_empty=non_empty,
                         set_expressions=set_list)


def retrieve_where_statement(root_tree: lark.Tree) -> WhereStatement:
    tree = [
        child for child in root_tree.find_data(WHERE_STATEMENT)
        if [child for child in child.find_data(MEMBER)]
    ]
    if not tree:
        return WhereStatement(members=[])
    assert len(tree) == 1, "There should be only one where statement"
    child = tree[0]
    members = []
    for member in child.find_data(MEMBER):
        members.append(
            Member.from_tree(member.children[0], _tree=member.children[0]), )
    return WhereStatement(members=members)


def retrieve_cube_source(root_tree: lark.Tree):
    return next(
        next(next(root_tree.find_data('cube_source')).find_data(
            'name')).scan_values(lambda x: x.type == IDENTIFIER)).value


def _find_non_empty(tree: lark.Tree):
    try:
        return next(tree.find_data(NON_EMPTY))
    except StopIteration:
        return None
