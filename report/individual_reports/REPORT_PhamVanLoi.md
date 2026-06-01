# Individual Report: Lab 3 - Chatbot vs ReAct Agent

- **Student Name**: Phạm Văn Lợi
- **Student ID**: 2A202600784
- **Date**: 2026-06-01
- **Team**: 16383

---

## I. Technical Contribution (15 Points)

Tôi phụ trách **Chatbot baseline & phần Đánh giá so sánh**.

- **Modules Implemented**:
  - `src/chatbot.py`: lớp `Chatbot` gọi LLM đúng 1 lần, không tool, để làm mốc so sánh.
  - Bộ 5 test case trong `main.py` (`TEST_CASES`) kèm đáp án đúng (ground truth) để chấm.
  - Bổ sung test offline trong `tests/test_logic.py` cho các case dễ gây lỗi: sản phẩm số nhiều, địa điểm không hỗ trợ, địa danh tiếng Việt có dấu, và agent trả `Final Answer` quá sớm khi chưa gọi tool.
  - Bảng so sánh Chatbot vs Agent dùng số liệu thật từ log.

- **Code Highlights**:
  ```python
  class Chatbot:
      SYSTEM_PROMPT = ("You are a helpful shopping assistant. "
                       "Answer the user's question directly and concisely.")
      def run(self, user_input: str) -> str:
          result = self.llm.generate(user_input, system_prompt=self.SYSTEM_PROMPT)
          tracker.track_request(provider=result.get("provider"), model=self.llm.model_name,
                                usage=result.get("usage", {}), latency_ms=result.get("latency_ms", 0))
          return result["content"]
  ```

- **Documentation**: Chatbot cố tình "ngây thơ" (1 lượt, không tool) để chứng minh giới hạn của LLM thuần khi gặp câu nhiều bước; cùng đi qua `tracker` để telemetry công bằng giữa 2 phiên bản.

---

## II. Debugging Case Study (10 Points)

- **Problem Description**: Chatbot **bịa giá** ở câu 4 (`Buy 2 iphones and apply coupon WINNER (10% off)`). Nó tự giả định iPhone giá $799 rồi tính ra tổng $1,438.20 — sai so với đáp án đúng $1,798.20.
- **Log Source** (`logs/2026-06-01.log`):
  ```json
  {"event": "CHATBOT_END", "data": {"answer": "Assuming each iPhone costs $799 ... Final total: $1,438.20 ..."}}
  ```
- **Diagnosis**: Chatbot không có quyền truy cập catalog giá thật (`lookup_product_price`). Khi thiếu dữ liệu, model **lấp chỗ trống bằng kiến thức huấn luyện** ($799 là giá iPhone base phổ biến) — đây là hallucination kinh điển. Câu 5 thì ngược lại: model **từ chối** và hỏi lại giá vì câu phức tạp hơn.
- **Solution**: Đây là giới hạn cố hữu của Chatbot, không "sửa" được bằng prompt. Bài học: với bài toán cần dữ liệu thật, phải dùng Agent + tool. Tôi dùng chính case này làm bằng chứng định lượng cho phần so sánh.

---

## III. Personal Insights: Chatbot vs ReAct (10 Points)

1. **Reasoning**: Chatbot trả lời ngay nên không có cơ hội "dừng lại tra cứu". Agent nhờ `Thought` mà biết mình thiếu dữ liệu gì và đi lấy.
2. **Reliability**: Chatbot **nhanh và rẻ hơn** ở câu hỏi kiến thức chung, nhưng với câu cần số liệu thật thì độ tin cậy gần như bằng 0 (0/5 trong test của nhóm). Agent chậm/đắt hơn nhưng đúng 4/5.
3. **Observation**: Điểm khác biệt cốt lõi là Chatbot không có vòng phản hồi từ môi trường; nó không bao giờ "biết" giá iPhone trong catalog là $999.

---

## IV. Future Improvements (5 Points)

- **Scalability**: Tự động hóa chấm điểm — so khớp số trong Final Answer với đáp án đúng để tính success rate không cần đọc tay.
- **Safety**: Nâng guardrail từ prompt/regex lên native tool-calling hoặc JSON schema để model không thể tự viết `Observation` hay trả `Final Answer` khi chưa gọi tool bắt buộc.
- **Robustness**: Mở rộng bộ test "đánh lừa" hiện có với nhiều input tự nhiên hơn: tên sản phẩm số nhiều, địa danh viết tắt, coupon sai, sản phẩm hết hàng, và địa điểm không hỗ trợ giao hàng.
- **Performance**: Thêm cột đo "đúng/sai theo từng loại câu" (1 bước vs nhiều bước) và chạy lại cùng seed/provider để so sánh ổn định hơn giữa Chatbot và Agent.
