from datetime import date, timedelta
from pypdf import PdfReader
from llm import ask_llm


def extract_pdf_text(files, max_chars=6000):
    """Read uploaded PDFs (Streamlit files) and return their text, trimmed to max_chars."""
    if not files:
        return ""
    per_file = max_chars // len(files)
    parts = []
    for f in files:
        try:
            reader = PdfReader(f)
            text = " ".join((p.extract_text() or "") for p in reader.pages)
            text = " ".join(text.split())
            if text:
                parts.append(f"[{f.name}]\n{text[:per_file]}")
        except Exception:
            continue
    return "\n\n".join(parts)


def generate_plan(subjects, syllabus, exam_date, hours_per_day=4, notes=""):
    days_left = (exam_date - date.today()).days
    if days_left < 1:
        return "Please choose an exam date after today."

    revision_days = 2 if days_left > 4 else 1
    notes_block = f"\nExtra notes from uploaded PDFs:\n{notes}\n" if notes else ""

    prompt = f"""Create a personalized day-by-day study schedule.

Today: {date.today()}
Exam date: {exam_date} ({days_left} days left)
Study hours available per day: {hours_per_day}

Subjects: {subjects}

Syllabus / important topics:
{syllabus}
{notes_block}
Rules:
- Split the syllabus across the listed subjects sensibly.
- Give more time to subjects with larger or harder syllabus.
- Cover every topic at least once.
- Keep the last {revision_days} day(s) for revision only.
- Never exceed {hours_per_day} hours in a day.
- Output a markdown table with columns: Day | Date | Subject | Topics | Hours.
- If there are more than 14 days, group days into weeks to keep the table short.
- After the table, add 3 short, practical study tips.
- Output only the schedule and tips, with no introduction."""
    return ask_llm(prompt)


if __name__ == "__main__":
    print(generate_plan(
        "DBMS, OS",
        "DBMS: ER model, SQL, normalization. OS: processes, scheduling, deadlocks.",
        date.today() + timedelta(days=10),
    ))