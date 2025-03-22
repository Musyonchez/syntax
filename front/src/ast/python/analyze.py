# import ast
# import sys
# import json

# code = sys.stdin.read()
# tree = ast.parse(code)
# ast_json = ast.dump(tree, annotate_fields=True, include_attributes=True)

# print(json.dumps(ast_json))


import ast
import sys
import json

code = sys.stdin.read()

try:
    # Attempt to parse the code
    tree = ast.parse(code)
    partial = False
except SyntaxError:
    # If there's a syntax error, it's likely because the code is incomplete
    tree = ast.parse(code + '\npass')  # Append `pass` to make it syntactically complete
    partial = True

def node_to_dict(node):
    if isinstance(node, ast.AST):
        fields = {a: node_to_dict(b) for a, b in ast.iter_fields(node)}
        return {
            '_type': node.__class__.__name__,
            **fields
        }
    elif isinstance(node, list):
        return [node_to_dict(item) for item in node]
    else:
        return node

ast_dict = node_to_dict(tree)
print(json.dumps({'ast': ast_dict, 'partial': partial}, indent=2))
