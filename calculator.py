# calculator.py
import re
import ast


def looks_like_math(expression: str) -> bool:
    if not expression or not isinstance(expression, str):
        return False

    lowered = expression.lower()
    has_number = bool(re.search(r"\d", lowered))
    has_operator = any(
        token in lowered
        for token in (
            " plus ",
            " minus ",
            " times ",
            " multiplied by ",
            " multiply ",
            " divided by ",
            " over ",
            " into ",
            "+",
            "-",
            "*",
            "/",
            " x ",
        )
    )
    return "calculate" in lowered or (has_number and has_operator)
def _safe_eval(expression: str):
    """
    Safely evaluate a math expression constructed from numbers and + - * / and parentheses.
    Uses AST parsing and only allows safe nodes.
    """
    node = ast.parse(expression, mode='eval').body
    def _eval(n):
        # Binary operations
        if isinstance(n, ast.BinOp):
            left = _eval(n.left)
            right = _eval(n.right)
            if isinstance(n.op, ast.Add):
                return left + right
            if isinstance(n.op, ast.Sub):
                return left - right
            if isinstance(n.op, ast.Mult):
                return left * right
            if isinstance(n.op, ast.Div):
                return left / right
            if isinstance(n.op, ast.Pow):
                return left ** right
            raise ValueError("Unsupported operator")
        # Unary +/-
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, (ast.UAdd, ast.USub)):
            val = _eval(n.operand)
            return +val if isinstance(n.op, ast.UAdd) else -val
        # Numbers (Python 3.8+: Constant; older: Num)
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            return n.value
        if hasattr(ast, "Num") and isinstance(n, ast.Num):  # older nodes
            return n.n
        raise ValueError("Unsupported expression")
    return _eval(node)
def calculate(expression: str) -> str:
    """
    Convert common spoken/written math phrases into a safe arithmetic expression,
    then evaluate it and return a spoken-friendly result string.

    Examples supported:
      - "calculate 12 times 5"
      - "what is 12 x 5"
      - "12 * 5"
      - "calculate 3.5 plus 2"
    """
    if not expression or not isinstance(expression, str):
        return "I could not understand the math problem."
    # Normalize
    expr = expression.lower().strip()
    # Remove filler phrases
    expr = expr.replace("calculate", "")
    expr = expr.replace("what is", "")
    expr = expr.replace("please", "")
    expr = expr.replace("?", "")
    expr = expr.strip()
    # Replace word forms with operator symbols (carefully)
    # handle phrases first to avoid partial replacements
    expr = expr.replace("divided by", "/")
    expr = expr.replace("multiplied by", "*")
    expr = expr.replace("times", "*")
    expr = expr.replace("multiply by", "*")
    expr = expr.replace("multiply", "*")
    expr = expr.replace("into", "*")          # indian style "12 into 5"
    expr = expr.replace("plus", "+")
    expr = expr.replace("add", "+")
    expr = expr.replace("minus", "-")
    expr = expr.replace("subtract", "-")
    expr = expr.replace("over", "/")         # "6 over 3" -> 6/3
    # Replace common multiplication symbols 'x' and '×' when they are used as operator.
    # Use regex with word boundaries so 'x' in words is not replaced.
    expr = re.sub(r'\b[x×]\b', '*', expr)
    # Now extract only numbers, decimal points, parentheses and allowed operators
    # This regex will keep numbers (including decimals and optional leading +/−) and operators
    tokens = re.findall(r'[-+]?\d+\.?\d*|\(|\)|[*/+\-]', expr)
    if not tokens:
        return "I could not understand the math problem."
    cleaned = "".join(tokens)
    # Extra safety: do not allow expressions that are just numbers glued without operators
    # (e.g., "12 5" -> tokens ['12','5'] -> cleaned '125' would be incorrect).
    # If two consecutive number tokens appear without an operator between them in the original text,
    # we treat that as an error.
    # Build a token-type list to check adjacency in the original token sequence:
    types = []
    for t in tokens:
        if re.fullmatch(r'[-+]?\d+\.?\d*', t):
            types.append('N')
        else:
            types.append('O')
    # If there are adjacent numbers without operator, that's probably a missing operator like '12 5' or '12x5' (if x not recognized).
    for i in range(len(types) - 1):
        if types[i] == 'N' and types[i+1] == 'N':
            # there were two numbers next to each other; fail safely
            return "I could not understand the math problem. Please say 'times' or 'multiply' between numbers."
    # Evaluate safely using AST
    try:
        result = _safe_eval(cleaned)
    except Exception:
        return "I could not calculate that."
    # Format result: show integer without .0
    if isinstance(result, float) and result.is_integer():
        result = int(result)
    return f"The answer is {result}"
