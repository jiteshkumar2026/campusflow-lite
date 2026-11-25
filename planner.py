from datetime import date, timedelta
from llm import ask_llm


def generate_plan(subjects, exam_date, hours_per_day=4):
    """
    subjects: list of {"name": str, "syllabus": str, "difficulty": optional str}
    exam_date: datetime.date
    hours_per_day: number of study hours available each day
    Returns the study plan as markdown text.
    """
    if not subjects:
        return "Please add at least one subject."

    days_left = (exam_date - date.today()).days
    if days_left < 1:
        return "The exam date must be in the future."

    lines = []
    for s in subjects:
        line = f"- {s['name']}: {s['syllabus']}"
        if s.get("difficulty"):
            line += f" (difficulty: {s['difficulty']})"
        lines.append(line)
    subj_text = "\n".join(lines)

    revision_days = 2 if days_left > 4 else 1

    prompt = f"""Create a personalized day-by-day study schedule.

Today: {date.today()}
Exam date: {exam_date} ({days_left} days left)
Study hours available per day: {hours_per_day}

Subjects and syllabus:
{subj_text}

Rules:
- Give more time to subjects with a larger syllabus or higher difficulty.
- Cover every topic at least once.
- Keep the last {revision_days} day(s) for revision only.
- Never exceed {hours_per_day} hours in a day.
- Output a markdown table with columns: Day | Date | Subject | Topics | Hours.
- After the table, add 3 short, practical study tips.
- Output only the schedule and tips, with no introduction."""
    return ask_llm(prompt)


if __name__ == "__main__":
    plan = generate_plan(
        [
            {"name": "DBMS", "syllabus": "ER model, SQL, normalization, transactions"},
            {"name": "OS", "syllabus": "Processes, scheduling, deadlocks, memory"},
        ],
        date.today() + timedelta(days=10),
        hours_per_day=4,
    )
    print(plan)