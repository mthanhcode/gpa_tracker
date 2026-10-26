"""Command-line interface for GPA Tracker, designed for automation and OpenClaw skills."""
import argparse
import json
import sys

from src.grading import calculate_final_score, convert_score, calculate_gpa, classify, predict_score
from src.storage import load_courses, save_courses


def emit(data):
    print(json.dumps(data, ensure_ascii=False, indent=2))


def command_summary(_args):
    courses = load_courses()
    gpa10, gpa4 = calculate_gpa(courses)
    emit({
        "course_count": len(courses),
        "counted_course_count": sum(1 for c in courses if c.get("counts_in_gpa", True)),
        "gpa_10": gpa10,
        "gpa_4": gpa4,
        "classification": classify(gpa4),
        "courses": courses,
    })


def command_list(args):
    courses = load_courses()
    if args.semester:
        courses = [c for c in courses if c.get("semester", "") == args.semester]
    emit({"count": len(courses), "courses": courses})


def command_add(args):
    courses = load_courses()
    if any(c.get("name", "").strip().casefold() == args.name.strip().casefold()
           and c.get("semester", "") == args.semester for c in courses):
        emit({"ok": False, "error": "A course with this name already exists in this semester."})
        return 2
    final_score = calculate_final_score(args.midterm, args.final)
    letter, gpa4 = convert_score(final_score)
    course = {
        "name": args.name.strip(),
        "credits": args.credits,
        "midterm": args.midterm,
        "final": args.final,
        "final_score": final_score,
        "letter": letter,
        "gpa4": gpa4,
        "counts_in_gpa": not args.exclude_from_gpa,
        "semester": args.semester.strip() or "Chưa phân loại",
    }
    courses.append(course)
    save_courses(courses)
    emit({"ok": True, "message": "Course added.", "course": course})
    return 0


def command_predict(args):
    needed = predict_score(args.midterm, args.target)
    max_possible = round(0.4 * args.midterm + 0.6 * 10, 2)
    emit({
        "midterm": args.midterm,
        "target_final_score": args.target,
        "required_final_exam_score": needed,
        "possible": needed <= 10,
        "already_reached_without_exam": needed <= 0,
        "maximum_final_score": max_possible,
    })


def command_delete(args):
    if not args.confirm:
        emit({"ok": False, "error": "Deletion requires --confirm. Ask the user for explicit confirmation first."})
        return 2
    courses = load_courses()
    if not (1 <= args.index <= len(courses)):
        emit({"ok": False, "error": f"Index must be between 1 and {len(courses)}."})
        return 2
    removed = courses.pop(args.index - 1)
    save_courses(courses)
    emit({"ok": True, "message": "Course deleted.", "course": removed})
    return 0


def build_parser():
    parser = argparse.ArgumentParser(description="GPA Tracker automation interface")
    sub = parser.add_subparsers(dest="command", required=True)

    summary = sub.add_parser("summary", help="Show GPA summary and courses")
    summary.set_defaults(func=command_summary)

    listing = sub.add_parser("list", help="List saved courses")
    listing.add_argument("--semester", help="Filter by exact semester label")
    listing.set_defaults(func=command_list)

    add = sub.add_parser("add", help="Add a course")
    add.add_argument("--name", required=True)
    add.add_argument("--credits", required=True, type=int)
    add.add_argument("--midterm", required=True, type=float)
    add.add_argument("--final", required=True, type=float)
    add.add_argument("--semester", default="Chưa phân loại")
    add.add_argument("--exclude-from-gpa", action="store_true")
    add.set_defaults(func=command_add)

    predict = sub.add_parser("predict", help="Calculate required final-exam score")
    predict.add_argument("--midterm", required=True, type=float)
    predict.add_argument("--target", required=True, type=float, help="Target overall course score from 0 to 10")
    predict.set_defaults(func=command_predict)

    delete = sub.add_parser("delete", help="Delete a course by 1-based index")
    delete.add_argument("--index", required=True, type=int)
    delete.add_argument("--confirm", action="store_true", help="Required confirmation flag")
    delete.set_defaults(func=command_delete)
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    try:
        if hasattr(args, "credits") and args.credits <= 0:
            parser.error("--credits must be greater than zero")
        for field in ("midterm", "final", "target"):
            value = getattr(args, field, None)
            if value is not None and not 0 <= value <= 10:
                parser.error(f"--{field.replace('_', '-')} must be between 0 and 10")
        result = args.func(args)
        return result if isinstance(result, int) else 0
    except (ValueError, KeyError, TypeError) as exc:
        emit({"ok": False, "error": str(exc)})
        return 2


if __name__ == "__main__":
    sys.exit(main())
