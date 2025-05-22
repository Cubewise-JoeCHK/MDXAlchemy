from mdxalchemy.lark.mdx.schema import QueryStatement
from .lark.mdx import analyze
from TM1py.Objects.NativeView import NativeView
from TM1py.Objects.Axis import ViewAxisSelection, ViewTitleSelection
from TM1py.Objects.Subset import AnonymousSubset


def mdx_to_tm1py_native_view(mdx: str):
    query_statement: QueryStatement = analyze(mdx)
    title: list[ViewTitleSelection] = [
        ViewTitleSelection(dimension_name=member.dimension,
                           subset=AnonymousSubset(
                               dimension_name=member.dimension,
                               hierarchy_name=member.hierarchy,
                               elements=member.element),
                           selected=member.element)
        for member in query_statement.where.members
    ]
    rows: list[ViewAxisSelection] = [
        ViewAxisSelection(dimension_name=member.dimension,
                          subset=AnonymousSubset(
                              dimension_name=member.dimension,
                              hierarchy_name=member.hierarchy,
                              expression=member.mdx))
        for member in query_statement.rows.set_expressions
    ]
    columns: list[ViewAxisSelection] = [
        ViewAxisSelection(dimension_name=member.dimension,
                          subset=AnonymousSubset(
                              dimension_name=member.dimension,
                              hierarchy_name=member.hierarchy,
                              expression=member.mdx))
        for member in query_statement.columns.set_expressions
    ]
    cube_name: str = query_statement.cube

    return NativeView(
        titles=title,
        rows=rows,
        columns=columns,
        cube_name=cube_name,
        view_name='MDX to TM1py Native View',
        suppress_empty_columns=query_statement.columns.non_empty,
        suppress_empty_rows=query_statement.rows.non_empty,
    )
