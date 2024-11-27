import random
import logging
from statistics import mean
from typing import List, Optional


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


class Student:
    def __init__(self, first_name: str, last_name: str, attendance: int,
                 math_scores: List[int], english_scores: List[int], PE_scores: List[int]):
        self.first_name = first_name
        self.last_name = last_name
        self.attendance = attendance
        self.scores = {
            "math": math_scores,
            "english": english_scores,
            "PE": PE_scores
        }

    def get_class_average(self, subject: str) -> Optional[float]:
        if subject in self.scores and self.scores[subject]:
            return mean(self.scores[subject])
        return None

    def get_total_average(self) -> Optional[float]:
        all_scores = [score for scores in self.scores.values() for score in scores]
        if all_scores:
            return mean(all_scores) #ewentualnie else i zwórć wyjątek
        return None

    def __str__(self):
        return f"{self.first_name} {self.last_name}, Attendance: {self.attendance}"

    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "attendance": self.attendance,
            "scores": self.scores
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            first_name=data["first_name"],
            last_name=data["last_name"],
            attendance=data["attendance"],
            math_scores=data["scores"]["math"],
            english_scores=data["scores"]["english"],
            PE_scores=data["scores"]["PE"]
        )


class Highschool:
    def __init__(self):
        self.students: List[Student] = []

    def add_student(self, student: Student):
        self.students.append(student)
        logging.info(f"Added {student}")

    def get_school_average(self) -> Optional[float]:
        averages = [student.get_total_average() for student in self.students if
                    student.get_total_average() is not None]
        if averages:
            return mean(averages)
        return None

    def get_class_average(self, subject: str) -> Optional[float]:
        averages = [student.get_class_average(subject) for student in self.students if
                    student.get_class_average(subject) is not None]
        if averages:
            return mean(averages)
        return None


def student_generator(num_students: int) -> List[Student]:
    first_names = ["John", "Jane", "Alice", "Bob", "Charlie", "Diana", "Eve", "Frank"]
    last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson"]
    students = []

    for _ in range(num_students):
        student = Student(
            first_name=random.choice(first_names),
            last_name=random.choice(last_names),
            attendance=random.randint(30, 45),
            math_scores=[random.randint(2, 5) for _ in range(5)],
            english_scores=[random.randint(2, 5) for _ in range(5)],
            PE_scores=[random.randint(2, 5) for _ in range(5)]
        )
        students.append(student)
        logging.info(f"Generated student: {student}")
    return students


if __name__ == '__main__':

    highschool = Highschool()

    new_students = list(student_generator(5))
    for student in new_students:
        highschool.add_student(student)

    print("Class Averages:")
    for subject in ["math", "english", "PE"]:
        print(f"{subject.capitalize()} Average: {highschool.get_class_average(subject):.2f}")

    print(f"\nOverall School Average: {highschool.get_school_average():.2f}")