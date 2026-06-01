"""
Streamlit UI for Lab 3: Chatbot vs ReAct Agent.

Run it with:
    streamlit run app.py

Features:
- Pick the LLM provider/model from the sidebar.
- Choose a mode: Chatbot, ReAct Agent, or Compare (side by side).
- Watch the agent's Thought -> Action -> Observation steps appear live.
- See token usage and latency for each run.
"""
import os
import time
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

from src.core.factory import create_provider
from src.core.openai_provider import OpenAIProvider
from src.core.gemini_provider import GeminiProvider
from src.chatbot import Chatbot
from src.agent.agent import ReActAgent
from src.tools import TOOL_REGISTRY


st.set_page_config(page_title="Chatbot vs ReAct Agent", page_icon="🤖", layout="wide")


# --------------------------------------------------------------------------
# Provider builder (respects sidebar selection, falls back to .env)
# --------------------------------------------------------------------------
def build_provider(provider_choice: str, model_name: str):
    provider_choice = provider_choice.lower()
    if provider_choice in ("router", "9router"):
        from src.core.router_provider import RouterProvider
        return RouterProvider(model_name=model_name or "cx/gpt-5.5")
    if provider_choice == "mimo":
        from src.core.mimo_provider import MiMoProvider
        return MiMoProvider(model_name=model_name or "mimo-v2.5-pro")
    if provider_choice in ("google", "gemini"):
        return GeminiProvider(model_name=model_name or "gemini-2.0-flash")
    if provider_choice == "openai":
        return OpenAIProvider(model_name=model_name or "gpt-4o")
    if provider_choice == "local":
        from src.core.local_provider import LocalProvider
        path = os.getenv("LOCAL_MODEL_PATH", "./models/Phi-3-mini-4k-instruct-q4.gguf")
        return LocalProvider(model_path=path)
    # default
    return create_provider()


# --------------------------------------------------------------------------
# Sidebar controls
# --------------------------------------------------------------------------
st.sidebar.title("⚙️ Cấu hình")

default_provider = os.getenv("DEFAULT_PROVIDER", "router")
provider_options = ["router", "mimo", "google", "openai", "local"]
provider_choice = st.sidebar.selectbox(
    "Provider",
    provider_options,
    index=provider_options.index(default_provider) if default_provider in provider_options else 0,
)

default_model_map = {
    "router": "cx/gpt-5.5",
    "mimo": "mimo-v2.5-pro",
    "google": "gemini-2.0-flash",
    "openai": "gpt-4o",
    "local": "phi-3",
}
model_name = st.sidebar.text_input("Model", value=default_model_map.get(provider_choice, ""))

max_steps = st.sidebar.slider("Max steps (agent)", min_value=3, max_value=12, value=8)

mode = st.sidebar.radio(
    "Chế độ",
    ["So sánh (Chatbot vs Agent)", "Chỉ Chatbot", "Chỉ ReAct Agent"],
)

st.sidebar.markdown("---")
st.sidebar.subheader("Câu hỏi mẫu")

SAMPLE_GROUPS = {
    "🟢 Đơn giản (1 bước)": [
        "Giá của macbook là bao nhiêu?",
        "Mã giảm giá BLACKFRIDAY được giảm bao nhiêu phần trăm?",
        "Sản phẩm pixel còn hàng không?",
        "Phí ship tới tokyo là bao nhiêu?",
    ],
    "🟡 Nhiều bước (agent thắng)": [
        "Tôi muốn mua 2 chiếc iphone. Tổng tiền là bao nhiêu?",
        "Mua 2 iphone và áp dụng mã WINNER (giảm 10%). Tổng tiền?",
        "Mua 1 laptop và 1 headphones, áp mã SALE20, ship tới hanoi. Tổng cuối cùng?",
        "Mua 1 macbook và 2 earbuds, áp mã BLACKFRIDAY, ship tới singapore. Tổng cuối cùng?",
        "Mua 3 smartwatch với mã VIP50 và ship tới danang. Tôi phải trả bao nhiêu?",
    ],
    "🔴 Bẫy / Edge case": [
        "Tôi muốn mua 1 con mouse. Còn hàng không và giá bao nhiêu?",
        "Mua 1 tablet và 1 monitor, ship tới bangkok. Tổng tiền? (tablet có thể đã hết hàng)",
        "Mua 2 laptop với mã FREESHIP ship tới tokyo. Tổng cuối cùng?",
        "Mua 1 iphone với mã FAKE123 ship tới sao hỏa. Tổng tiền?",
    ],
}

