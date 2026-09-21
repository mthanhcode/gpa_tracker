# Hệ số tính điểm tổng kết 
MIDTERM_WEIGHT = 0.4
FINAL_WEIGHT = 0.6

def calculate_final_score(midterm, final) :
    raw = MIDTERM_WEIGHT * midterm + FINAL_WEIGHT * final
    return round(raw, 1)


# Bảng quy đổi điểm của HITC
# (ngưỡng tối thiểu, điểm chữ, hệ 4)
# Đã được kiểm chứng từ bảng điểm thật: 7.0 -> B, 6.9 -> C, 8.6 -> A
GRADE_TABLE = [
    (8.5, "A", 4.0),
    (7.0, "B", 3.0),
    (5.5, "C", 2.0),
    (4.0, "D", 1.0),
    (0.0, "F", 0.0),
]


def convert_score(score, table = GRADE_TABLE):
    if not (0.0 <= score <= 10.0):
        raise ValueError(f"Điểm không hợp lệ: {score}. Phải từ 0 đến 10.")
    for min_score, letter, gqa4 in table:
        if score >= min_score:
            return letter, gqa4
    