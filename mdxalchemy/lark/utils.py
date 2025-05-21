import lark 

def revert_tree(tree: lark.Tree, buffer: str = ''): 
  for child in tree.children: 
    if isinstance(child, lark.Token): 
      buffer += child.value
    if isinstance(child, lark.Tree):
      buffer = revert_tree(child, buffer)
  return buffer
      