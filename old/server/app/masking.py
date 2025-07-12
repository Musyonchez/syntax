import random
from pygments import lex
from pygments.lexers import PythonLexer, JavascriptLexer
from pygments.token import Keyword, Punctuation, Operator, Name, Comment


# Alternatives You might consider (if you want smarter control later):
# Token importance weighting:

# Prioritize masking based on how essential a token is to understanding logic (e.g., mask return before print).

# Harder to implement but makes the quiz more meaningful.

# Adaptive masking:

# Track which types the user struggles with and increase masking in those areas.

# Pattern-based masking:

# Use syntactic patterns (e.g., always mask loop keywords in difficulty 7+) instead of pure randomness.


#  elif language.lower() == "javascript":
#         lexer = JavascriptLexer()
#         masked_code = ""
#         for token_type, token_value in lex(code, lexer):
#             # Skip comments entirely
#             if token_type in Comment:
#                 continue

#             # Mask all Keyword types
#             elif token_type in Keyword:
#                 masked_code += "___" if token_value.strip() else token_value

#             # Mask all Punctuation
#             elif token_type in Punctuation:
#                 masked_code += "___" if token_value.strip() else token_value

#             # Mask all Operator types
#             elif token_type in Operator:
#                 masked_code += "___" if token_value.strip() else token_value

#             # Mask specific Name types
#             elif token_type in {
#                 Name.Builtin,
#                 Name.Builtin.Pseudo,
#                 Name.Decorator,
#                 Name.Exception,
#             }:
#                 masked_code += "___" if token_value.strip() else token_value

#             # Leave everything else unmasked
#             else:
#                 masked_code += token_value

#         return masked_code


def mask_code_content(code: str, language: str, difficulty: int = 5) -> str:
    """
    Masks language-specific tokens in code for user practice.
    Difficulty is an integer from 1 (easiest) to 10 (hardest).
    """
    if not 1 <= difficulty <= 10:
        raise ValueError("Difficulty must be between 1 and 10.")

    if language.lower() == "python":
        lexer = PythonLexer()
        return mask_tokens_in_code(code, lexer, difficulty)
    elif language.lower() == "javascript":
        lexer = JavascriptLexer()
        return mask_tokens_in_code(code, lexer, difficulty)
    else:
        raise ValueError("Unsupported language. Use 'python' or 'javascript'.")


def mask_tokens_in_code(code, lexer, difficulty):
    masked_code = ""
    answers = []
    probability = difficulty / 10  # Convert difficulty to probability: 0.1–1.0

    in_import = False
    current_line = ""

    for token_type, token_value in lex(code, lexer):
        current_line += token_value

        # Detect import lines
        if token_type in Keyword and token_value.strip() in ("import", "from"):
            in_import = True

        if token_value == "\n":
            in_import = False
            current_line = ""

        if in_import or token_type in Comment:
            masked_code += token_value
        else:
            should_mask = token_type in (
                Keyword,
                Punctuation,
                Operator,
                Name.Builtin,
                Name.Builtin.Pseudo,
                Name.Decorator,
                Name.Exception,
            )

            if should_mask and token_value.strip() and random.random() < probability:
                masked_code += "___"
                answers.append(token_value.strip())  # Save actual token as answer
            else:
                masked_code += token_value

    return masked_code, answers
