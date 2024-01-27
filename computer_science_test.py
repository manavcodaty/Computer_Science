students = [""] * 30
test_1 = [0] * 30
test_2 = [0] * 30
test_3 = [0] * 30
total = [0] * 30
total_score = [0] * 30

def get_values():
    for i in range(30):
        students[i] = input("Enter student name: ")
        test_1[i] = int(input("Enter test 1 score: "))
        test_2[i] = int(input("Enter test 2 score: "))
        test_3[i] = int(input("Enter test 3 score: "))
        total_score[i] = test_1[i] + test_2[i] + test_3[i]
        
def validate():
    for i in range(len(test_1)):
        if test_1[i] < 0 or test_1[i] > 20:
            print("Invalid test 1 score.")
            get_values()
    for j in range(len(test_2)):
        if test_2[j] < 0 or test_2[j] > 25:
            print("Invalid test 2 score.")
            get_values()
    for x in range(len(test_3)):
        if test_3[x] < 0 or test_3[x] > 35:
            print("Invalid test 3 score.")
            get_values()
            
            
def calc_marks():
    for i in range(30):
        print(f"{students[i]} got {total_score[i]} marks.")
        total_marks += total[i]
        
    average = total_marks / 30
    print(f"The average score is {average}.")
    
    
    
def highest_score():
    for i in range(30):
        if total_score[i] > highest:
            highest = total_score[i]
            highest_name = students[i]
    print(f"{highest_name} got the highest score of {highest}.")
    
    
get_values()
calc_marks()
highest_score()

    