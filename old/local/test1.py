import ast

tree_ast = ast.parse('''
@app.post("/api/process_code")
async def process_code(request: CodeRequest):
    code = request.code
    result = subprocess.run(['node', 'ast_processor.js', code], capture_output=True, text=True)

    if result.returncode != 0:
        raise HTTPException(status_code=500, detail="Error processing code")

    result_json = json.loads(result.stdout)
    blanked_code = result_json['blankedCode']
    placeholders = result_json['placeholders']
    return {"blankedCode": blanked_code, "placeholders": placeholders}
''')

print(ast.dump(tree_ast, indent=4))
