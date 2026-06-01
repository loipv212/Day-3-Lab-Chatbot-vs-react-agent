# 10 Đề Tài Gợi Ý - Lab 3: Chatbot vs ReAct Agent

> Nhóm chọn 1 đề tài thống nhất cho cả Chatbot baseline và ReAct Agent.
> Tiêu chí đề tốt: (1) cần nhiều bước → chatbot dễ fail, (2) dễ tự tính đáp án đúng để kiểm chứng, (3) tool đơn giản viết bằng dữ liệu giả.

---

| # | Đề tài | Các tool gợi ý | Câu hỏi test (nhiều bước) | Dễ làm | Nổi bật |
| :-- | :--- | :--- | :--- | :--: | :--: |
| 1 | 🛒 Trợ lý mua sắm E-commerce | `lookup_product_price`, `calculator`, `get_discount`, `calc_shipping` | "Mua 2 iPhone + 1 laptop, áp mã WINNER giảm 10%, ship Hà Nội. Tổng bao nhiêu?" | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| 2 | 🍔 Trợ lý đặt món nhà hàng | `get_menu_price`, `calculator`, `apply_combo`, `calc_service_charge` | "Đặt 3 phần gà rán + 2 coca, thêm 5% phí phục vụ. Tổng tiền?" | ⭐⭐⭐⭐ | ⭐⭐ |
| 3 | ✈️ Trợ lý đặt vé du lịch | `get_flight_price`, `get_hotel_price`, `calculator`, `convert_currency` | "Bay Đà Nẵng + ở 3 đêm khách sạn, đổi tổng ra VND." | ⭐⭐⭐ | ⭐⭐⭐ |
| 4 | 🏦 Trợ lý tài chính cá nhân | `get_salary`, `calc_tax`, `calculator`, `calc_savings` | "Lương 30 triệu, trừ thuế 10%, để dành 20% còn lại. Tiết kiệm bao nhiêu?" | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 5 | 🌡️ Trợ lý thời tiết + gợi ý | `get_weather`, `convert_temp`, `get_clothing_advice` | "Hà Nội bao nhiêu độ, đổi sang độ F, nên mặc gì?" | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| 6 | 🏥 Trợ lý y tế / nhà thuốc | `lookup_drug_price`, `check_dosage`, `calculator`, `check_interaction` | "Mua 2 hộp Paracetamol + 1 Vitamin C, kiểm tra liều cho người 30kg, tính tổng." | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 7 | 🎮 Trợ lý build PC / gaming | `get_component_price`, `check_compatibility`, `calculator`, `calc_power_usage` | "Build PC i5 + RAM 16GB + RTX 4060. Tổng tiền và công suất nguồn?" | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| 8 | 📚 Trợ lý đăng ký tín chỉ | `get_course_credits`, `get_tuition_per_credit`, `calculator`, `check_prerequisite` | "Đăng ký CS101, CS202, MATH301. Tổng tín chỉ và học phí?" | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 9 | 🏗️ Trợ lý báo giá xây dựng | `get_material_price`, `calc_area`, `calculator`, `calc_labor_cost` | "Lát gạch phòng 5x4m, gạch 200k/m², công 50k/m². Tổng chi phí?" | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| 10 | 🚚 Trợ lý logistics / giao hàng | `get_distance`, `calc_shipping_fee`, `calculator`, `estimate_delivery_time` | "Gửi 3 kiện 5kg từ HN đi HCM. Phí ship và thời gian giao?" | ⭐⭐⭐ | ⭐⭐⭐ |

---

## 💡 Gợi ý chọn nhanh

- **Muốn an toàn, làm nhanh trong 150 phút** → Đề **#1 (E-commerce)**: code đã có sẵn 2 tool, chỉ cần thêm 2 tool nữa.
- **Gần gũi sinh viên, dễ nghĩ test case** → Đề **#8 (Đăng ký tín chỉ)**.
- **Nổi bật, dễ ăn điểm bonus "guardrail/failure handling"** → Đề **#6 (Y tế)**: có bước kiểm tra an toàn (tương tác thuốc) → agent phải biết dừng và cảnh báo thay vì tính bừa.
- **Chuỗi tính toán phụ thuộc dài, làm chatbot fail rõ nhất** → Đề **#4 (Tài chính)** hoặc **#9 (Xây dựng)**.

---

## ✅ Sau khi chốt đề tài, nhóm cần làm:

1. Liệt kê 3-4 tool sẽ viết (tên + mô tả + dữ liệu giả).
2. Soạn 5 câu test: 2 câu đơn giản (1 bước) + 3 câu nhiều bước.
3. Tự tính sẵn đáp án đúng cho từng câu (để chấm đúng/sai).
4. Phân công theo file `CHIA_VIEC_NHOM.md`.