for group_name, questions in SAMPLE_GROUPS.items():
    with st.sidebar.expander(group_name):
        for q in questions:
            if st.button(q, key=f"sample_{q}", use_container_width=True):
                st.session_state["question"] = q

st.sidebar.markdown("---")
st.sidebar.caption("Tools khả dụng:")
for t in TOOL_REGISTRY:
    st.sidebar.caption(f"• `{t['name']}`")


# --------------------------------------------------------------------------
# Header
# --------------------------------------------------------------------------
st.title("🤖 Chatbot vs ReAct Agent")
st.caption("Lab 3 — Trợ lý mua sắm E-commerce. Xem agent gọi tool từng bước.")

question = st.text_input(
    "Nhập câu hỏi:",
    value=st.session_state.get("question", "Mua 1 laptop và 1 headphones, áp mã SALE20, ship tới hanoi. Tổng cuối cùng?"),
    key="question",
)

run_btn = st.button("🚀 Chạy", type="primary", use_container_width=True)


# --------------------------------------------------------------------------
# Rendering helpers
# --------------------------------------------------------------------------
def render_chatbot(container, provider, q):
    with container:
        st.subheader("💬 Chatbot (baseline)")
        st.caption("Gọi LLM 1 lần, không có tool.")
        with st.spinner("Chatbot đang trả lời..."):
            start = time.time()
            bot = Chatbot(provider)
            answer = bot.run(q)
            elapsed = int((time.time() - start) * 1000)
        st.success("Hoàn tất")
        st.markdown("**Trả lời:**")
        st.write(answer)
        st.caption(f"⏱️ {elapsed} ms")


def render_agent(container, provider, q, max_steps):
    with container:
        st.subheader("🧠 ReAct Agent")
        st.caption("Vòng lặp Thought → Action → Observation.")
        agent = ReActAgent(provider, TOOL_REGISTRY, max_steps=max_steps)

        total_tokens = 0
        total_latency = 0
        final_answer = None
        step_area = st.container()

        with st.spinner("Agent đang suy luận..."):
            for ev in agent.run_iter(q):
                total_tokens += ev.get("usage", {}).get("total_tokens", 0)
                total_latency += ev.get("latency_ms", 0)

                if ev["type"] == "thought_action":
                    with step_area:
                        with st.chat_message("assistant", avatar="🧠"):
                            st.markdown(f"**Bước {ev['step']} — Thought**")
                            if ev.get("thought"):
                                st.write(ev["thought"])
                            st.markdown(f"➡️ **Action:** `{ev['tool']}({ev['arg']})`")

                elif ev["type"] == "tool_call":
                    with step_area:
                        with st.chat_message("user", avatar="🔧"):
                            st.markdown(f"**Observation (bước {ev['step']})**")
                            st.code(ev["observation"], language="text")

                elif ev["type"] == "parser_error":
                    with step_area:
                        st.warning(f"⚠️ Bước {ev['step']}: PARSER_ERROR — LLM không xuất đúng `Action:` hoặc `Final Answer:`.")
                        with st.expander("Xem output thô"):
                            st.code(ev["raw"], language="text")

                elif ev["type"] == "final":
                    final_answer = ev["answer"]

                elif ev["type"] == "timeout":
                    st.error(f"⛔ Vượt quá {max_steps} bước mà chưa có Final Answer.")

        if final_answer is not None:
            st.success("✅ Final Answer")
            st.markdown(f"### {final_answer}")
        st.caption(f"🔢 Tổng token: {total_tokens}  |  ⏱️ Tổng latency: {total_latency} ms")


# --------------------------------------------------------------------------
# Main action
# --------------------------------------------------------------------------
if run_btn and question.strip():
    try:
        provider = build_provider(provider_choice, model_name)
    except Exception as exc:
        st.error(f"Không khởi tạo được provider '{provider_choice}': {exc}")
        st.stop()

    if mode == "So sánh (Chatbot vs Agent)":
        col1, col2 = st.columns(2)
        render_chatbot(col1, provider, question)
        render_agent(col2, provider, question, max_steps)
    elif mode == "Chỉ Chatbot":
        render_chatbot(st.container(), provider, question)
    else:
        render_agent(st.container(), provider, question, max_steps)
elif run_btn:
    st.warning("Hãy nhập câu hỏi trước khi chạy.")
