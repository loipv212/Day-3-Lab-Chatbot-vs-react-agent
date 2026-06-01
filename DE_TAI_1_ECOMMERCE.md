# Đề Tài 1: Trợ Lý Mua Sắm E-commerce (Smart Shopping Assistant)

> Lab 3: Chatbot vs ReAct Agent | Nhóm 5 người | 150 phút

---

## 1. Ứng dụng thực tế (để nhóm hiểu "tại sao làm cái này")

Đây là phiên bản thu nhỏ của các trợ lý mua sắm thật như **Shopee Assistant, Amazon Rufus, Lazada chatbot**. Trong thực tế, các trợ lý này:
- Tra giá sản phẩm **thật** từ database (không bịa).
- Kiểm tra tồn kho, áp mã giảm giá, tính phí ship theo địa chỉ.
- Tổng hợp lại thành 1 câu trả lời chính xác cho khách.

Bài lab thay API thật bằng **tool giả** để học cơ chế. Hiểu xong, ráp vào API thật là thành sản phẩm thương mại.

**Vì sao chatbot thường KHÔNG làm được?** Vì nó không có dữ liệu giá thật → nó đoán → sai. Agent thì gọi tool lấy số thật → đúng.

---

## 2. Ý tưởng đề tài

Trợ lý giúp khách hàng tính **tổng tiền đơn hàng**: tra giá sản phẩm, nhân số lượng, áp mã giảm giá, cộng phí ship. Đây là chuỗi nhiều bước phụ thuộc nhau → làm nổi bật sự khác biệt Chatbot vs Agent.

---

## 3. Danh sách Tool (4 tool)

| Tool | Input | Output | Mô tả |
| :--- | :--- | :--- | :--- |
| `lookup_product_price` | tên sản phẩm | giá (USD) | Tra giá sản phẩm (ĐÃ CÓ SẴN trong code) |
| `calculator` | biểu thức toán | kết quả | Tính toán số học (ĐÃ CÓ SẴN) |
| `get_discount` | mã giảm giá | % giảm | Tra phần trăm giảm theo mã (nhóm tự thêm) |
| `calc_shipping` | nơi đến / cân nặng | phí ship | Tính phí vận chuyển (nhóm tự thêm) |

### Dữ liệu giả gợi ý

```python
# Giá sản phẩm (ĐÃ CÓ SẴN trong basic_tools.py)
PRICES = {
    "iphone": 999,
    "laptop": 1200,
    "headphones": 150,
    "keyboard": 80,
}

# Mã giảm giá (nhóm tự thêm)
DISCOUNTS = {
    "WINNER": 10,   # giảm 10%
    "SALE20": 20,   # giảm 20%
    "VIP50":  50,   # giảm 50%
}

# Phí ship theo thành phố (USD) (nhóm tự thêm)
SHIPPING = {
    "hanoi": 5,
    "hcm": 7,
    "danang": 6,
}
```

---

## 4. Bộ câu test (5 câu)

### Câu đơn giản (1 bước) — chatbot làm được
1. "Giá của iPhone là bao nhiêu?" → **Đáp án: $999**
2. "Mã WINNER giảm bao nhiêu %?" → **Đáp án: 10%**

### Câu nhiều bước (chatbot dễ fail) — agent thắng
3. "Mua 2 iPhone, tổng tiền bao nhiêu?"
   - Bước 1: giá iphone = 999
   - Bước 2: 999 × 2 = **$1998**

4. "Mua 2 iPhone, áp mã WINNER (giảm 10%). Tổng bao nhiêu?"
   - Bước 1: 999 × 2 = 1998
   - Bước 2: giảm 10% → 1998 × 0.9 = **$1798.2**

5. "Mua 1 laptop + 1 headphones, áp mã SALE20, ship Hà Nội. Tổng cuối cùng?"
   - Bước 1: 1200 + 150 = 1350
   - Bước 2: giảm 20% → 1350 × 0.8 = 1080
   - Bước 3: cộng ship Hà Nội $5 → **$1085**

> ⚠️ Nhóm tự tính sẵn đáp án từng câu để chấm đúng/sai khi chạy.

---

## 5. Ví dụ vòng lặp ReAct (câu số 5)

```
User: Mua 1 laptop + 1 headphones, áp mã SALE20, ship Hà Nội. Tổng cuối?

Thought: Cần biết giá laptop và headphones.
Action: lookup_product_price(laptop)
Observation: laptop: $1200

Thought: Giờ tra giá headphones.
Action: lookup_product_price(headphones)
Observation: headphones: $150

Thought: Tổng tạm = 1200 + 150.
Action: calculator(1200 + 150)
Observation: 1350

Thought: Mã SALE20 giảm bao nhiêu?
Action: get_discount(SALE20)
Observation: 20

Thought: Giảm 20% → 1350 * 0.8.
Action: calculator(1350 * 0.8)
Observation: 1080

Thought: Cộng phí ship Hà Nội.
Action: calc_shipping(hanoi)
Observation: 5

Thought: Tổng cuối = 1080 + 5.
Action: calculator(1080 + 5)
Observation: 1085

Thought: Đã đủ thông tin.
Final Answer: Tổng tiền cuối cùng là $1085.
```

So với **Chatbot** (không tool): nó sẽ đoán "khoảng $1000-1100" hoặc quên trừ giảm giá / quên cộng ship → đây là điểm fail để đưa vào bảng so sánh.

---

## 6. Lý do đề tài này dễ làm + ăn điểm

- **Code đã có sẵn 2/4 tool** (`lookup_product_price`, `calculator`) → tiết kiệm thời gian.
- Đúng gợi ý của đề bài (Instructor Guide nhắc tới "E-commerce Assistant").
- Chuỗi nhiều bước rõ ràng → chatbot fail dễ thấy → bảng so sánh đẹp.
- Dễ tự tính tay để kiểm chứng đáp án.
