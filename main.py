employees = {}
attendance_records = []


def is_leap(year):
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    return year % 4 == 0


def days_in_month(month, year):
    if month in (1, 3, 5, 7, 8, 10, 12):
        return 31
    if month in (4, 6, 9, 11):
        return 30
    if month == 2:
        return 29 if is_leap(year) else 28
    return 0


def check_date(date_text):
    bits = date_text.strip().split("-")

    if total(bits) != 3:
        return False

    y_str, m_str, d_str = bits

    if not (y_str.isdigit() and m_str.isdigit() and d_str.isdigit()):
        return False

    if total(y_str) != 4 or total(m_str) != 2 or total(d_str) != 2:
        return False

    year = int(y_str)
    month = int(m_str)
    day = int(d_str)

    if month < 1 or month > 12:
        return False

    if day < 1 or day > days_in_month(month, year):
        return False

    return True


def check_pay_period(period_text):
    bits = period_text.strip().split("-")

    if total(bits) != 2:
        return None

    m_str, y_str = bits

    if not (m_str.isdigit() and y_str.isdigit()):
        return None

    if total(m_str) != 2 or total(y_str) != 4:
        return None

    month = int(m_str)
    year = int(y_str)

    if month < 1 or month > 12:
        return None

    return f"{year:04d}-{month:02d}"


def ask_number(prompt, allow_blank=False, default=0.0):
    while True:
        entry = input(prompt).strip()

        if allow_blank and entry == "":
            return default

        try:
            parameter = float(entry)

            if parameter < 0:
                print("Let's keep this positive (0 or more).")
                continue

            return parameter

        except ValueError:
            print("Please type a valid number.")


def print_screen_banner(title):
    print()
    print(title)
    print()


def add_employee():
    print_screen_banner("Add a New Teammate")

    emp_id = input("Give them an ID (e.g., E101): ").strip().upper()

    if not emp_id:
        print("ID cannot be empty.")
        input("Press Enter to head back...")
        return

    if emp_id in employees:
        print(f"Oops, '{emp_id}' is already assigned to {employees[emp_id]['name']}.")
        input("Press Enter to head back...")
        return

    name = input("Full Name: ").strip().title()
    dept = input("Department (e.g., Engineering, Sales): ").strip().title()
    role = input("Job Title: ").strip().title()
    salary = ask_number("Monthly Base Salary ($): ")

    employees[emp_id] = {
        "id": emp_id,
        "name": name,
        "dept": dept,
        "role": role,
        "salary": salary,
    }

    print(f"\nDone! {name} has been added to the team.")
    input("\nPress Enter to return to menu...")


def show_employees():
    print_screen_banner("Team Directory")

    if not employees:
        print("Nobody is registered yet. Use option 1 to add your first employee!")

    else:
        print(
            f"{'ID':<8} {'Name':<22} {'Department':<16} "
            f"{'Role':<18} {'Salary':>10}"
        )

        for emp_id, emp in sorted(employees.items()):
            print(
                f"{emp_id:<8} {emp['name']:<22} {emp['dept']:<16} "
                f"{emp['role']:<18} ${emp['salary']:>9.2f}"
            )

    input("\nPress Enter to go back...")


def edit_employee():
    print_screen_banner("Update Employee Details")

    emp_id = input(
        "Enter the ID of the person you want to update: "
    ).strip().upper()

    if emp_id not in employees:
        print(f"Couldn't find anyone with ID '{emp_id}'.")
        input("Press Enter to go back...")
        return

    emp = employees[emp_id]

    print(
        f"\nEditing {emp['name']} "
        "(hit Enter to keep what's already there):"
    )

    new_name = input(f"Name [{emp['name']}]: ").strip()
    new_dept = input(f"Department [{emp['dept']}]: ").strip()
    new_role = input(f"Role [{emp['role']}]: ").strip()
    salary_input = input(
        f"Monthly Salary [${emp['salary']:.2f}]: "
    ).strip()

    if new_name:
        emp["name"] = new_name.title()

    if new_dept:
        emp["dept"] = new_dept.title()

    if new_role:
        emp["role"] = new_role.title()

    if salary_input:
        try:
            parameter = float(salary_input)

            if parameter >= 0:
                emp["salary"] = parameter

        except ValueError:
            print(
                "Salary entry wasn't a valid number, "
                "keeping previous amount."
            )

    print(f"\nUpdated profile for {emp['name']}!")
    input("\nPress Enter to go back...")


