---
name: gpa-tracker
description: Read and manage the user's GPA Tracker records, calculate GPA, predict required scores, and summarize academic progress.
user-invocable: true
---

# GPA Tracker assistant

Use this skill when the user asks about their GPA Tracker records, course grades, target scores, semester summaries, or study priorities.

## Project location and interface

Run commands from the root of the user's cloned `gpa_tracker` repository. Use the project's Python environment if one exists.

- Read GPA summary: `python gpa_cli.py summary`
- List courses: `python gpa_cli.py list`
- List one semester: `python gpa_cli.py list --semester "HK1-2025"`
- Predict final-exam score: `python gpa_cli.py predict --midterm 7.0 --target 8.5`
- Add a course: `python gpa_cli.py add --name "Kỹ thuật lập trình" --credits 3 --midterm 8.0 --final 7.5 --semester "HK2-2026"`
- Delete a course: `python gpa_cli.py delete --index 2 --confirm`

The command-line interface emits JSON. Interpret the output and explain it in plain Vietnamese unless the user asks for another language.

## Safety and correctness

1. Treat saved grades as user-owned academic data. Never invent grades or claim a command succeeded unless its output confirms success.
2. Read the current summary/list before answering questions about saved records.
3. For calculations, use the project's grading functions through the CLI rather than estimating manually.
4. Before adding a course, make sure the user has supplied the course name, credit count, continuous-assessment score, final-exam score, and semester. If anything is missing, ask for it.
5. Before changing saved data, summarize the exact change and obtain explicit user approval. Do not add, edit, or delete records based on an ambiguous request.
6. Deletion is especially sensitive: show the indexed list, ask the user to confirm the exact course, then use `delete --index N --confirm`.
7. Do not expose the full course list unless relevant to the user's request. Never send academic data to an external service unless the user explicitly asks and the service is configured.
8. Distinguish the course's final score from cumulative GPA. State that GPA rules depend on the institution's grading policy.
9. If a command fails, report the error plainly and do not claim the task completed.
