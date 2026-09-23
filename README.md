<div align="center">

![banner](./banner.svg)

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python&logoColor=white)
![Pytest](https://img.shields.io/badge/Tests-19%20passed-brightgreen?logo=pytest&logoColor=white)
![Status](https://img.shields.io/badge/Status-Complete-success?logo=checkmarx)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Platform](https://img.shields.io/badge/Platform-Terminal-lightgrey?logo=windows-terminal)

**Chương trình tính GPA theo đúng quy tắc của Trường Cao đẳng Công Thương TP.HCM (HITC)**

*Chạy trên terminal · Lưu dữ liệu bằng JSON · Kiểm chứng từ bảng điểm thật*

</div>

---

## 🎯 Vấn đề

Sinh viên HITC thường tính GPA bằng tay hoặc Excel, dễ nhầm ở các mốc biên:

> *"6.9 hay 7.0 thì khác điểm chữ không?"*  
> *"Cuối kỳ cần bao nhiêu điểm để GPA lên Khá?"*

Chương trình này giải quyết đúng hai câu hỏi đó, theo đúng công thức của trường.

---

## ✨ Chức năng

| # | Chức năng | Mô tả |
|---|-----------|-------|
| 1 | 📥 **Thêm môn học** | Nhập TBTK, điểm cuối kỳ, tín chỉ, học kỳ |
| 2 | 📋 **Xem bảng điểm** | Hiển thị theo từng học kỳ, có điểm chữ và hệ 4 |
| 3 | 📊 **Tính GPA và xếp loại** | GPA hệ 10, hệ 4, xếp loại học lực |
| 4 | 🔮 **Dự đoán điểm cuối kỳ** | Cần bao nhiêu điểm để đạt mục tiêu |
| 5 | 🗑️ **Xóa môn học** | Xóa môn nhập nhầm |

---

## 🚀 Cách chạy

### ⚙️ Yêu cầu
- Python 3.10 trở lên
- pytest (để chạy test)

### 📦 Cài đặt

```bash
git clone https://github.com/mthanhcode/gpa_tracker.git
cd gpa_tracker
pip install pytest
```

### ▶️ Chạy chương trình

```bash
python main.py
```

### 🧪 Chạy test

```bash
pytest tests/test_grading.py -v
```

---

## 🖥️ Demo

```
===== GPA TRACKER - HITC =====
1. Thêm môn học
2. Xem bảng điểm
3. Xem GPA và xếp loại
4. Dự đoán điểm cuối kỳ cần đạt
5. Xóa môn học
0. Thoát
==============================

📅 HK1-2025
STT   Tên môn         TC   Tổng kết  Chữ   Hệ 4   GPA
-------------------------------------------------------
1     Kỹ năng mềm     2    9.6       A     4.0    ✅
2     Toán ứng dụng   3    8.1       B     3.0    ✅

📊 GPA hệ 10: 8.74
📊 GPA hệ 4:  3.40
🎓 Xếp loại:  Giỏi
```

---

## 📁 Cấu trúc dự án

```
gpa_tracker/
├── 📄 main.py              # Menu chính, nhập/xuất
├── 📁 src/
│   ├── grading.py          # Logic tính toán (convert, GPA, classify)
│   └── storage.py          # Đọc/ghi JSON
├── 📁 tests/
│   └── test_grading.py     # 19 test cases
├── 📁 data/
│   └── courses.json        # Dữ liệu môn học (tự tạo khi chạy)
├── 🖼️ banner.svg           # Banner README
├── 📄 README.md
└── 📄 AI_USAGE.md
```

---

## 🏗️ Quyết định thiết kế

### 🔀 Tách logic khỏi giao diện
`grading.py` là logic thuần, không có `input()` hay `print()`. Nhờ vậy test được mà không cần gõ bàn phím, và dễ thêm giao diện web sau này mà không sửa lõi.

### 📋 Quy tắc trường là dữ liệu, không phải code

```python
GRADE_TABLE = [
    (8.5, "A", 4.0),
    (7.0, "B", 3.0),
    (5.5, "C", 2.0),
    (4.0, "D", 1.0),
    (0.0, "F", 0.0),
]
```

Muốn đổi trường → chỉ đổi bảng, không sửa thuật toán.

### 🔒 Tuple cho bảng quy đổi
Dữ liệu cố định, không ai được sửa trong lúc chạy → dùng `tuple` thay `list`.

### 🛡️ `.get()` thay vì `[]` khi truy cập dict

```python
course.get("counts_in_gpa", True)  # An toàn hơn course["counts_in_gpa"]
```

Nếu thiếu key thì dùng giá trị mặc định, không crash.

---

## 🧪 Kiểm thử

19 test cases bao gồm:

| Loại | Ví dụ |
|------|-------|
| ✅ Normal case | Tính điểm tổng kết từ TBTK và cuối kỳ |
| 🔲 Boundary case | 7.0 → B, 6.9 → C (đúng biên) |
| 📭 Empty input | Danh sách môn rỗng → GPA = 0.0 |
| ❌ Invalid input | Điểm 11.0 hoặc -1.0 → ValueError |
| 💾 Storage | Lưu rồi đọc lại → khớp chính xác |
| 🔥 Corrupt file | JSON hỏng → trả về list rỗng |

### 📊 Kiểm chứng bằng số thật

| Học kỳ | GPA hệ 10 | GPA hệ 4 | Kết quả |
|--------|-----------|----------|---------|
| HK1 (2025-2026) | 7.77 | 3.06 | ✅ Khớp |
| HK2 (2025-2026) | 6.82 | 2.25 | ✅ Khớp |
| Tích lũy | 7.27 | 2.63 | ✅ Khớp |

---

## 🔧 Công thức áp dụng

```
📐 Điểm tổng kết = 0.4 × TBTK + 0.6 × Cuối kỳ  (làm tròn 1 chữ số)
📐 GPA           = Σ(điểm_hệ4 × tín_chỉ) / Σ tín_chỉ
📐 Điểm cần đạt = (Mục tiêu − 0.4 × TBTK) / 0.6
```

---

## 🚧 Cải tiến trong tương lai

- [ ] 🌐 Đọc bảng quy đổi từ JSON để hỗ trợ nhiều trường
- [ ] 💻 Giao diện web bằng Streamlit
- [ ] 📄 Xuất bảng điểm ra file PDF
- [ ] 🔄 Xử lý môn học lại

---

<div align="center">

**👨‍💻 mthanhcode** · Sinh viên HITC · Capstone Project Python Journey 🎓

</div>
