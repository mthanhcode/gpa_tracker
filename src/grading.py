# Hệ số tính điểm tổng kết 
MIDTERM_WEIGHT = 0.4
FINAL_WEIGHT = 0.6

def calculate_final_score(midterm, final) :
    raw = MIDTERM_WEIGHT * midterm + FINAL_WEIGHT * final
    return round(raw, 1)
    