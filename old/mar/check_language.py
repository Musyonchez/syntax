from pygments.lexers import guess_lexer
from pygments.util import ClassNotFound

def detect_language(code):
    """Detects the programming language of a code file."""
    try:
        # with open(file_path, "r", encoding="utf-8") as f:
        #     code = f.read()

        lexer = guess_lexer(code)  # Try to guess the language
        return lexer.name  # Return the detected language name

    except ClassNotFound:
        return "Unknown"
    # except FileNotFoundError:
    #     return f"Error: File '{file_path}' not found."
    except Exception as e:
        return f"Error: {e}"

# file_path = "mar/sample_codes/Swift.txt"  # Change this if using a different file
# detected_language = detect_language(file_path)
# print(f"Detected Language: {detected_language}")
