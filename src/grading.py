# Hệ số tính điểm tổng kết 
MIDTERM_WEIGHT = 0.4
FINAL_WEIGHT = 0.6

# Hàm 1:
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

# Hàm 2:
def convert_score(score, table = GRADE_TABLE):
    if not (0.0 <= score <= 10.0):
        raise ValueError(f"Điểm không hợp lệ: {score}. Phải từ 0 đến 10.")
    for min_score, letter, gqa4 in table:
        if score >= min_score:
            return letter, gqa4
    
#Hàm 3: calculate_gpa
def calculate_gpa(courses):
    if not courses:
        return 0.0, 0.0

    total_credits = 0
    weighted_10 = 0.0
    weighted_4 = 0.0

    for course in courses:
        #bỏ qua môn không tính GPA
        if not course.get("counts_in_gpa", True):
            continue
        credits = course["credits"]
        score = course["final_score"]
        _, gpa4 = convert_score(score)

        total_credits += credits
        weighted_10 += score * credits
        weighted_4 += gpa4 * credits

    if total_credits == 0:
        return 0.0, 0.0
    gpa_10 = round(weighted_10 / total_credits, 2)
    gpa_4 = round(weighted_4 / total_credits, 2)
    return gpa_10, gpa_4

    # Hàm 4: Classify
    # Bảng xếp loại học lực của HITC
    # Nguồn: qtkd.hitu.edu.vn, kiểm chứng: 3.06 --> khá, 2.25 --> trung bình
CLASSIFICATION_TABLE = [
        (3.60, "Xuất sắc"),
        (3.20, "Giỏi"),
        (2.50, "Khá"),
        (2.00, "Trung bình"),
        (0.00, "Yếu"),
    ]

def classify(gpa4):
    for min_gpa, label in CLASSIFICATION_TABLE:
        if gpa4 >= min_gpa:
            return label
    return "Yếu"