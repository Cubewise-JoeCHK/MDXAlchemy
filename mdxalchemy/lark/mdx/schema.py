from dataclasses import dataclass
import lark
from enum import StrEnum, auto

from mdxalchemy.lark.utils import revert_tree


@dataclass
class SetExpression:
    _tree: lark.Tree

    @property
    def mdx(self):
        return revert_tree(self._tree)

    @classmethod
    def analyze(cls, tree: lark.Tree):
        # get the first level children of the tree

        match (child := [
                child for child in tree.children
                if isinstance(child, lark.Tree)
        ][0]).data:
            case 'member_with_expression' | 'member':
                if expression := next(child.find_data('member_expression')):
                    expression = expression.children[0].value
                    return Member.from_tree(child.children[0].children[0],
                                            expression=expression)
                return Member.from_tree(child.children[0].children[0])
            case _:
                raise ValueError(f"Unknown tree data: {child.data}")


class Axis(StrEnum):
    rows = auto()
    columns = auto()


@dataclass
class Member(SetExpression):
    dimension: str
    hierarchy: str
    element: str
    expression: str = ''

    @classmethod
    def from_tree(cls, member: lark.Tree, expression: str = ''):
        if member.data == 'short_member':
            dimension, element = [
                i.value for i in member.scan_values(
                    lambda x: isinstance(x, lark.Token))
                if i.type == 'IDENTIFIER'
            ]
            return cls(dimension=dimension,
                       hierarchy=dimension,
                       element=element,
                       _tree=member,
                       expression=expression)
        if member.data == 'long_member':
            dimension, hierarchy, element = [
                i.value for i in member.scan_values(
                    lambda x: isinstance(x, lark.Token))
                if i.type == 'IDENTIFIER'
            ]
            return cls(dimension=dimension,
                       hierarchy=hierarchy,
                       element=element,
                       _tree=member,
                       expression=expression)
        raise ValueError(f"Unknown member data: {member.data}")

    def to_json(self):
        return {
            'dimension': self.dimension,
            'hierarchy': self.hierarchy,
            'element': self.element,
            'expression': self.expression
        }


@dataclass
class AxisStatement:
    axis: Axis
    non_empty: bool
    set_expressions: list[Member]

    def to_json(self):
        return {
            'axis': self.axis,
            'non_empty': self.non_empty,
            'set_expressions': [i.to_json() for i in self.set_expressions]
        }


@dataclass
class WhereStatement:
    members: list[Member]

    def to_json(self):
        return {'members': [member.to_json() for member in self.members]}


class QueryStatement:
    rows: AxisStatement
    columns: AxisStatement
    where: WhereStatement
    cube: str

    def to_json(self):
        return {
            'cube': self.cube,
            'rows': self.rows.to_json(),
            'columns': self.columns.to_json(),
            'where': self.where.to_json()
        }
