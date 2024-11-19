import os
import matplotlib.pyplot as plt


class Student:
    def __init__(self, name, id):
        self.name = name
        self.id = int(id)


class Assignment:
    def __init__(self, name, id, points):
        self.points = int(points)
        self.name = name
        self.id = int(id)


class Submission:
    def __init__(self, assignment, student, score):
        self.student = int(student)
        self.assignment = int(assignment)
        self.score = int(score)


def get_students():
    with open("data/students.txt", "r") as file:
        students = {}
        for line in file:
            students[line[3:].strip()] = Student(line[3:].strip(), int(line[:3]))
        return students


def get_assignments():
    with open("data/assignments.txt", "r") as file:
        assignments = file.read()
        assignments = assignments.split("\n")
        assignments = [
            Assignment(*assignments[i : i + 3])
            for i in range(0, len(assignments) - 3, 3)
        ]
        assignment_dict = {}
        for assignment in assignments:
            assignment_dict[assignment.id] = assignment
        return assignment_dict


def get_submissions():
    submissions = []
    for filename in os.listdir("data/submissions"):
        with open(f"data/submissions/{filename}", "r") as file:
            student_id, assignment_id, score = file.read().split("|")
            submissions.append(Submission(assignment_id, student_id, score))
    return submissions


def get_menu_selection():
    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph")
    print()
    return input("Enter your selection: ")


def main():
    students = get_students()
    assignments = get_assignments()
    submissions = get_submissions()
    selection = get_menu_selection()
    if selection == "1":
        name = input("What is the student's name: ")
        try:
            student = students[name]
        except KeyError:
            print("Student not found")
            return
        score = 0
        for submission in submissions:
            if submission.student != student.id:
                continue
            score += assignments[submission.assignment].points * (
                submission.score / 100
            )
        print(f"{round(score / 10)}%")
    if selection == "2" or selection == "3":
        name = input("What is the assignment name: ")
        for a in assignments.values():
            if a.name == name:
                assignment = a
                break
        else:
            print("Assignment not found")
            return
        subs = list(
            map(
                lambda s: s.score,
                filter(lambda s: s.assignment == assignment.id, submissions),
            )
        )
        if selection == "2":
            min_score = min(subs)
            average_score = sum(subs) // len(subs)
            max_score = max(subs)
            print(f"Min: {min_score}%")
            print(f"Avg: {average_score}%")
            print(f"Max: {max_score}%")

        if selection == "3":
            plt.hist(subs, bins=range(50, 101, 5))
            plt.show()


if __name__ == "__main__":
    main()