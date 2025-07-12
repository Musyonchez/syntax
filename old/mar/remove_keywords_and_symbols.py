from pygments import lex
from pygments.lexers import get_lexer_by_name
from pygments.token import Keyword, Punctuation, Operator ## , Number, Name
import check_language

file_path = "mar/sample_codes/JavaScript.txt"  # Change this if using a different file
with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()
detected_language = check_language.detect_language(code)

def remove_keywords_and_symbols(code: str, language: str):
    """Removes keywords, punctuation, and operators from the given code"""

    masked_code = ""

    lexer = get_lexer_by_name(detected_language.lower())  # Convert string to lexer object


    for token_type, token_value in lex(code, lexer):
        print(token_type, token_value)  # Debugging: print tokens

        if token_type in Keyword or token_type in Punctuation or token_type in Operator:
            masked_code += "_" * len(token_value)  # Replace with underscores
        else:
            masked_code += token_value  # Keep variable names and function names

    return masked_code

print("\n--- Python Code Masking ---", detected_language)
print(remove_keywords_and_symbols(code, "javascript"))