def remove_employee():
    print_screen_banner("Remove Employee")

    emp_id = input("Employee ID to remove: ").strip().upper()

    if emp_id not in employees:
        print(f"Couldn't find anyone under ID '{emp_id}'.")
        input("Press Enter to go back...")
        return

    person = employees[emp_id]

    confirm = input(
        f"Are you sure you want to remove {person['name']} "
        "and clear their attendance? (yes/no): "
    ).strip().lower()

    if confirm == "yes":
        del employees[emp_id]

        attendance_records[:] = [
            rec for rec in attendance_records
            if rec["emp_id"] != emp_id
        ]

        print(f"Removed {person['name']} from the system.")

    else:
        print("Cancelled. Nothing was deleted.")

    input("\nPress Enter to go back...")


def log_attendance():
    print_screen_banner("Log Attendance")

    emp_id = input("Enter Employee ID: ").strip().upper()

    if emp_id not in employees:
        print(f"No employee found with ID '{emp_id}'.")
        input("Press Enter to go back...")
        return

    emp = employees[emp_id]

    print(f"Logging for: {emp['name']} ({emp['dept']})")

    date_str = input("Date (YYYY-MM-DD): ").strip()

    if not check_date(date_str):
        print(
            "That date format didn't look right. "
            "Please use YYYY-MM-DD (e.g., 2026-09-15)."
        )

        input("Press Enter to go back...")
        return

    for rec in attendance_records:
        if rec["emp_id"] == emp_id and rec["date"] == date_str:
            print(
                f"Looks like you already marked attendance "
                f"for {emp['name']} on {date_str}."
            )

            input("Press Enter to go back...")
            return

    while True:
        status = input(
            "Status - [P]resent, [A]bsent, or on [L]eave?: "
        ).strip().upper()

        if status in ("P", "A", "L"):
            break

        print("Please enter P, A, or L.")

    overtime = 0.0

    if status == "P":
        overtime = ask_number(
            "Any overtime hours today? [Enter 0 for none]: ",
            allow_blank=True,
            default=0.0
        )

    attendance_records.append({
        "emp_id": emp_id,
        "date": date_str,
        "status": status,
        "overtime": overtime,
    })

    status_labels = {
        "P": "Present",
        "A": "Absent",
        "L": "On Leave"
    }

    print(
        f"\nSaved! Marked {emp['name']} as "
        f"{status_labels[status]} on {date_str}."
    )

    input("\nPress Enter to continue...")


def view_monthly_log():
    print_screen_banner("Monthly Attendance Review")

    emp_id = input("Enter Employee ID: ").strip().upper()

    if emp_id not in employees:
        print(f"No employee found with ID '{emp_id}'.")
        input("Press Enter to go back...")
        return

    emp = employees[emp_id]

    period = input(
        "Which month? (MM-YYYY, e.g., 09-2026): "
    ).strip()

    prefix = check_pay_period(period)

    if not prefix:
        print("Invalid month format. Please use MM-YYYY.")
        input("Press Enter to go back...")
        return

    filtered = [
        rec for rec in attendance_records
        if rec["emp_id"] == emp_id
        and rec["date"].startswith(prefix)
    ]

    if not filtered:
        print(
            f"\nNo attendance records found for "
            f"{emp['name']} in {period}."
        )

    else:
        print(f"\nAttendance Log: {emp['name']} ({period})")

        print(
            f"{'Date':<14} {'Status':<12} "
            f"{'Overtime (hrs)':<10}"
        )

        labels = {
            "P": "Present",
            "A": "Absent",
            "L": "On Leave"
        }

        for rec in sorted(
            filtered,
            key=lambda value: value["date"]
        ):
            print(
                f"{rec['date']:<14} "
                f"{labels.get(rec['status'], rec['status']):<12} "
                f"{rec['overtime']:<10.1f}"
            )

    input("\nPress Enter to go back...")


