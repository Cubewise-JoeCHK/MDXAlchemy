from mdxpy.mdx import *
import lark

parse_tuple_to_data = lambda x: {i[0]: i[1] for i in x if isinstance(i, tuple)}


class MDXTransformer(lark.Transformer):

    def string(self, item):
        return item[1].value

    def child(self, item):
        return item[0].value

    def consolidation(self, item):
        return None

    def name(self, item):
        # syntax : [ IDENTIFIER ]
        return [i for i in item if isinstance(i, str)][1]

    def dimension(self, item):
        return ('dimension', item[0])

    def hierarchy(self, item):
        return ('hierarchy', item[0])

    def element(self, item):
        try:
            return ('element', item[0])
        except Exception as e:
            breakpoint()
            raise e

    def member(self, item):
        data = {i[0]: i[1] for i in item if isinstance(i, tuple)}
        try:
            if data.get('element'):
                return Member(dimension=data['dimension'], hierarchy=data.get('hierarchy', data['dimension']),
                              element=data['element'])
            return CurrentMember.build_unique_name(dimension=data['dimension'],
                                                   hierarchy=data.get('hierarchy', data['dimension']))
        except Exception as e:
            breakpoint()
            raise e

    def mdx_tuple(self, item):
        return MdxTuple(members=[i for i in item if isinstance(i, Member)])

    def mdx_axis_row(self, item):
        mdx_axis = MdxAxis.empty()
        for node in item:
            if isinstance(node, lark.Token):
                continue
            if isinstance(node, MdxTuple):
                mdx_axis.add_tuple(node)
        return ('row', mdx_axis)

    def where(self, item):
        return ('where', [i for i in item if isinstance(i, MdxTuple)][0])

    def cube_source(self, item):
        return ('cube', item[0])

    def mdx_axis_column(self, item):
        mdx_axis = MdxAxis.empty()
        for node in item:
            if isinstance(node, lark.Token):
                continue
            if isinstance(node, MdxTuple):
                mdx_axis.add_tuple(node)
        return ('column', mdx_axis)

    def mdx_builder(self, item):
        data = {i[0]: i[1] for i in item if isinstance(i, tuple)}
        builder = MdxBuilder(cube=data['cube'],)
        axes = {}
        if row_data := data.get('row'):
            axes.update({0: row_data})
        if column_data := data.get('column'):
            axes.update({1: column_data})
        builder.axes = axes
        builder._where = where if (where := data.get('where')) else MdxTuple.empty()
        return builder

    def mdx_hierarchy_set(self, item):
        for i in item:
            if isinstance(i, lark.Tree):
                breakpoint()
        return [i for i in item if not isinstance(i, lark.Token)][0]

    def tuples_set(self, item):
        # assume the list of mdx tuple
        assert isinstance((first_member := item[0]),
                          MdxTuple), "the solution assumed the first element of the list is MdxTuple"
        assert isinstance((first_member := first_member.members[0]),
                          Member), "the solution assumed the first element of the MdxTuple is Member"
        dimension = first_member.dimension
        hierarchy = first_member.hierarchy
        tuple_set = TuplesSet(item)
        tuple_set.dimension = dimension
        tuple_set.hierarchy = hierarchy
        return tuple_set

    def tm1_subset_to_set(self, item):
        data = parse_tuple_to_data(item)
        return Tm1SubsetToSetHierarchySet(dimension=data['dimension'],
                                          hierarchy=data.get('hierarchy', data['dimension']),
                                          subset=[i for i in item if isinstance(i, str)][0])

    def drill_down_member(self, item):
        data = [i for i in item if not isinstance(i, lark.Token)]
        return Tm1DrillDownMemberSet(
            underlying_hierarchy_set=data[0],
            other_set=data[1],
        )

    def all_members_hierarchy_set(self, item):
        data = parse_tuple_to_data(item)
        dimension = data['dimension']
        hierarchy = data.get('hierarchy', dimension)
        return AllMembersHierarchySet(dimension=dimension, hierarchy=hierarchy)

    def tm1_subset_all_hierarchy_set(self, item):
        data = parse_tuple_to_data(item)
        dimension = data['dimension']
        hierarchy = data.get('hierarchy', dimension)
        return Tm1SubsetAllHierarchySet(dimension=dimension, hierarchy=hierarchy)

    def tm1_filter_by_pattern(self, item):
        assert isinstance(item[1],
                          MdxHierarchySet), 'the solution assumed the first element of the list is MdxHierarchySet'
        assert isinstance([i for i in item if isinstance(i, str)][0],
                          str), 'the solution assumed there is at least one string in the list'
        return Tm1FilterByPattern(item[1], wildcard=[i for i in item if isinstance(i, str)][0])

    def drill_up_member(self, item):
        raise ValueError("drill up member is not supported by mdxpy")

    def children_hierarchy_set(self, item):
        assert isinstance(item[0], Member), 'the solution assumed the first elemetn of the list is Member'
        return ChildrenHierarchySet(item[0])

    def tm1_filter_by_level(self, item):
        assert isinstance(item[1],
                          MdxHierarchySet), 'the solution assumed the first element of the list is MDXHierarchySet'
        assert (numeric_list :=
                [i.value for i in [i for i in item if isinstance(i, lark.Token)] if i.type == 'NUMERIC'
                ]), 'the solution assumed there is at least one numeric token'
        return Tm1FilterByLevelHierarchySet(underlying_hierarchy_set=item[1], level=int(numeric_list[0]))

    def except_hierarchy_set(self, item):
        assert isinstance(
            item[1], (MdxHierarchySet,
                      TuplesSet)), 'the solution assumed the second element of the list is MDXHierarchySst or TupleSet'
        assert isinstance(
            item[3], (MdxHierarchySet,
                      TuplesSet)), 'the solution assumed the forth element of the list is MDX HierarchySet or TupleSet'
        return ExceptHierarchySet(item[1], item[3])

    def range_hierarchy_set(self, item):
        assert isinstance(item[1], (Member)), 'the solution assumed the second element of the list is Member'
        assert isinstance(item[3], (Member)), 'the solution assumed the fourth element of the list is Member'
        return RangeHierarchySet(item[1], item[3])

    def union_hierarchy_set(self, item):
        assert isinstance(
            item[1], (MdxHierarchySet,
                      TuplesSet)), 'the solution assumed the second element of the list is MDXHierarchySet or TuplesSet'
        assert isinstance(
            item[3], (MdxHierarchySet,
                      TuplesSet)), 'the solution assumed the forth element of the list is MDX HierarchySet or TuplesSet'
        return UnionHierarchySet(item[1], item[3], allow_duplicates=False)

    def tm1_drill_down_member(self, item):

        assert isinstance(
            item[1],
            (MdxHierarchySet, TuplesSet)), 'the solution assumed the second element of the list is MdxHierarchySet'
        assert item[3] == 'ALL' or isinstance(
            item[3], (MdxHierarchySet,
                      TuplesSet)), 'the solution assumed the forth element of the list is MdxHierarchySet or "ALL"'
        other_set = None if item[3] == 'ALL' else item[3]
        recursive = [i for i in item if isinstance(i, lark.Token) and i.type == 'RECURSIVE']
        return Tm1DrillDownMemberSet(underlying_hierarchy_set=item[1], other_set=other_set, recursive=bool(recursive))

    def default_member_hierarchy_set(self, item):
        assert isinstance(item[0], Member), 'the solution assumed the first element of the list is Member'
        return DefaultMemberHierarchySet(item[0].dimension, item[0].hierarchy)

    def order_by_cell_value_hierarchy_set(self, item):
        data = parse_tuple_to_data(item)
        assert isinstance(
            item[1], (MdxHierarchySet,
                      TuplesSet)), 'the solution assumed the second element of the list is MdxHierarchySet or TuplesSet'
        assert isinstance(item[5], (MdxTuple)), 'the solution assumed the fifth element of the list is MdxTuple'
        assert isinstance(data.get('cube'), str), 'the solution assumed there is a cube in the data'
        return OrderByCellValueHierarchySet(underlying_hierarchy_set=item[1], cube=data['cube'], mdx_tuple=item[5])

    def descendants_hierarchy_set(self, item):
        assert isinstance(
            item[1],
            (TuplesSet,
             MdxHierarchySet)), 'the solution assumed the second element of the list is TuplesSet or MdxHierarchySet'
        if len(item) > 3:
            raise ValueError(
                "descendants hierarchy set does not support parameter, but it is needed. raise the issue to GitHub")
        return DescendantsHierarchySet(member=item[1],)
