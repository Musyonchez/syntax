import ast

tree = ast.parse("print('hello world')")

print("tree", tree)

exec(compile(tree, filename="<ast>", mode="exec"))
