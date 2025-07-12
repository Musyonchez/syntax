import ast
import sys
import json
import autopep8  # You'll need to install autopep8 using pip

def analyze_code(code):
    try:
        # Attempt to parse the code into an AST
        tree = ast.parse(code)
        
        # If successful, format the code using autopep8
        formatted_code = autopep8.fix_code(code)
        
        # Return the formatted code
        return json.dumps({"formatted_code": formatted_code})

    except SyntaxError as e:
        # If a SyntaxError is encountered, return the error message
        return json.dumps({"error": f"Syntax error: {str(e)}"})

if __name__ == "__main__":
    # Read code from stdin
    input_code = sys.stdin.read()
    
    # Analyze the code
    result = analyze_code(input_code)
    
    # Print the result so it can be captured by the parent process
    print(result)
