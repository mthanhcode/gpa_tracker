from src.grading import calculate_final_score

def test_calculate_final_score_normal():
    #Kỹ thuật lập trình: 0.4*8.30 + 0.6*5.50 = 6.62 -> 6.6
    assert calculate_final_score(8.30, 5.50) == 6.6

def test_calculate_final_score_phan_mem_xu_ly_anh():
    #Phần mềm xử lý ảnh: 0.4*7.70 + 0.6*6.00 = 6.68 -> 6.7
    assert calculate_final_score(7.70, 6.00) == 6.7

def test_calculate_final_score_ky_nang_mem():
    #Kỹ năng mềm: 0/4*10.00 + 0.6*9.00 = 9.40 -> 9.4
    assert calculate_final_score(10.00, 9.00) == 9.4