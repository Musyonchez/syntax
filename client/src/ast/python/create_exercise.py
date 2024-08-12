# import random

# def create_exercise(ast_node):
#     if isinstance(ast_node, dict):
#         for key, value in ast_node.items():
#             if key == 'id':  # For example, remove variable or function names
#                 if random.random() > 0.5:  # Randomly decide whether to remove it
#                     ast_node[key] = '___'  # Placeholder for user to fill in
#             else:
#                 create_exercise(value)
#     elif isinstance(ast_node, list):
#         for item in ast_node:
#             create_exercise(item)

#     return ast_node


import random

def create_exercise(ast_node, depth=0):
    indent = '  ' * depth  # To visualize depth in the AST

    if isinstance(ast_node, dict):
        print(f"{indent}Processing dict node: {ast_node.get('_type', 'unknown')}")

        for key, value in ast_node.items():
            if key == 'id':  # For example, remove variable or function names
                print(f"{indent}Found 'id' key with value '{value}'")
                if random.random() > 0.5:  # Randomly decide whether to remove it
                    print(f"{indent}Replacing '{value}' with '___'")
                    ast_node[key] = '___'  # Placeholder for user to fill in
                else:
                    print(f"{indent}Keeping '{value}' unchanged")
            else:
                print(f"{indent}Descending into key: {key}")
                create_exercise(value, depth + 1)
    elif isinstance(ast_node, list):
        print(f"{indent}Processing list node with {len(ast_node)} elements")
        for index, item in enumerate(ast_node):
            print(f"{indent}Descending into list item {index}")
            create_exercise(item, depth + 1)

    print(f"{indent}Returning node at depth {depth}: {ast_node}")
    return ast_node

# Example usage with an AST node
example_ast = {
    "_type": "Module",
    "body": [
        {
            "_type": "Expr",
            "value": {
                "_type": "Call",
                "func": {
                    "_type": "Name",
                    "id": "print",
                    "ctx": {
                        "_type": "Load"
                    }
                },
                "args": [
                    {
                        "_type": "Constant",
                        "value": "Hello, world!"
                    }
                ],
                "keywords": []
            }
        }
    ],
    "type_ignores": []
}

modified_ast = create_exercise(example_ast)
print("Final modified AST:", modified_ast)
