from src.grading import calculate_final_score, convert_score, calculate_gpa, classify

def test_calculate_final_score_normal():
    #Kỹ thuật lập trình: 0.4*8.30 + 0.6*5.50 = 6.62 -> 6.6
    assert calculate_final_score(8.30, 5.50) == 6.6

def test_calculate_final_score_phan_mem_xu_ly_anh():
    #Phần mềm xử lý ảnh: 0.4*7.70 + 0.6*6.00 = 6.68 -> 6.7
    assert calculate_final_score(7.70, 6.00) == 6.7

def test_calculate_final_score_ky_nang_mem():
    #Kỹ năng mềm: 0/4*10.00 + 0.6*9.00 = 9.40 -> 9.4
    assert calculate_final_score(10.00, 9.00) == 9.4


def test_convert_score_A():
    #8.6 -> A, kiểm chứng từ môn Cầu Lông
    assert convert_score(8.6) == ("A", 4.0)

def test_convert_score_B():
    #7.0 -> B, kiểm chứng từ môn GDQP (đúng biên)
    assert convert_score(7.0) == ("B", 3.0)

def test_convert_score_C():
    #6.9 -> C, kiểm chứng từ môn Pháp Luật
    assert convert_score(6.9) == ("C", 2.0)

def test_convert_score_D():
    #5.1-> D, kiểm chứng từ môn Cơ sở dữ liệu
    assert convert_score(5.1) == ("D", 1.0)

def test_convert_score_invalid():
    # Điểm ngoài 0-10 phải báo lỗi
    import pytest
    with pytest.raises(ValueError):
        convert_score(11.0)
    with pytest.raises(ValueError):
        convert_score(-1.0)

def test_calculate_gpa_ky1():
    #Dữ liệu kỳ 1 thật, trường tính: 7.77 / 3,06
    courses = [
        {"credits": 3, "final_score": 8.1, "counts_in_gpa": True},
        {"credits": 2, "final_score": 9.4, "counts_in_gpa": True},
        {"credits": 5, "final_score": 7.6, "counts_in_gpa": True},
        {"credits": 2, "final_score": 9.1, "counts_in_gpa": True},
        {"credits": 3, "final_score": 5.5, "counts_in_gpa": True},
        {"credits": 3, "final_score": 8.0, "counts_in_gpa": True},
        {"credits": 3, "final_score": 7.0, "counts_in_gpa": False},
    ]
    gpa_10, gpa_4 = calculate_gpa(courses)
    assert gpa_10 == 7.77
    assert gpa_4 == 3.06

def test_calculate_gpa_empty():
    #Danh sách môn học rỗng
    assert calculate_gpa([]) == (0.0, 0.0)

def test_calculate_gpa_all_excluded():
    #Tất cả môn học không tính GPA
    courses = [
        {"credits": 3, "final_score": 8.0, "counts_in_gpa": False},
        {"credits": 2, "final_score": 9.0, "counts_in_gpa": False},
    ]
    assert calculate_gpa(courses) == (0.0, 0.0)


def test_classify_xuat_sac():
    assert classify(3.60) == "Xuất sắc"

def test_classify_gioi():
    assert classify(3.20) == "Giỏi"

def test_classify_kha():
    #kiểm chứng từ GPA 3.06 kỳ 1 thật
    assert classify(3.06) == "Khá"

def test_classify_trung_binh():
    #kiểm chứng từ GPA 2.25 --> Trung bình
    assert classify(2.25) == "Trung bình"

def test_classify_yeu():
    assert classify(1.50) == "Yếu"

    