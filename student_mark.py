import pretty_errors

StudentName = ["Ben", "Grace", "Holly", "Bob"]
ClassSize = len(StudentName)
SubjectMark = [[34, 12, 56, 78], [55, 87, 88, 91], [23, 23, 23, 23], [40, 45, 50, 55]]
SubjectNo = len(SubjectMark)
student_combined_mark = []
average = []
distinction = 0
merit = 0
passing = 0
fail = 0


def calc_combined_mark():
    for i in range(ClassSize):
        total = 0
        for j in range(SubjectNo):
            total += SubjectMark[i][j]
        student_combined_mark.append(total)
        print(StudentName[i], "has a combined mark of", student_combined_mark[i])


def calc_average_mark():
    for i in range(ClassSize):
        total = 0
        for j in range(SubjectNo):
            total += SubjectMark[i][j]
        average_temp = total / SubjectNo
        average_temp = round(average_temp, 2)
        average.append(average_temp)
        print(StudentName[i], "has an average mark of", average)


def award_grade():
    for i in range(ClassSize):
        if average[i] >= 70:
            print(f"{StudentName[i]} has got a Distinction")
            distinction += 1
        elif average[i] >= 55 and average[i] < 70:
            print(f"{StudentName[i]} has got a Merit")
            merit += 1
        elif average[i] >= 40 and average[i] < 55:
            print(f"{StudentName[i]} has got a Pass")
            passing += 1
        else:
            print(f"{StudentName[i]} has got a Fail")
            fail += 1


def output():
    for i in range(ClassSize):
        for j in range(SubjectNo):
            print(
                StudentName[i],
                "has a combined mark of",
                student_combined_mark[i],
                "and has an average mark of",
                average[i],
                "and has been awarded a grade of",
                award_grade[i],
            )
    print("The number of students who have been awarded a distinction is", distinction)
    print("The number of students who have been awarded a merit is", merit)
    print("The number of students who have been awarded a pass is", passing)
    print("The number of students who have been awarded a fail is", fail)


calc_combined_mark()
calc_average_mark()
award_grade()
output()
