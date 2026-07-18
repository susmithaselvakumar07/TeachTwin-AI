from database.id_generator import generate_teachtwin_id

departments = [
    "CSE",
    "IT",
    "AIDS",
    "ECE",
    "EEE",
    "MECH",
    "CIVIL",
    "MBA",
    "BCA",
    "MCA"
]

print("Available Departments")

for i, dept in enumerate(departments, start=1):
    print(f"{i}. {dept}")

choice = int(input("\nChoose Department Number: "))

department = departments[choice - 1]

teacher_id = generate_teachtwin_id(department)

print("\nGenerated TeachTwin ID:", teacher_id)
