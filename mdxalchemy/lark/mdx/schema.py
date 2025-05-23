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
                try:
                    expression = next(child.find_data(MEMBER_EXPRESSION))
                except StopIteration:
                    expression = None

                if expression:
                    expression = expression.children[0].value
                    #! since the design of grammar, the member with expression has one additional layer then normal member. so we need to get the first child of the first child
                    return Member.from_tree(
                        member=child.children[0].children[0],
                        expression=expression,
                        _tree=tree)
                return Member.from_tree(member=child.children[0], _tree=tree)
            case 'function':
                FUNCTION = 'function'
                function_tree = next(child.find_data(FUNCTION)).children[0]
                function = Function(name=function_tree.data.value,
                                    _tree=function_tree)

                for child in function_tree.children:
                    if isinstance(child, lark.Token):
                        continue
                    child = child if child.data != 'literals' else lark.Tree(
                        'literals', [child])
                    function.add_paramters(SetExpression.analyze(child))
                return function
            case 'literals':
                return Literal.from_tree(child)
            case _:
                raise ValueError(f"Unknown tree data: {child.data}")

    @property
    def data(self):
        return {}

    def to_json(self):
        return {'type': self.type, 'data': self.data}


@dataclass(kw_only=True)
class Function(SetExpression):
    name: str
    type: str = field(default='function')
    parameters: list[SetExpression] = field(default_factory=list)

    def add_paramters(self, expression: SetExpression):
        self.parameters.append(expression)

    @property
    def data(self):
        return {
            'name': self.name,
            'parameters': [i.to_json() for i in self.parameters]
        }


@dataclass(kw_only=True)
class Literal(SetExpression):
    type: str = field(default='literal')
    value: str = field(default='')

    @classmethod
    def from_tree(cls, _tree):
        return cls(value=[
            i for i in _tree.children if isinstance(i, lark.Token)
        ][0].value,
                   _tree=_tree)

    @property
    def data(self):
        return {'data': self.value}


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
