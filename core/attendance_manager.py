import os
import csv
from datetime import datetime

ATTENDANCE_FILE = "data/attendance.csv"


def init_attendance():
    if not os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["username", "date", "punch_in", "punch_out"])


def read_attendance():
    init_attendance()
    records = []

    with open(ATTENDANCE_FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("username") and row.get("date"):
                records.append(row)

    return records


def punch_in(username):
    init_attendance()
    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%H:%M:%S")

    rows = read_attendance()

    for row in rows:
        if row["username"] == username and row["date"] == today:
            return False, "Already punched in today"

    with open(ATTENDANCE_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([username, today, now, ""])

    return True, f"Punch in successful for {username}"


def punch_out(username):
    init_attendance()
    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%H:%M:%S")

    rows = read_attendance()
    updated = False

    with open(ATTENDANCE_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["username", "date", "punch_in", "punch_out"])

        for row in rows:
            if (
                row["username"] == username
                and row["date"] == today
                and row["punch_out"] == ""
            ):
                row["punch_out"] = now
                updated = True

            writer.writerow([
                row["username"],
                row["date"],
                row["punch_in"],
                row["punch_out"]
            ])

    if not updated:
        return False, "Punch in first"

    return True, f"Punch out successful for {username}"
