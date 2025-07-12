import astor  # You can use astor library for converting AST back to code
import ast

def ast_to_code(ast_dict):
    node = ast.parse('')  # Start with an empty AST
    for key, value in ast_dict.items():
        setattr(node, key, value)
    return astor.to_source(node)
