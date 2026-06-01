# Hướng Dẫn Chạy - Lab 3: Chatbot vs ReAct Agent (Nhóm 16383)

Trợ lý mua sắm E-commerce: so sánh **Chatbot baseline** và **ReAct Agent** kèm telemetry. Hỗ trợ nhiều provider (9router/`cx/gpt-5.5`, MiMo, Gemini) và giao diện web Streamlit.

---

## 1. Yêu cầu

- **Python 3.10+** (đã test trên 3.12).
- API key cho ít nhất 1 provider (xem mục 3).
- (Tuỳ chọn) Nếu dùng `cx/gpt-5.5`: cài và chạy **9router** local (mở cổng `localhost:20128`).

---

## 2. Cài đặt

```cmd
:: (Khuyến nghị) tạo môi trường ảo riêng
python -m venv venv
venv\Scripts\activate

:: Cài thư viện
pip install -r requirements.txt
```

---

## 3. Cấu hình API key (.env)

Tạo file `.env` từ mẫu:

```cmd
copy .env.example .env
```

Mở `.env` và điền key cho provider muốn dùng. Có thể dán **nhiều key** cách nhau bằng dấu phẩy để hệ thống **tự xoay vòng** khi gặp rate limit.

Chọn 1 trong các cấu hình dưới đây:

### Cách A — 9router + cx/gpt-5.5 (provider chính của nhóm)
> Cần chạy app 9router trước (cổng 20128).
```env
ROUTER_API_KEYS=sk-key1,sk-key2
ROUTER_BASE_URL=http://localhost:20128/v1
DEFAULT_PROVIDER=router
DEFAULT_MODEL=cx/gpt-5.5
```

### Cách B — MiMo (Xiaomi)
```env
MIMO_API_KEYS=tp-key1,tp-key2
MIMO_BASE_URL=https://token-plan-sgp.xiaomimimo.com/v1
DEFAULT_PROVIDER=mimo
DEFAULT_MODEL=mimo-v2.5-pro
```

### Cách C — Gemini (cần key chuẩn dạng AIza...)
```env
GEMINI_API_KEYS=AIza...
DEFAULT_PROVIDER=google
DEFAULT_MODEL=gemini-2.0-flash
```

> ⚠️ `.env` đã được `.gitignore` — không commit key lên git.

---

## 4. Chạy giao diện web (khuyến nghị)

```cmd
streamlit run app.py
```

Mở trình duyệt: **http://localhost:8501**

Trong UI:
- **Sidebar**: chọn Provider, Model, Chế độ (⚖️ So sánh / 💬 Chatbot / 🧠 Agent), Max steps.
- Nhập câu hỏi hoặc bấm **câu hỏi mẫu**.
- Agent hiển thị từng bước **Thought → Action → Observation** (gấp trong expander), kèm token & latency.

---

## 5. Chạy bằng dòng lệnh (CLI)

```cmd
:: Chạy cả Chatbot + Agent trên 5 test case có sẵn
python main.py

:: Chỉ chạy chatbot / chỉ chạy agent
python main.py chatbot
python main.py agent

:: Hỏi 1 câu tùy ý
python main.py "Mua 2 iphone áp mã WINNER, ship tới hanoi. Tổng?"
```

Mọi lượt chạy ghi log JSON vào `logs/<ngày>.log`.

---

## 6. Chạy test (không cần API key)

```cmd
:: Test logic tool + parser của agent (offline)
python tests\test_logic.py
```

---

## 7. Cấu trúc dự án

```
.
├── app.py                      # Giao diện web Streamlit
├── main.py                     # Runner CLI (5 test case)
├── requirements.txt
├── .env                        # API key (không commit)
├── src/
│   ├── agent/agent.py          # Vòng lặp ReAct (Thought-Action-Observation)
│   ├── chatbot.py              # Chatbot baseline (1 lần gọi, không tool)
│   ├── core/                   # Các provider + factory + key rotation
│   │   ├── llm_provider.py     # Lớp abstract
│   │   ├── router_provider.py  # 9router (cx/gpt-5.5)
│   │   ├── mimo_provider.py    # MiMo
│   │   ├── gemini_provider.py  # Gemini
│   │   ├── openai_provider.py  # OpenAI
│   │   ├── local_provider.py   # Model local (GGUF)
│   │   ├── factory.py          # Tạo provider theo .env
│   │   └── key_manager.py      # Xoay vòng nhiều API key
│   ├── tools/basic_tools.py    # 6 tool e-commerce + dataset
│   └── telemetry/              # logger (JSON) + metrics (token/latency/cost)
├── logs/                       # Log telemetry (auto tạo)
├── tests/                      # test_logic, smoke_router, test_local
└── report/
    ├── group_report/GROUP_REPORT_16383.md
    └── individual_reports/REPORT_*.md
```

---

## 8. Đổi provider để demo (cho rubric)

Chỉ cần sửa `DEFAULT_PROVIDER` và `DEFAULT_MODEL` trong `.env` (router | mimo | google | openai | local), hoặc đổi trực tiếp trong sidebar UI. Không cần sửa code.

---

## 9. Xử lý sự cố thường gặp

| Triệu chứng | Nguyên nhân & cách xử lý |
| :--- | :--- |
| `All router API keys exhausted` | 9router chưa chạy / sai cổng. Kiểm tra `localhost:20128`. |
| `429 quota exceeded, limit: 0` | Key không có quota free tier. Dùng key/provider khác. |
| `404 model ... not found` | Tên model sai. Đổi `DEFAULT_MODEL` cho đúng provider. |
| Latency rất cao (>30s) | Model sinh nhiều token. Chọn model flash hoặc giảm max_steps. |
| UI không cập nhật | Refresh trình duyệt; Streamlit tự reload khi sửa file. |

---

> Demo nhanh: `streamlit run app.py` → chọn chế độ **⚖️ So sánh** → bấm câu mẫu 🟡 "Mua 1 laptop và 1 headphones, áp mã SALE20, ship tới hanoi" để thấy Chatbot vs Agent.
