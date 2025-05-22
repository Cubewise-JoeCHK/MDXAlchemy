from dataclasses import dataclass, field
import lark
from enum import StrEnum, auto
from .const import IDENTIFIER, SHORT_MEMBER, LONG_MEMBER, MEMBER_EXPRESSION, SET_EXPRESSION, MEMBER

from mdxalchemy.lark.utils import revert_tree


@dataclass
class SetExpression:
    _tree: lark.Tree
    type: str = field(default=SET_EXPRESSION)

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
                if expression := next(child.find_data(MEMBER_EXPRESSION)):
                    expression = expression.children[0].value
                    return Member.from_tree(
                        member=child.children[0].children[0],
                        expression=expression,
                        _tree=tree)
                return Member.from_tree(member=child.children[0].children[0],
                                        _tree=tree)
            case _:
                raise ValueError(f"Unknown tree data: {child.data}")

    @property
    def data(self):
        return {}

    def to_json(self):
        return {'type': self.type, 'data': self.data}


class Axis(StrEnum):
    rows = auto()
    columns = auto()


@dataclass(kw_only=True)
class Member(SetExpression):
    dimension: str
    hierarchy: str
    element: str
    expression: str = field(default='')
    type: str = field(default=MEMBER)

    @classmethod
    def from_tree(
        cls,
        member: lark.Tree,
        _tree: lark.Tree,
        expression: str = '',
    ):
        if member.data == SHORT_MEMBER:
            dimension, element = [
                i.value for i in member.scan_values(
                    lambda x: isinstance(x, lark.Token))
                if i.type == IDENTIFIER
            ]
            return cls(dimension=dimension,
                       hierarchy=dimension,
                       element=element,
                       _tree=_tree,
                       expression=expression)
        if member.data == LONG_MEMBER:
            dimension, hierarchy, element = [
                i.value for i in member.scan_values(
                    lambda x: isinstance(x, lark.Token))
                if i.type == IDENTIFIER
            ]
            return cls(dimension=dimension,
                       hierarchy=hierarchy,
                       element=element,
                       _tree=_tree,
                       expression=expression)
        raise ValueError(f"Unknown member data: {member.data}")

    @property
    def data(self):
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
