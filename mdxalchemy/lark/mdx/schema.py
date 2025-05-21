from dataclasses import dataclass
import lark
from enum import StrEnum, auto

class Axis(StrEnum): 
  rows = auto()
  columns = auto()
      
@dataclass
class AxisStatement:
  axis: Axis
  non_empty: bool
  set_expressions: list[str]
  
  def to_json(self): 
    return {
      'axis': self.axis,
      'non_empty': self.non_empty,
      'set_expressions': self.set_expressions
    }
  
@dataclass 
class Member: 
  dimension: str
  hierarchy: str
  element: str
  
  @classmethod 
  def from_tree(cls, member: lark.Tree):
    if len(result:=[i.value for i in member.scan_values(lambda x : isinstance(x, lark.Token)) if i.type == 'IDENTIFIER']) == 2: 
      dimension, element = result
      return cls(dimension=dimension, hierarchy=dimension, element=element)
    dimension, hierarchy, element = result
    return cls(dimension=dimension, hierarchy=hierarchy, element=element)
  
  def to_json(self): 
    return {
      'dimension': self.dimension,
      'hierarchy': self.hierarchy,
      'element': self.element
    }


@dataclass
class WhereStatement: 
  members: list[Member]

  def to_json(self): 
    return {
      'members': [member.to_json() for member in self.members]
    }

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
