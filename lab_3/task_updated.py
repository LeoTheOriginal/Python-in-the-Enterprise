import random
import logging
from statistics import mean
from typing import Dict, Any
import json
from datetime import date, timedelta

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


def generate_attendance(days: int, presence_weight: float = 0.8) -> Dict[str, bool]:
    start_date = date(2024, 9, 1)
    attendance = {}
    for i in range(days):
        current_date = start_date + timedelta(days=i)
        attendance[current_date.strftime("%d-%m")] = random.choices([True, False],
                                                                    weights=[presence_weight, 1-presence_weight])[0]
    return attendance


def generate_students(num_students: int, subjects: list) -> Dict[str, Dict[str, Any]]:
    first_names = ["John", "Jane", "Alice", "Bob", "Charlie", "Diana", "Eve", "Frank"]
    last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson"]
    students = {}

    for _ in range(num_students):
        full_name = f"{random.choice(first_names)} {random.choice(last_names)}"
        students[full_name] = {
            "subjects": {
                subject: {
                    "scores": [random.randint(2, 5) for _ in range(5)],
                    "attendance": generate_attendance(60)
                } for subject in subjects
            }
        }

        for subject_data in students[full_name]["subjects"].values():
            subject_data["average_attendance"] = calculate_average_attendance(subject_data["attendance"])

        students[full_name]["average_attendance"] = (calculate_average_attendance_for_student
                                                     (students[full_name]["subjects"]))
        students[full_name]["average_score"] = calculate_average_score_for_student(students[full_name]["subjects"])

        logging.info(f"Generated student: {full_name}")

    return students


def calculate_average_attendance(attendance: Dict[str, bool]) -> float:
    return sum(attendance.values()) / len(attendance) if attendance else 0.0


def calculate_average_attendance_for_student(subjects: Dict[str, Dict[str, Any]]) -> float:
    attendance_values = [attendance
                         for subject_data in subjects.values()
                         for attendance in subject_data["attendance"].values()]
    return sum(attendance_values) / len(attendance_values) if attendance_values else 0.0


def calculate_average_score_for_student(subjects: Dict[str, Dict[str, Any]]) -> float:
    all_scores = [score for subject_data in subjects.values() for score in subject_data["scores"]]
    return mean(all_scores) if all_scores else 0.0


def calculate_daily_average_attendance(students: Dict[str, Dict[str, Any]]) -> Dict[str, float]:
    daily_attendance = {}
    for student_data in students.values():
        for subject_data in student_data["subjects"].values():
            for day, was_present in subject_data["attendance"].items():
                if day not in daily_attendance:
                    daily_attendance[day] = []
                daily_attendance[day].append(was_present)

    daily_average_attendance = {day: mean(presences) for day, presences in daily_attendance.items()}
    return daily_average_attendance


def save_students_to_file(students: Dict[str, Dict[str, Any]], filename: str):
    with open(filename, 'w') as file:
        json.dump(students, file, indent=2, ensure_ascii=False)
    logging.info(f"Saved students to {filename}")


def load_students_from_file(filename: str) -> Dict[str, Dict[str, Any]]:
    with open(filename, 'r') as file:
        students = json.load(file)
    logging.info(f"Loaded students from {filename}")
    return students


if __name__ == '__main__':

    num_students = 12
    subjects = ["math", "english", "PE", "chemistry", "physics"]

    students = generate_students(num_students, subjects)
    save_students_to_file(students, 'students_data.txt')

    loaded_students = load_students_from_file('students_data.txt')

    print("Students' Data and Averages:")
    for student_name, data in loaded_students.items():
        print(f"\nStudent: {student_name}")
        print(f"  Average Attendance: {data['average_attendance']*100:.2f}%")
        print(f"  Average Score: {data['average_score']:.2f}")
        for subject, subject_data in data["subjects"].items():
            print(f"    Subject: {subject.capitalize()}")
            print(f"      Scores: {subject_data['scores']}")
            print(f"      Attendance: {subject_data['attendance']}")
            print(f"      Average Attendance: {subject_data['average_attendance'] * 100:.2f}%")

    daily_avg_attendance = calculate_daily_average_attendance(loaded_students)
    print("\nDaily Average Attendance:")
    for day, avg in daily_avg_attendance.items():
        print(f"  {day}: {avg * 100:.2f}%")
