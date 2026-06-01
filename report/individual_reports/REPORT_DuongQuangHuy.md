# Individual Report: Lab 3 - Chatbot vs ReAct Agent

- **Student Name**: Dương Quang Huy
- **Student ID**: 2A202600839
- **Date**: 2026-06-01
- **Team**: 16383

---

## I. Technical Contribution (15 Points)

Tôi phụ trách **cải tiến Prompt v1 → v2** dựa trên failure trace, là hạng mục trọng tâm của lab.

- **Modules Implemented**:
  - Viết lại `ReActAgent.get_system_prompt()` từ v1 (khuyến khích dùng tool) sang v2 (bắt buộc dùng tool + cấm tự viết Observation + few-shot example).
  - Thiết kế quy trình "đọc log → xác định lỗi → sửa prompt → đo lại".

- **Code Highlights** (các rule then chốt của v2):
  ```
  2. NEVER do arithmetic in your head. EVERY calculation MUST go through calculator.
  5. To get any shipping fee, you MUST call calc_shipping. Never guess the shipping cost.
  7. Provide exactly ONE Action per step ... Do NOT write your own Observation.
  ```
  Kèm 1 few-shot example multi-step (mua 2 keyboard + WINNER + ship hcm) để model bắt chước đúng định dạng.

- **Documentation**: Mỗi thay đổi trong v2 đều gắn với một lỗi cụ thể quan sát được trong `logs/2026-06-01.log`, không sửa theo cảm tính.

---

## II. Debugging Case Study (10 Points)

- **Problem Description**: Câu 5, agent v1 ra **$1090** thay vì **$1085** (đáp án đúng).
- **Log Source** (`logs/2026-06-01.log`, bước 6):
  ```json
  {"event": "AGENT_STEP", "data": {"step": 6, "llm_output": "Observation: hanoi: $10\nThought: ... Shipping to Hanoi: $10. Final total: $1090 ..."}}
  ```
- **Diagnosis**: Đây là **HALLUCINATION**. Model **tự bịa** dòng `Observation: hanoi: $10` thay vì gọi tool `calc_shipping(hanoi)` (giá trị thật = $5). Vì prompt v1 không bắt buộc dùng `calc_shipping` và không cấm tự viết Observation, model lấy ship = $10 trong "trí nhớ" → sai $5 → kết quả lệch.
- **Solution (v2)**: Thêm rule "you MUST call calc_shipping" và "Do NOT write your own Observation", cộng few-shot có bước `calc_shipping(hcm) → $7`. Kỳ vọng: agent gọi đúng tool ship → ra $5 → tổng đúng **$1085**. (Số liệu định lượng v2 sẽ cập nhật sau khi chạy lại `python main.py agent`.)

---

## III. Personal Insights: Chatbot vs ReAct (10 Points)

1. **Reasoning**: `Thought` giúp tôi *nhìn thấy* lý do model sai — nó "nghĩ" ship là $10. Với Chatbot, lỗi nằm trong hộp đen, không truy được.
2. **Reliability**: Agent v1 có thể đúng nhờ may (câu 4) hoặc sai do hallucinate (câu 5). Prompt là đòn bẩy rẻ nhất để tăng độ tin cậy mà không đổi model.
3. **Observation**: Bài học lớn nhất: **Observation phải đến từ môi trường thật**. Khoảnh khắc model tự viết Observation là khoảnh khắc nó rời khỏi sự thật.

---

## IV. Future Improvements (5 Points)

- **Scalability**: Tạo bộ "regression prompt test" — mỗi lần đổi prompt, chạy lại 5 câu và so success rate tự động.
- **Safety**: Thêm lớp hậu kiểm: nếu Final Answer chứa số không khớp với chuỗi Observation đã thu, đánh cờ cảnh báo.
- **Performance**: Thử rút gọn few-shot để giảm prompt_tokens trong khi vẫn giữ độ chính xác (cân bằng cost vs accuracy).
