from src.grading import calculate_final_score, convert_score

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