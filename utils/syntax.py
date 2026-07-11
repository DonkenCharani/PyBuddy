import ast
import traceback

def validate_syntax(code: str) -> tuple[bool, str]:
    """
    Validates Python code syntax using the Abstract Syntax Tree (AST) parser.
    Does not execute the code, making it safe from code injection.
    
    Returns:
        (True, "") if code is syntactically correct.
        (False, error_details) if code contains syntax errors.
    """
    if not code.strip():
        return True, ""
        
    try:
        ast.parse(code)
        return True, ""
    except SyntaxError as e:
        # Format a user-friendly error message indicating line and column
        error_msg = f"Syntax Error: {e.msg} (Line {e.lineno}, Col {e.offset})"
        if e.text:
            error_msg += f"\nCode block: {e.text.strip()}"
        return False, error_msg
    except Exception as e:
        return False, f"Unexpected Validation Error: {str(e)}"

def format_code(code: str) -> str:
    """
    Formats the given Python code using 'black' if it is syntactically correct.
    Fallback to the original code if formatting fails or syntax is invalid.
    """
    try:
        import black
        # Check syntax first to avoid black exceptions
        is_valid, _ = validate_syntax(code)
        if not is_valid:
            return code
            
        formatted = black.format_str(code, mode=black.Mode())
        return formatted
    except Exception:
        # Fall back to original code if formatting fails
        return code
