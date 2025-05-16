from pygments import lex
from pygments.lexers import PythonLexer, JavascriptLexer
from pygments.token import Keyword, Punctuation, Operator, Comment, Name


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


def mask_code_content(code: str, language: str) -> str:
    """Masks language-specific tokens in code for user practice."""

    if language.lower() == "python":
        lexer = PythonLexer()
        return mask_tokens_in_code(code, lexer)
    elif language.lower() == "javascript":
        lexer = JavascriptLexer()
        return mask_tokens_in_code(code, lexer)
    else:
        raise ValueError("Unsupported language. Use 'python' or 'javascript'.")


def mask_tokens_in_code(code, lexer):
    masked_code = ""
    for token_type, token_value in lex(code, lexer):
        # Skip comments entirely
        if token_type in Comment:
            continue

        # Mask all Keyword types
        elif token_type in Keyword:
            masked_code += "___" if token_value.strip() else token_value

        # Mask all Punctuation
        elif token_type in Punctuation:
            masked_code += "___" if token_value.strip() else token_value

        # Mask all Operator types
        elif token_type in Operator:
            masked_code += "___" if token_value.strip() else token_value

        # Mask specific Name types
        elif token_type in {
            Name.Builtin,
            Name.Builtin.Pseudo,
            Name.Decorator,
            Name.Exception,
        }:
            masked_code += "___" if token_value.strip() else token_value

        # Leave everything else unmasked
        else:
            masked_code += token_value

    return masked_code
