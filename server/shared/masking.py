"""
Code masking engine for SyntaxMem
Intelligently masks tokens in code based on difficulty level
Updated for Flask serverless functions
"""
import random
import re
import hashlib
from typing import List, Tuple, Dict, Any
from pygments import lex
from pygments.lexers import PythonLexer, JavascriptLexer, get_lexer_by_name
from pygments.token import Keyword, Punctuation, Operator, Name, Comment, String


def generate_blank_id() -> str:
    """Generate unique ID for blanks"""
    return hashlib.md5(str(random.random()).encode()).hexdigest()[:8]


class CodeMasker:
    """Handles intelligent code masking for practice exercises"""
    
    def __init__(self):
        self.lexers = {
            "python": PythonLexer(),
            "javascript": JavascriptLexer(),
            "js": JavascriptLexer(),
        }
    
    def mask_code(self, code: str, language: str, difficulty: int = 5) -> Dict[str, Any]:
        """
        Mask code tokens based on difficulty level
        
        Args:
            code: Source code to mask
            language: Programming language (python, javascript)
            difficulty: Difficulty level 1-10 (higher = more masking)
            
        Returns:
            Dict with masked_code, blanks list, and metadata
        """
        if not 1 <= difficulty <= 10:
            raise ValueError("Difficulty must be between 1 and 10")
        
        language = language.lower()
        if language not in self.lexers:
            raise ValueError(f"Unsupported language: {language}")
        
        lexer = self.lexers[language]
        return self._mask_tokens_in_code(code, lexer, difficulty)
    
    def _mask_tokens_in_code(self, code: str, lexer, difficulty: int) -> Dict[str, Any]:
        """Internal method to mask tokens using pygments lexer"""
        masked_code = ""
        blanks = []
        probability = difficulty / 10  # Convert difficulty to probability: 0.1–1.0
        
        in_import = False
        in_string = False
        position = 0
        
        for token_type, token_value in lex(code, lexer):
            # Detect import lines (preserve imports)
            if token_type in Keyword and token_value.strip() in ("import", "from", "require", "include"):
                in_import = True
            
            # Detect strings (preserve string contents)
            if token_type in String:
                in_string = True
            
            # Reset flags on newline
            if token_value == "\n":
                in_import = False
                in_string = False
            
            # Skip masking for imports, comments, and strings
            if in_import or in_string or token_type in Comment:
                masked_code += token_value
            else:
                should_mask = self._should_mask_token(token_type, token_value, difficulty)
                
                if should_mask and token_value.strip() and random.random() < probability:
                    # Create blank
                    blank_id = generate_blank_id()
                    blank_placeholder = f"____{blank_id}____"
                    
                    # Store blank information
                    blank_info = {
                        "id": blank_id,
                        "correct_answer": token_value.strip(),
                        "token_type": str(token_type),
                        "start_position": position,
                        "end_position": position + len(token_value),
                        "hint": self._get_token_hint(token_type, token_value),
                        "difficulty_level": self._get_token_priority(token_type)
                    }
                    blanks.append(blank_info)
                    
                    # Add placeholder to masked code
                    masked_code += blank_placeholder
                else:
                    masked_code += token_value
            
            position += len(token_value)
        
        return {
            "masked_code": masked_code,
            "blanks": blanks,
            "original_length": len(code),
            "masked_length": len(masked_code),
            "total_blanks": len(blanks),
            "difficulty": difficulty,
            "language": language
        }
    
    def _should_mask_token(self, token_type, token_value: str, difficulty: int) -> bool:
        """Determine if a token should be eligible for masking"""
        # Skip very short tokens
        if len(token_value.strip()) < 2:
            return False
        
        # Skip common punctuation
        if token_value.strip() in ['.', ',', ';', ':', '(', ')', '[', ']', '{', '}']:
            return False
        
        # Always mask these token types
        high_priority = {
            Keyword,
            Operator,
            Name.Builtin,
            Name.Builtin.Pseudo,
            Name.Exception,
        }
        
        # Medium priority (mask at higher difficulties)
        medium_priority = {
            Name.Function,
            Name.Class,
        }
        
        # Low priority (only mask at very high difficulties)
        low_priority = {
            Name,
        }
        
        if token_type in high_priority:
            return True
        elif token_type in medium_priority:
            return difficulty >= 4
        elif token_type in low_priority:
            return difficulty >= 7
        
        return False
    
    def _get_token_priority(self, token_type) -> int:
        """Get priority for token masking (higher = more important)"""
        if token_type in Keyword:
            return 10
        if token_type in Operator:
            return 9
        if token_type in Name.Builtin:
            return 8
        if token_type in Name.Function:
            return 7
        if token_type in Name.Class:
            return 7
        if token_type in Name:
            return 5
        return 3
    
    def _get_token_hint(self, token_type, token_value: str) -> str:
        """Generate a hint for the masked token"""
        if token_type in Keyword:
            return f"Keyword ({len(token_value)} letters)"
        elif token_type in Name.Function:
            return f"Function name ({len(token_value)} letters)"
        elif token_type in Name.Class:
            return f"Class name ({len(token_value)} letters)"
        elif token_type in Name:
            return f"Variable ({len(token_value)} letters)"
        elif token_type in Operator:
            return f"Operator ({len(token_value)} chars)"
        else:
            return f"{len(token_value)} characters"
    
    def validate_answer(self, user_answer: str, correct_answer: str, strict: bool = False) -> float:
        """
        Validate user answer against correct answer
        
        Args:
            user_answer: User's input
            correct_answer: Expected answer
            strict: If True, requires exact match. If False, allows similar matches
            
        Returns:
            Similarity score between 0.0 and 1.0
        """
        if not user_answer or not correct_answer:
            return 0.0
        
        user_answer = user_answer.strip()
        correct_answer = correct_answer.strip()
        
        # Exact match
        if user_answer == correct_answer:
            return 1.0
        
        if strict:
            return 0.0
        
        # Case insensitive match
        if user_answer.lower() == correct_answer.lower():
            return 0.9
        
        # Fuzzy matching using simple string similarity
        return self._calculate_similarity(user_answer.lower(), correct_answer.lower())
    
    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """Calculate similarity between two strings using longest common subsequence"""
        if not str1 or not str2:
            return 0.0
        
        # Simple similarity calculation
        longer = str1 if len(str1) > len(str2) else str2
        shorter = str2 if len(str1) > len(str2) else str1
        
        if len(longer) == 0:
            return 1.0
        
        # Count matching characters in order
        matches = 0
        j = 0
        for i in range(len(shorter)):
            while j < len(longer) and longer[j] != shorter[i]:
                j += 1
            if j < len(longer):
                matches += 1
                j += 1
        
        return matches / len(longer)


# Convenience functions for Flask functions
def mask_code(code: str, language: str, difficulty: int = 5) -> Dict[str, Any]:
    """Convenience function to mask code"""
    masker = CodeMasker()
    return masker.mask_code(code, language, difficulty)


def validate_answer(user_answer: str, correct_answer: str, strict: bool = False) -> float:
    """Convenience function to validate answer"""
    masker = CodeMasker()
    return masker.validate_answer(user_answer, correct_answer, strict)