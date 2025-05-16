
import sys
import os

# Ensure the app module is discoverable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

from masking import mask_code_content

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
    difficulty = 5
    
    print("\n--- Python Code Masking ---")
    print(mask_code_content(test_python, "python", difficulty))

    print("\n--- JavaScript Code Masking ---")
    print(mask_code_content(test_js, "javascript", difficulty))



# from pygments.token import Token

# def list_token_hierarchy(base_token):
#     for name in dir(base_token):
#         attr = getattr(base_token, name)
#         if isinstance(attr, type(base_token)):
#             print(f"{base_token} -> {attr}")

# list_token_hierarchy(Token)
# list_token_hierarchy(Token.Keyword)
# list_token_hierarchy(Token.Operator)
# list_token_hierarchy(Token.Punctuation)
