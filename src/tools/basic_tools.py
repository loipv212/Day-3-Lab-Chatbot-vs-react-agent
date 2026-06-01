def calculator(expression: str) -> str:
    allowed_chars = set("0123456789+-*/(). ")
    if not expression or any(char not in allowed_chars for char in expression):
        return "Invalid expression. Only numbers and basic math operators are allowed."

    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as exc:
        return f"Calculation error: {exc}"


def lookup_product_price(product_name: str) -> str:
    prices = {
        "iphone": 999,
        "laptop": 1200,
        "headphones": 150,
        "keyboard": 80,
    }
    key = product_name.strip().lower()
    if key not in prices:
        return f"No price found for {product_name}."
    return f"{product_name}: ${prices[key]}"


TOOL_REGISTRY = [
    {
        "name": "calculator",
        "description": "Run basic arithmetic. Input should be a math expression string, for example: calculator(2 * 999 + 10).",
        "function": calculator,
    },
    {
        "name": "lookup_product_price",
        "description": "Look up a sample product price. Input should be a product name, for example: lookup_product_price(iPhone).",
        "function": lookup_product_price,
    },
]
