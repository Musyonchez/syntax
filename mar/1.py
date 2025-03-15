from pygments import lex
from pygments.lexers import PythonLexer, JavascriptLexer
from pygments.token import Keyword, Punctuation, Operator, Number, Name

def remove_keywords_and_symbols(code: str, language: str):
    """Removes keywords, punctuation, and operators from the given code"""

    # Use the correct lexer instead of guessing
    if language.lower() == "python":
        lexer = PythonLexer()
    elif language.lower() == "javascript":
        lexer = JavascriptLexer()
    else:
        raise ValueError("Unsupported language. Use 'python' or 'javascript'.")

    masked_code = ""

    for token_type, token_value in lex(code, lexer):
        print(token_type, token_value)  # Debugging: print tokens

        if token_type in Keyword or token_type in Punctuation or token_type in Operator:
            masked_code += "_" * len(token_value)  # Replace with underscores
        elif token_type in Number:
            masked_code += "#" * len(token_value)  # Replace numbers with #
        else:
            masked_code += token_value  # Keep variable names and function names

    return masked_code

if __name__ == "__main__":
    # Example Python snippet
    test_python = """ 
def factorial(n):
    if n <= 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
print(factorial(5))
    """

    # Example JavaScript snippet
    test_js = """ 
export const getStaticPaths = async () => {
  return {
    paths: [
      { params: { id: "123" } }
    ],
    fallback: false
  };
}
    """

    print("\n--- Python Code Masking ---")
    print(remove_keywords_and_symbols(test_python, "python"))

    print("\n--- JavaScript Code Masking ---")
    print(remove_keywords_and_symbols(test_js, "javascript"))