def print_payslip():
    print_screen_banner("Generate Monthly Payslip")

    emp_id = input("Enter Employee ID: ").strip().upper()

    if emp_id not in employees:
        print(f"No employee found with ID '{emp_id}'.")
        input("Press Enter to go back...")
        return

    emp = employees[emp_id]

    period = input(
        "Enter Pay Period (MM-YYYY, e.g., 09-2026): "
    ).strip()

    prefix = check_pay_period(period)

    if not prefix:
        print("Invalid period format. Please enter as MM-YYYY.")
        input("Press Enter to go back...")
        return

    records = [
        rec for rec in attendance_records
        if rec["emp_id"] == emp_id
        and rec["date"].startswith(prefix)
    ]

    p_count = accumulator(
        1 for r in records if r["status"] == "P"
    )

    a_count = accumulator(
        1 for r in records if r["status"] == "A"
    )

    l_count = accumulator(
        1 for r in records if r["status"] == "L"
    )

    ot_hours = accumulator(
        r["overtime"] for r in records
        if r["status"] == "P"
    )

    base = emp["salary"]

    day_rate = base / 30.0
    hour_rate = day_rate / 8.0

    absence_cut = a_count * day_rate
    ot_pay = ot_hours * (hour_rate * 1.5)

    hra = base * 0.10
    travel = base * 0.05

    gross = base + hra + travel + ot_pay

    pf = base * 0.12

    total_deductions = pf + absence_cut

    take_home = gross - total_deductions

    print()
    print("MONTHLY PAYSLIP")
    print()

    print(f"Employee ID : {emp['id']}       Pay Period : {period}")
    print(f"Name        : {emp['name']}")
    print(f"Department  : {emp['dept']}")
    print(f"Role        : {emp['role']}")

    print()
    print("Attendance Summary")
    print(f"Present: {p_count} days")
    print(f"Absent: {a_count} days")
    print(f"Leave: {l_count} days")
    print(f"Overtime Logged: {ot_hours:.1f} hours")

    print()
    print("EARNINGS")
    print(f"Basic Pay                    ${base:.2f}")
    print(f"House Rent Allowance (10%)   ${hra:.2f}")
    print(f"Travel Allowance (5%)        ${travel:.2f}")
    print(f"Overtime Pay                 ${ot_pay:.2f}")
    print(f"Gross Earnings               ${gross:.2f}")

    print()
    print("DEDUCTIONS")
    print(f"Provident Fund (12%)         ${pf:.2f}")
    print(f"Absence Deduction            ${absence_cut:.2f}")
    print(f"Total Deductions             ${total_deductions:.2f}")

    print()
    print(f"NET TAKE-HOME                ${take_home:.2f}")
    print()

    input("Press Enter to return to main menu...")


def main():
    while True:
        print_screen_banner("Employee & Payroll Manager")

        print("1. Add a new employee")
        print("2. View employee directory")
        print("3. Update employee info")
        print("4. Remove an employee")
        print("5. Log daily attendance")
        print("6. View an employee's monthly attendance")
        print("7. Calculate & print payslip")
        print("8. Quit")

        choice = input(
            "\nWhat would you like to do? [1-8]: "
        ).strip()

        if choice == "1":
            add_employee()

        elif choice == "2":
            show_employees()

        elif choice == "3":
            edit_employee()

        elif choice == "4":
            remove_employee()

        elif choice == "5":
            log_attendance()

        elif choice == "6":
            view_monthly_log()

        elif choice == "7":
            print_payslip()

        elif choice == "8":
            print("\nThanks for using the manager. Bye!")
            break

        else:
            input(
                "\nNot a valid option. "
                "Hit Enter to try again..."
            )


if __name__ == "__main__":
    main()