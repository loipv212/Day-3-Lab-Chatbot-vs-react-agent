# Individual Report: Lab 3 - Chatbot vs ReAct Agent

- **Student Name**: Nguyễn Trường Giang
- **Student ID**: 2A202600624
- **Date**: 2026-06-01
- **Team**: 16383

---

## I. Technical Contribution (15 Points)

Tôi phụ trách **Agent Core** — trái tim của hệ thống, là vòng lặp ReAct trong `src/agent/agent.py`.

- **Modules Implemented**:
  - `ReActAgent.run()` và `ReActAgent.run_iter()`: vòng lặp Thought–Action–Observation.
  - `_parse_action()`: bóc tách `Action: tool(arg)` bằng regex.
  - `_parse_final_answer()`, `_parse_thought()`: phát hiện điểm dừng và lý do suy luận.
  - `_execute_tool()`: ánh xạ tên tool → hàm Python thật, bắt lỗi tool không tồn tại.

- **Code Highlights**:
  ```python
  # Bóc tách action: lấy action CUỐI CÙNG nếu model viết nhiều dòng
  matches = re.findall(r"Action:\s*([a-zA-Z_]\w*)\s*\((.*?)\)", text, re.DOTALL)
  if not matches:
      return None
  tool_name, tool_arg = matches[-1]
  ```
  ```python
  # Bắt hallucination: tool không có trong registry
  available = ", ".join([t["name"] for t in self.tools])
  return f"Tool '{tool_name}' not found. Available tools: {available}."
  ```

- **Documentation**: LLM chỉ sinh *text* mô tả hành động; code của tôi mới là phần thực thi tool và đưa `Observation` trở lại scratchpad cho bước kế tiếp. Tôi cũng thêm `run_iter()` dạng generator để UI Streamlit hiển thị từng bước live.

---

## II. Debugging Case Study (10 Points)

- **Problem Description**: Ở câu 5 (`Buy 1 laptop and 1 headphones, apply coupon SALE20, ship to hanoi`), agent v1 **không dừng đúng lúc** và sinh 2 lỗi `PARSER_ERROR` ở bước 1 và 4.
- **Log Source** (`logs/2026-06-01.log`):
  ```json
  {"event": "AGENT_ERROR", "data": {"step": 1, "error_code": "PARSER_ERROR", "raw": "lookup_product_price(laptop)"}}
  {"event": "AGENT_ERROR", "data": {"step": 4, "error_code": "PARSER_ERROR", "raw": "The final total is $1110."}}
  ```
- **Diagnosis**: Regex của tôi yêu cầu tiền tố `Action:` và `Final Answer:`. Ở bước 1 model viết thẳng `lookup_product_price(laptop)` (thiếu `Action:`); ở bước 4 viết `The final total is $1110.` (thiếu `Final Answer:`). Đây là lỗi **format đầu ra của LLM**, không phải lỗi regex — nhưng code phải xử lý mềm dẻo.
- **Solution**: Tôi thêm nhánh "nudge": khi không parse được, agent chèn một `Observation` nhắc model trả lời đúng định dạng rồi tiếp tục vòng lặp thay vì crash. Nhờ đó agent tự phục hồi (bước 2 và 5 sau đó đúng format). Về lâu dài, phối hợp với prompt v2 (few-shot) để giảm tần suất lỗi này.

---

## III. Personal Insights: Chatbot vs ReAct (10 Points)

1. **Reasoning**: Khối `Thought` buộc model "nói ra" kế hoạch trước khi hành động, nhờ đó nó chia bài toán nhiều bước thành các bước nhỏ tra cứu được — điều Chatbot trả lời 1 phát không làm được.
2. **Reliability**: Agent đôi khi **tệ hơn** Chatbot ở câu cực đơn giản: tốn nhiều token/latency hơn (câu 1: agent gọi tool còn chatbot chỉ cần nói), và có thể lỗi parser. Với câu 1 bước, overhead của ReAct là không cần thiết.
3. **Observation**: Việc đưa kết quả tool thật (`iphone: $999`) trở lại prompt chính là thứ "neo" model vào sự thật. Khi model bỏ qua bước này và tự bịa Observation (câu 5), kết quả sai ngay.

---

## IV. Future Improvements (5 Points)

- **Scalability**: Thay parser regex bằng **native tool-calling** (function calling JSON schema) để loại bỏ hẳn lớp lỗi PARSER_ERROR.
- **Safety**: Thêm bộ kiểm tra "Observation phải do hệ thống tạo" — chặn mọi dòng Observation do model tự viết.
- **Performance**: Cache kết quả tool trong một câu hỏi để tránh gọi lại `lookup_product_price` nhiều lần.
