#student manager system

students = []

def add_student():
    student = {}
    student = input("Please enter the student's name: ")
    students.append(student)
    print("Student added successfully")
    
def search_student():
    student = input("Please enter the student's name: ")
    for i in range(len(students)):
        if students[i] == student:
            print("Student found")
        else:
            print("Student not found")
            
            
def sort_students():
    for i in range(0, len(students)):
        for j in range(i+1, len(students)):
            if students[i] > students[j]:
                students[i], students[j] = students[j], students[i]
    print("Students sorted successfully")

def main():
    print("Welcome to the student manager system")
    print("1: Add a student")
    print("2: Search a student")
    print("3: Sort students")
    
    choice = input("Please enter your choice: ")
    
    if choice == "1":
        add_student()
    elif choice == "2":
        search_student()
    elif choice == "3":
        sort_students()