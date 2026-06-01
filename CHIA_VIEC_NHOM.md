# Phân Công Công Việc - Lab 3: Chatbot vs ReAct Agent

> Đề tài: **Trợ lý Mua sắm E-commerce** (xem `DE_TAI_1_ECOMMERCE.md`)
> Nhóm 5 người | Thời gian: 150 phút | Tổng điểm: 100 (Group 60 + Individual 40)

---

## 🎯 Mục tiêu nộp bài (Deliverable)

Cả nhóm phải nộp:
1. **Code chạy được**: Chatbot baseline + ReAct Agent (tối thiểu 2 tool) + telemetry.
2. **1 Group Report** chung (theo `report/group_report/TEMPLATE_GROUP_REPORT.md`).
3. **1 trace thành công + 1 trace lỗi** (lấy từ thư mục `logs/`).
4. **5 Individual Report** (mỗi người 1 file trong `report/individual_reports/`).
5. **Bonus** (tùy chọn): provider thứ 2 (Gemini), human-escalation, hoặc metrics nâng cao.

---

## 👥 Phân công 5 người

### 🟦 Người 1 — "Agent Core" (Trái tim hệ thống)
**Nhiệm vụ:** Hoàn thiện vòng lặp ReAct trong `src/agent/agent.py`
- [ ] Viết `get_system_prompt()`: format Thought / Action / Observation / Final Answer.
- [ ] Viết `run()`: vòng lặp gọi LLM → parse → gọi tool → nối Observation → lặp lại.
- [ ] Viết parser (regex) bóc tách `Action: tool_name(args)`.
- [ ] Viết `_execute_tool()`: gọi đúng hàm Python trong tool registry.
- [ ] Xử lý dừng: phát hiện "Final Answer" và giới hạn `max_steps`.

**Individual report:** case debug lỗi parser hoặc lặp vô hạn.

---

### 🟩 Người 2 — "Chatbot Baseline & Đánh giá"
**Nhiệm vụ:** Tạo baseline và phân tích so sánh
- [ ] Tạo file `src/chatbot.py`: chatbot gọi LLM 1 lần, KHÔNG có tool.
- [ ] Chạy chatbot trên bộ 5 câu test → ghi lại kết quả.
- [ ] Lập bảng so sánh Chatbot vs Agent (ai đúng, ai sai, câu nào).

**Individual report:** case chatbot bịa đáp án ở câu nhiều bước.

---

### 🟨 Người 3 — "Tools" (Bộ công cụ mua sắm)
**Nhiệm vụ:** Viết các tool e-commerce trong `src/tools/basic_tools.py`
- [ ] `get_discount(mã)` — tra % giảm giá theo mã.
- [ ] `calc_shipping(thành phố)` — tính phí ship theo địa điểm.
- [ ] (Tận dụng sẵn) `lookup_product_price` và `calculator` đã có trong code.
- [ ] (Bonus) `check_stock(sản phẩm)` — kiểm tra tồn kho.
- [ ] Viết mô tả tool rõ ràng + ví dụ cách gọi (rất quan trọng cho LLM).

**Individual report:** case agent chọn sai tool hoặc bịa tham số → sửa mô tả tool.

---

### 🟧 Người 4 — "Cải tiến v1 → v2" (Tối ưu hóa)
**Nhiệm vụ:** Phân tích log và nâng cấp agent
- [ ] Sau khi Agent v1 chạy & có log lỗi: phân tích các loại lỗi.
- [ ] Cải tiến system prompt (thêm few-shot, cấm markdown, ép Final Answer...).
- [ ] So sánh tỉ lệ thành công v1 vs v2 bằng số liệu.
- [ ] Ghi rõ: v1 sai gì → sửa gì → v2 cải thiện bao nhiêu %.

**Individual report:** case study chi tiết 1 lỗi được sửa từ v1 sang v2.

---

### 🟥 Người 5 — "Telemetry, Trace & Group Report"
**Nhiệm vụ:** Đo lường, thu trace, tổng hợp báo cáo
- [ ] Đảm bảo `tracker.track_request(...)` được gọi đúng chỗ (token, latency).
- [ ] Viết script đọc `logs/*.log` để tính: số bước, token, latency trung bình.
- [ ] Thu 1 trace thành công + 1 trace lỗi đẹp để nộp.
- [ ] Tổng hợp **Group Report** (gom dữ liệu từ tất cả thành viên).
- [ ] (Bonus) Thử provider Gemini, so sánh latency với OpenAI.

**Individual report:** phân tích metrics (token/latency) giữa các phiên bản.

---

## ⏱️ Thứ tự làm việc (150 phút)

| Giai đoạn | Thời gian | Ai làm gì |
| :--- | :--- | :--- |
| **0. Setup** | 0-15p | Cả nhóm: cài `requirements.txt`, copy `.env`, điền API key, clone repo. |
| **1. Dựng nền** | 15-60p | **Người 1** làm vòng lặp ReAct. **Người 3** viết tool. **Người 2** viết chatbot. |
| **2. Chạy thử & thu log** | 60-90p | Ghép code, chạy 5 câu test → thu `logs/` → tìm lỗi v1. **Người 5** lo telemetry. |
| **3. Cải tiến & đánh giá** | 90-120p | **Người 4** sửa v1→v2. **Người 2** làm bảng so sánh. **Người 5** thu trace. |
| **4. Viết report** | 120-150p | **Người 5** gom Group Report. Mỗi người viết Individual Report. |

> ⚠️ **Phụ thuộc quan trọng:** Người 1 (Agent) và Người 3 (Tools) phải xong sớm vì mọi thứ khác chờ chúng. Ưu tiên 2 người này trước.

---

## 🔗 Quy tắc Git (tránh đè code)

- Mỗi người làm trên **file riêng**:
  - Người 1 → `src/agent/agent.py`
  - Người 2 → `src/chatbot.py`
  - Người 3 → `src/tools/basic_tools.py`
  - Người 4 → system prompt (trong `agent.py`, phối hợp Người 1) + file ghi chú v1/v2
  - Người 5 → script eval, telemetry, report
- Mỗi người 1 nhánh riêng rồi merge. Commit thường xuyên.

---

## ✅ Checklist nghiệm thu (đối chiếu Rubric)

**Group (60đ):**
- [ ] Chatbot baseline + Agent ≥2 tool chạy được (16đ)
- [ ] Cải tiến v1 → v2 từ failure trace (12đ)
- [ ] Trace thành công + trace lỗi (12đ)
- [ ] So sánh Chatbot vs Agent bằng số liệu (12đ)
- [ ] Code sạch + telemetry tích hợp (8đ)

**Individual (40đ/người):**
- [ ] Đóng góp kỹ thuật rõ ràng (15đ)
- [ ] Case debug đọc từ log (15đ)
- [ ] Reflection chatbot vs agent (10đ)
