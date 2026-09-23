# 🤖 AI Usage — GPA Tracker

> Tài liệu này khai báo trung thực việc sử dụng AI trong quá trình làm dự án,
> theo yêu cầu của Python Journey Capstone Project.

---

## 📌 Công cụ AI đã dùng

| Công cụ | Mục đích |
|---------|----------|
| Claude (Anthropic) | Hướng dẫn từng bước, giải thích khái niệm |
| Gemini (Google) | Review code, phát hiện lỗi tiềm ẩn |

---

## 1️⃣ Tôi đã dùng AI cho những việc gì?

### 🗂️ Thiết kế & Cấu trúc
- Gợi ý cấu trúc thư mục dự án
- Giải thích lý do tách `grading.py` khỏi `main.py`

### 📚 Giải thích khái niệm
- Sự khác nhau giữa `tuple` và `list`
- Tại sao dùng `.get()` thay vì `[]` khi truy cập dict
- `monkeypatch` và `tmp_path` trong pytest là gì
- Cách đọc traceback từ dưới lên để tìm lỗi

### 🔍 Review & Kiểm tra
- Gemini review hàm `calculate_gpa`, phát hiện thiếu `.get()`
- Hướng dẫn cách đọc và xử lý lỗi `IndentationError`, `KeyError`, `NameError`

---

## 2️⃣ Tôi đã tự viết hoặc thay đổi phần nào?

### ✍️ Tự gõ tay
- Toàn bộ code trong `grading.py`, `storage.py`, `main.py`, `test_grading.py`
- Không copy-paste bất kỳ đoạn code nào nguyên trạng

### 🐛 Tự phát hiện và sửa lỗi
| Lỗi | Nguyên nhân | Cách sửa |
|-----|-------------|----------|
| `IndentationError` | Quên gõ `assert` trong hàm test | Thêm dòng `assert` |
| `NameError: CLASSIFICATION_TABLE` | Bảng bị thụt vào trong hàm khác | Dùng `Shift+Tab` đưa ra ngoài |
| `KeyError: final-score` | Gõ nhầm `-` thay vì `_` | Sửa thành `final_score` |
| `fixture 'monkeypath' not found` | Gõ thiếu chữ `c` | Sửa thành `monkeypatch` |
| Thiếu 3 dòng cộng dồn | Quên gõ trong vòng `for` | Thêm `total_credits +=`, `weighted_10 +=`, `weighted_4 +=` |

### 🔧 Tự quyết định thiết kế
- Thêm trường `semester` để nhóm môn theo học kỳ
- Quyết định **không** dùng đề xuất tích hợp "Jev AI" vì không phù hợp với tinh thần đề bài và không thể giải thích được toàn bộ code

---

## 3️⃣ Tôi kiểm chứng câu trả lời của AI bằng cách nào?

### 📊 Kiểm chứng bằng dữ liệu thật
Đối chiếu kết quả chương trình với bảng điểm thật từ hệ thống của trường:

```
GPA kỳ 1:      7.77 / 3.06  ✅ Khớp
GPA kỳ 2:      6.82 / 2.25  ✅ Khớp
GPA tích lũy:  7.27 / 2.63  ✅ Khớp
```

### ❌ Giả thuyết AI bị bác bỏ
Hai giả thuyết AI đề xuất đã bị bác bỏ bởi dữ liệu thật:

1. **"Hệ 4 = Hệ 10 × 0.4"** → Sai. 6.70 × 0.4 = 2.68, nhưng trường cho 2.00 (C)
2. **Bảng 8 mức (A/B+/B/C+/C/D+/D/F)"** → Sai. Trường chỉ dùng 5 mức (A/B/C/D/F)

### 🧪 Kiểm chứng bằng test
19 test cases chạy pass, bao gồm các trường hợp biên và dữ liệu thật.

---

## 💡 Bài học rút ra

> *"AI là công cụ hỗ trợ, không phải người làm thay. Mọi câu trả lời của AI đều cần kiểm chứng bằng dữ liệu thật hoặc chạy thử."*

- Dùng AI để **hiểu** khái niệm, không phải để **có** code
- Dữ liệu thật (bảng điểm thực tế) là bộ test tốt nhất
- Tự gõ code giúp phát hiện lỗi và hiểu sâu hơn copy-paste
