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


@dataclass
class WhereStatement: 
  members: list[Member]

  
class QueryStatement: 
  rows: AxisStatement
  columns: AxisStatement
  where: WhereStatement
  cube: str
