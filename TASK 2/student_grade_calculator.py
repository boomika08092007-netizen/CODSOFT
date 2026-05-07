
# ============================================================
#         STUDENT GRADE CALCULATOR
#         Uses: Arrays (Lists), Loops, Functions
# ============================================================

def get_subject_count():
    """Ask the user how many subjects to enter."""
    while True:
        try:
            count = int(input("Enter the number of subjects: "))
            if count <= 0:
                print("  [!] Number of subjects must be at least 1. Try again.\n")
            else:
                return count
        except ValueError:
            print("  [!] Invalid input. Please enter a whole number.\n")


def get_mark(subject_name):
    """
    Prompt for a mark for a given subject.
    Validates that the mark is between 0 and 100 (inclusive).
    """
    while True:
        try:
            mark = float(input(f"  Enter marks for {subject_name} (0–100): "))
            if 0 <= mark <= 100:
                return mark
            else:
                print("  [!] Marks must be between 0 and 100. Try again.")
        except ValueError:
            print("  [!] Invalid input. Please enter a numeric value.")


def collect_marks(num_subjects):
    """
    Collect marks for all subjects and return them as a list.
    """
    subjects = []
    marks = []
    print()
    for i in range(1, num_subjects + 1):
        name = input(f"  Enter name of Subject {i}: ").strip()
        if not name:
            name = f"Subject {i}"
        mark = get_mark(name)
        subjects.append(name)
        marks.append(mark)
        print()
    return subjects, marks


def calculate_total(marks):
    """Return the total of all marks."""
    return sum(marks)


def calculate_average(total, num_subjects):
    """Return the average percentage."""
    return total / num_subjects


def assign_grade(average):
    """
    Assign a letter grade based on average percentage.
    90–100 → A | 75–89 → B | 60–74 → C | 50–59 → D | <50 → Fail
    """
    if average >= 90:
        return "A", "Excellent"
    elif average >= 75:
        return "B", "Good"
    elif average >= 60:
        return "C", "Average"
    elif average >= 50:
        return "D", "Below Average"
    else:
        return "FAIL", "Failing"


def display_results(student_name, subjects, marks, total, average, grade, remark):
    """Display a clean, formatted result report."""
    max_marks = len(marks) * 100
    width = 50

    print("\n" + "=" * width)
    print("         STUDENT GRADE REPORT CARD")
    print("=" * width)
    print(f"  Student Name : {student_name}")
    print("-" * width)
    print(f"  {'Subject':<25} {'Marks':>10} {'/ Max':>8}")
    print("-" * width)
    for subject, mark in zip(subjects, marks):
        print(f"  {subject:<25} {mark:>10.1f} {' / 100':>8}")
    print("-" * width)
    print(f"  {'Total Marks':<25} {total:>10.1f} {f' / {max_marks}':>8}")
    print(f"  {'Average Percentage':<25} {average:>9.2f}%")
    print(f"  {'Grade':<25} {'  ' + grade:>10}")
    print(f"  {'Remark':<25} {'  ' + remark:>10}")
    print("=" * width)

    # Visual grade bar
    bar_filled = int(average / 5)   # scale 0-100 to 0-20 blocks
    bar = "█" * bar_filled + "░" * (20 - bar_filled)
    print(f"\n  Progress : [{bar}] {average:.1f}%")
    print("=" * width + "\n")


def main():
    """Main entry point for the Student Grade Calculator."""
    print("=" * 50)
    print("       STUDENT GRADE CALCULATOR")
    print("=" * 50)
    print()

    while True:
        # Get student name
        student_name = input("Enter Student Name: ").strip()
        if not student_name:
            student_name = "Student"

        print()

        # Get number of subjects
        num_subjects = get_subject_count()

        # Collect subject names and marks
        subjects, marks = collect_marks(num_subjects)

        # Perform calculations
        total   = calculate_total(marks)
        average = calculate_average(total, num_subjects)
        grade, remark = assign_grade(average)

        # Display report
        display_results(student_name, subjects, marks, total, average, grade, remark)

        # Ask to calculate for another student
        again = input("  Calculate for another student? (yes/no): ").strip().lower()
        print()
        if again not in ("yes", "y"):
            print("  Thank you for using the Student Grade Calculator!")
            print("=" * 50 + "\n")
            break


# ─────────────────────────────────────────────
if __name__ == "__main__":
    main()
