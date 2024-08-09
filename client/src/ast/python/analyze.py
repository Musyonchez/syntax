import ast
import sys
import json

code = sys.stdin.read()
tree = ast.parse(code)
ast_json = ast.dump(tree, annotate_fields=True, include_attributes=True)

print(json.dumps(ast_json))
