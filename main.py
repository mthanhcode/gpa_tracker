from src.grading import calculate_final_score, convert_score, calculate_gpa, classify
from src.storage import load_courses, save_courses


def show_menu():
    print("\n===== GPA TRACKER - HITC =====")
    print("1. Thêm môn học")
    print("2. Xem bảng điểm")
    print("3. Xem GPA và xếp loại")
    print("4. Dự đoán điểm cuối kỳ cần đạt")
    print("5. Xóa môn học")
    print("0. Thoát")
    print("==============================")

def add_course(courses):
    print("\n--- Thêm môn học ---")
    name = input("Tên môn: ").strip()
    if not name:
        print("❌ Tên môn không được để trông.")
        return

    try:
        credits = int(input("Số tín chỉ: "))
        if credits <= 0:
            print("❌ Số tín chỉ phải lớn hơn 0.")
            return
        midterm = float(input("Điểm quá trình (TBTK): "))
        final = float(input("Điểm cuối kỳ: "))
    except ValueError:
        print("❌ Điểm và tín chỉ phải là số.")
        return

    try:
        final_score = calculate_final_score(midterm, final)
        letter, gpa4 = convert_score(final_score)
    except ValueError as e:
        print(f"❌ {e}")
        return

    semester = input("Học kỳ (ví dụ: HK1-2025): ").strip()
    if not semester:
            semester = "Chưa phân loại"
    counts = input("Tính vào GPA không? (y/n): ").strip().lower()
    counts_in_gpa = counts != "n"
    course = {
        "name": name,
        "credits": credits,
        "midterm": midterm,
        "final": final,
        "final_score": final_score,
        "letter": letter,
        "gpa4": gpa4,
        "counts_in_gpa": counts_in_gpa,
        "semester": semester,
    }
    courses.append(course)
    save_courses(courses)
    print(f"✅ Đã thêm {name}: {final_score} ({letter}) - {gpa4}")

def show_courses(courses):
    if not courses:
        print("\n⚠️ Chưa có môn học nào. ")
        return

    # Nhóm môn theo học kỳ
    semesters = {}
    for c in courses:
        sem = c.get("semester", "Chưa phân loại")
        if sem not in semesters:
            semesters[sem] = [] 
        semesters[sem].append(c)
    
    stt = 1
    for sem, sem_courses in semesters.items():
        print(f" {sem}")
        print(f"{'STT':<5} {'Tên môn':<25} {'TC':<5} {'Tổng kết':<10} {'Chữ':<5} {'Hệ 4:':<6} {'GPA'}")
        print("-" * 65)
        for c in sem_courses:
            gpa_tag = "✅" if c["counts_in_gpa"] else "❌"
            print(f"{stt:<5} {c['name']:<25} {c['credits']:<4} {c['final_score']:<8} {c['letter']:<6} {c['gpa4']:<6} {gpa_tag}")
            stt += 1

def show_gpa(courses):
    if not courses:
        print("\n⚠️ Chưa có môn học nào, hãy thêm môn học")
        return
    gpa_10, gpa_4 = calculate_gpa(courses)
    label = classify(gpa_4)
    print(f"\n📊 GPA hệ 10: {gpa_10}")
    print(f"\n📊 GPA hệ 4: {gpa_4}")
    print(f"\n🎓 Xếp loại: {label}")

def predict_score(courses):
    print("\n--- Dự đoán điểm cuối kỳ cần đạt ---")
    try:
        midterm = float(input("Điểm quá trình (TBTK) môn sắp thi (0.0 - 10.0): "))
        if not (0 <= midterm <= 10):
            print("❌ Điểm quá trình phải nằm trong khoảng từ 0.0 đến 10.0, hãy nhập lại điểm quá trình!")
            return
        
        target = float(input("Điểm tổng kết mục tiêu (ví dụ 8.5 để đạt A): "))
        if not (0 <= target <= 10):
            print("❌ Điểm mục tiêu phải nằm trong khoảng từ 0.0 đến 10.0, hãy nhập lại điểm mục tiêu!")
            return
        
    except ValueError:
        print("❌ Vui lòng nhập số hợp lệ (0.0 - 10.0)")
        return
    
    # Công thức: Final = (Target - 0.4 * Midterm) / 0.6
    needed = (target - 0.4 * midterm) / 0.6

    if needed > 10:
        max_possible = midterm * 0.4 + 10.0 * 0.6
        print(f" Mục tiêu không khả thi!")
        print(f"❌ Dù thi cuối kỳ đạt 10/10 thì điểm tổng kết tối đa cũng chỉ được {max_possible:.1f}.")
    elif needed < 0:
        print(f"✅ Bạn đã đạt mục tiêu rồi, không cần thì cũng được!")
    else:
        print(f"✅ Cần đạt ít nhất {needed:.2f} điểm cuối kỳ.")

def delete_course(courses):
    show_courses(courses)
    if not courses:
        return
    try:
        idx = int(input("\n Nhập STT môn muốn xóa: ")) -1
        if not (0 <= idx < len(courses)):
            print("❌ STT không hợp lệ.")
            return
        removed = courses.pop(idx)
        save_courses(courses)
        print(f" Đã xóa môn: {removed['name']}")
    except ValueError: 
        print(f"❌ Vui lòng nhập số.")


def main():
    courses = load_courses()
    while True:
        show_menu()
        choice = input("Chọn: ").strip()
        if choice == "1":
            add_course(courses)
        elif choice == "2":
            show_courses(courses)
        elif choice == "3":
            show_gpa(courses)
        elif choice == "4":
            predict_score(courses)
        elif choice == "5":
            delete_course(courses)
        elif choice == "0":
            print("👋 Tạm biệt!")
            break
        else:
            print("❌ Lựa chọn không hợp lệ.")


if __name__ == "__main__":
    main()