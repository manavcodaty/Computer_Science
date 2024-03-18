mem_num = 0
date_visit = 0

def check():
    if mem_num == 0 or len(mem_num) > 7 or date_visit == 0 or len(date_visit) > 8:
        print("Please enter the member number and date of visit.")
        return False


def append_value():
    while input("Do you want to continue? (y/n): ") == 'y':
        mem_num = int(input("Enter the member number: "))
        check()
        date_visit = input("Enter the date of visit: ")
        check()
        final = str(mem_num) + " " + date_visit

        
        while True:
            fileHandle = open("file.txt", "a")
            fileHandle.write(final + "\n")
            fileHandle.close()
            break
       # with open("file.txt", "a") as file:
       #     file.write(final + "\n")
            
            
def search():
    '''
    with open("file.txt", "r") as file:
        search = input("Enter the member number to search: ")
        for line in file:
            if search in line:
                print(line)
            else:
                print("Not found")
    '''
    search = input("Enter the member number to search: ")
    fileHandle = open("file.txt", "r")
    for i in range(len(fileHandle)):
        if search in fileHandle[i]:
            print(fileHandle[i])
        else:
            print("Not found")
                
                
def main():
    print("1. Input Visit")
    print("2. Search Visit")
    
    choice = int(input("Enter your choice: "))
    
    if choice == 1:
        append_value()
    elif choice == 2:
        search()
        
        
        
main()