"""
Offline tests (no API key needed) for tools + agent parsing logic.
Run: python tests/test_logic.py
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.tools.basic_tools import (
    calculator,
    get_discount,
    calc_shipping,
    lookup_product_price,
    check_stock,
    get_product_weight,
)
from src.tools import TOOL_REGISTRY
from src.agent.agent import ReActAgent


class FakeLLM:
    model_name = "fake"

    def __init__(self, outputs):
        self.outputs = list(outputs)

    def generate(self, prompt, system_prompt=None):
        content = self.outputs.pop(0)
        return {
            "content": content,
            "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
            "latency_ms": 0,
            "provider": "fake",
        }


def test_tools():
    print("--- TOOLS ---")
    print("price iphone   :", lookup_product_price("iphone"))
    print("discount WINNER:", get_discount("WINNER"))
    print("ship hanoi     :", calc_shipping("hanoi"))
    print("calc 1998*0.9  :", calculator("1998 * 0.9"))
    assert lookup_product_price("iphone") == "iphone: $999"
    assert get_discount("WINNER") == "WINNER: 10% off"
    assert calc_shipping("hanoi") == "Shipping to hanoi: $5"
    assert calculator("999 * 2") == "1998"
    # New dataset entries
    assert lookup_product_price("macbook") == "macbook: $1999"
    assert get_discount("BLACKFRIDAY") == "BLACKFRIDAY: 30% off"
    assert calc_shipping("tokyo") == "Shipping to tokyo: $25"
    assert "UNSUPPORTED_DESTINATION" in calc_shipping("sao hỏa")
    assert "Default fee" not in calc_shipping("sao hỏa")
    assert lookup_product_price("2 iphones") == "iphone: $999"
    assert check_stock(" MICE ") == "mouse: OUT OF STOCK (0 units)."
    assert get_product_weight("laptops") == "laptop: 2.0 kg"
    assert calc_shipping("Hà Nội") == "Shipping to hanoi: $5"
    assert calc_shipping("Ho Chi Minh City") == "Shipping to hcm: $7"
    assert calc_shipping("Đà Nẵng") == "Shipping to danang: $6"
    assert calculator("   ") == "Invalid expression. Only numbers and basic math operators are allowed."


def test_parser():
    print("\n--- PARSER ---")
    # We pass llm=None because parsing helpers don't need the LLM.
    agent = ReActAgent(llm=None, tools=TOOL_REGISTRY)

    # 1. Normal action
    name, arg = agent._parse_action("Thought: need price.\nAction: lookup_product_price(iphone)")
    print("parsed action:", name, "|", arg)
    assert name == "lookup_product_price" and arg == "iphone"

    # 2. Action with math expression
    name, arg = agent._parse_action("Action: calculator(999 * 2)")
    assert name == "calculator" and arg == "999 * 2"

    # 3. Final answer detection
    final = agent._parse_final_answer("Thought: done.\nFinal Answer: The total is $1998.")
    print("parsed final :", final)
    assert final == "The total is $1998."

    # 4. No action present
    assert agent._parse_action("Thought: hmm, I am thinking.") is None

    # 5. Tool execution via registry
    obs = agent._execute_tool("calculator", "1200 + 150")
    print("exec tool     :", obs)
    assert obs == "1350"

    # 6. Hallucinated tool
    obs = agent._execute_tool("search_google", "iphone")
    print("hallucination :", obs)
    assert "not found" in obs


def test_agent_rejects_premature_final_answer():
    print("\n--- PREMATURE FINAL GUARD ---")
    llm = FakeLLM([
        "Final Answer: Mouse is in stock and costs $25.",
        "Thought: I need the mouse stock.\nAction: check_stock(mouse)",
        "Thought: I need the mouse price.\nAction: lookup_product_price(mouse)",
        "Thought: I now know the final answer.\nFinal Answer: Mouse is out of stock and costs $40.",
    ])
    agent = ReActAgent(llm=llm, tools=TOOL_REGISTRY, max_steps=5)
    answer = agent.run("Tôi muốn mua 1 con mouse. Còn hàng không và giá bao nhiêu?")
    print("guarded answer:", answer)
    assert answer == "Mouse is out of stock and costs $40."


if __name__ == "__main__":
    test_tools()
    test_parser()
    test_agent_rejects_premature_final_answer()
    print("\nAll offline tests PASSED.")
