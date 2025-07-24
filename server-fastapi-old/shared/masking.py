"""
Code masking engine for SyntaxMem
Intelligently masks tokens in code based on difficulty level
"""
import random
import re
from typing import List, Tuple, Dict
from pygments import lex
from pygments.lexers import PythonLexer, JavascriptLexer, get_lexer_by_name
from pygments.token import Keyword, Punctuation, Operator, Name, Comment, String


class CodeMasker:
    """Handles intelligent code masking for practice exercises"""
    
    def __init__(self):
        self.lexers = {
            "python": PythonLexer(),
            "javascript": JavascriptLexer(),
            "js": JavascriptLexer(),
        }
    
    def mask_code(self, code: str, language: str, difficulty: int = 5) -> Tuple[str, List[str]]:
        """
        Mask code tokens based on difficulty level
        
        Args:
            code: Source code to mask
            language: Programming language (python, javascript)
            difficulty: Difficulty level 1-10 (higher = more masking)
            
        Returns:
            Tuple of (masked_code, list_of_answers)
        """
        if not 1 <= difficulty <= 10:
            raise ValueError("Difficulty must be between 1 and 10")
        
        language = language.lower()
        if language not in self.lexers:
            raise ValueError(f"Unsupported language: {language}")
        
        lexer = self.lexers[language]
        return self._mask_tokens_in_code(code, lexer, difficulty)
    
    def _mask_tokens_in_code(self, code: str, lexer, difficulty: int) -> Tuple[str, List[str]]:
        """Internal method to mask tokens using pygments lexer"""
        masked_code = ""
        answers = []
        probability = difficulty / 10  # Convert difficulty to probability: 0.1–1.0
        
        in_import = False
        in_string = False
        current_line = ""
        
        for token_type, token_value in lex(code, lexer):
            current_line += token_value
            
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
                current_line = ""
            
            # Skip masking for imports, comments, and strings
            if in_import or in_string or token_type in Comment:
                masked_code += token_value
            else:
                should_mask = self._should_mask_token(token_type, token_value, difficulty)
                
                if should_mask and token_value.strip() and random.random() < probability:
                    # Create mask placeholder
                    mask_length = len(token_value.strip())
                    mask = "_" * max(1, min(mask_length, 10))  # Limit mask length
                    
                    # Preserve leading/trailing whitespace
                    leading_space = len(token_value) - len(token_value.lstrip())
                    trailing_space = len(token_value) - len(token_value.rstrip())
                    
                    masked_token = token_value[:leading_space] + mask + token_value[len(token_value)-trailing_space:]
                    masked_code += masked_token
                    answers.append(token_value.strip())
                else:
                    masked_code += token_value
        
        return masked_code, answers
    
    def _should_mask_token(self, token_type, token_value: str, difficulty: int) -> bool:
        """Determine if a token should be eligible for masking"""
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
            Punctuation,
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
    
    def calculate_score(self, user_answers: List[str], correct_answers: List[str], 
                       time_taken: float, max_time: float = 300) -> Dict[str, float]:
        """
        Calculate practice session score
        
        Args:
            user_answers: List of user's answers
            correct_answers: List of correct answers
            time_taken: Time taken in seconds
            max_time: Maximum time for full time score
            
        Returns:
            Dict with detailed scoring breakdown
        """
        if len(user_answers) != len(correct_answers):
            raise ValueError("Answer lists must be the same length")
        
        if not correct_answers:
            return {"total_score": 0, "accuracy": 0, "time_bonus": 0, "mistakes": 0}
        
        # Calculate accuracy
        similarities = []
        mistakes = 0
        
        for user_ans, correct_ans in zip(user_answers, correct_answers):
            similarity = self.validate_answer(user_ans, correct_ans)
            similarities.append(similarity)
            if similarity < 0.8:  # Consider < 80% similarity as mistake
                mistakes += 1
        
        accuracy = sum(similarities) / len(similarities)
        
        # Calculate time bonus (faster = better, but with diminishing returns)
        time_ratio = min(time_taken / max_time, 1.0)
        time_bonus = max(0, 1.0 - time_ratio) * 0.2  # Up to 20% bonus for speed
        
        # Total score (0-100)
        total_score = (accuracy * 80) + (time_bonus * 100)
        total_score = round(min(total_score, 100), 2)
        
        return {
            "total_score": total_score,
            "accuracy": round(accuracy, 3),
            "time_bonus": round(time_bonus, 3),
            "mistakes": mistakes,
            "time_taken": time_taken
        }


# Convenience functions - create new instance per request to avoid any potential issues
def mask_code(code: str, language: str, difficulty: int = 5) -> Tuple[str, List[str]]:
    """Convenience function to mask code"""
    masker = CodeMasker()
    return masker.mask_code(code, language, difficulty)


def validate_answer(user_answer: str, correct_answer: str, strict: bool = False) -> float:
    """Convenience function to validate answer"""
    masker = CodeMasker()
    return masker.validate_answer(user_answer, correct_answer, strict)


def calculate_score(user_answers: List[str], correct_answers: List[str], 
                   time_taken: float, max_time: float = 300) -> Dict[str, float]:
    """Convenience function to calculate score"""
    masker = CodeMasker()
    return masker.calculate_score(user_answers, correct_answers, time_taken, max_time)